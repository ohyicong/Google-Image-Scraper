from services.gspread_service import GoogleSheetsService

if __name__ == "__main__":
    gs_service = GoogleSheetsService()

    items = gs_service.get_items("Product", "Images found")

    print(items)
