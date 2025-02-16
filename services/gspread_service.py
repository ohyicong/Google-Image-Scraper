from typing import List, Optional, Tuple

import gspread
import re


class GoogleSheetsService:
    def __init__(
        self, spreadsheet_name: str = "Product Images", sheet_name: Optional[str] = None
    ):
        self.gc = gspread.service_account()
        if sheet_name is None:
            self.wks = self.gc.open(spreadsheet_name).sheet1
        else:
            ss = self.gc.open(sheet_name)
            self.wks = ss.worksheet(sheet_name)

    def get_items(
        self,
        product_list_column="Product",
        done_column="Processed",
        sku_column: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Tuple[str, str]]:
        """
        Will return the values in the product_list:column that have nothing on the done_column, this returns a tuple with the product ID for image storage and the search query
        :param limit: for testing, specify the amount of max items you want to iterate on
        :param sku_column: the column name for the SKU unique identifier for a product
        :param product_list_column: column name for the human-readable name for a product
        :param done_column: column name for the processing status of the product row, true means it has already been processed by AI
        :return aa tuple containing the product ID for image storage and the search query
        """
        rows = self.wks.get_all_values()
        headers = rows[0]

        items_to_find: List[Tuple[str, str]] = []
        if limit is not None:
            iterable_rows = rows[1 : limit + 1]
        else:
            iterable_rows = rows[1:]
        for row in iterable_rows:
            row_dict = {header: row[idx] for idx, header in enumerate(headers)}
            if not row_dict[done_column]:
                cleaned_product = re.sub(
                    r"[\t\r\n]", "", row_dict[product_list_column]
                ).strip()
                search_string = cleaned_product
                if sku_column is not None:
                    search_string = f"{search_string} ({row_dict[sku_column]})"
                items_to_find.append((row_dict[sku_column], search_string))
        return items_to_find

    def update_description(
        self,
        item: str,
        description: str,
        product_list_column="Product",
        description_column="Description",
        done_column="Processed",
    ) -> bool:
        """
        Will return the values in the product_list:column that have nothing on the done_column
        :param done_column:
        :param description_column:
        :param description:
        :param item:
        :param product_list_column:
        :return:
        """
        rows = self.wks.get_all_values()
        headers = rows[0]
        headers_dict = {header: idx + 1 for idx, header in enumerate(headers)}

        items_to_find = []
        for row_index, row in enumerate(rows[1:], start=2):
            row_dict = {header: row[idx] for idx, header in enumerate(headers)}

            if row_dict[product_list_column] in item:
                self.wks.update_cell(
                    row_index, headers_dict[description_column], description
                )
                self.wks.update_cell(row_index, headers_dict[done_column], True)
                return True
        return False

    def update_product_image(
        self,
        item: str,
        image_url: str,
        product_list_column="Product",
        image_column="AI Image",
        done_column="Processed",
    ) -> bool:
        """
        Will return the values in the product_list:column that have nothing on the done_column
        :param image_column:
        :param image_url:
        :param done_column:
        :param item:
        :param product_list_column:
        :return:
        """
        rows = self.wks.get_all_values()
        headers = rows[0]
        headers_dict = {header: idx + 1 for idx, header in enumerate(headers)}

        items_to_find = []
        for row_index, row in enumerate(rows[1:], start=2):
            row_dict = {header: row[idx] for idx, header in enumerate(headers)}

            if row_dict[product_list_column] in item:
                self.wks.update_cell(
                    row_index, headers_dict[image_column], f'=IMAGE("{image_url}", 2)'
                )
                self.wks.update_cell(row_index, headers_dict[done_column], True)
                return True
        return False
