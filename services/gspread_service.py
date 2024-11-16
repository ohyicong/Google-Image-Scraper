from typing import List

import gspread


class GoogleSheetsService:
    def __init__(self, spreadsheet_name: str = "Product Images"):
        self.gc = gspread.service_account()
        self.wks = self.gc.open(spreadsheet_name).sheet1

    def get_items(self, product_list_column, done_column) -> List[str]:
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
            print("Done value: {}".format(row_dict[done_column]))
            if not row_dict[done_column]:
                items_to_find.append(row_dict[product_list_column])
        return items_to_find


