from typing import List

import gspread


class GoogleSheetsService:
    def __init__(self, spreadsheet_name: str = "Product Images"):
        self.gc = gspread.service_account()
        self.wks = self.gc.open(spreadsheet_name).sheet1

    def get_items(
        self, product_list_column="Product", done_column="Processed"
    ) -> List[str]:
        """
        Will return the values in the product_list:column that have nothing on the done_column
        :param product_list_column:
        :param done_column:
        :return:
        """
        rows = self.wks.get_all_values()
        headers = rows[0]

        items_to_find = []
        for row in rows[1:]:
            row_dict = {header: row[idx] for idx, header in enumerate(headers)}
            if not row_dict[done_column]:
                items_to_find.append(row_dict[product_list_column])
        return items_to_find

    def update_description(
        self,
        item: str,
        description: str,
        product_list_column="Product",
        description_column="Description",
        done_column="Processed",
    ) -> List[str]:
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

            if row_dict[product_list_column] == item:
                self.wks.update_cell(
                    row_index, headers_dict[description_column], description
                )
                self.wks.update_cell(row_index, headers_dict[done_column], True)
                return True
        return False
