from yaab.yaab_store import YaabStoreService

if __name__ == "__main__":
    yaab_service = YaabStoreService()

    yaab_service.login()
    yaab_service.get_categories()
    yaab_service.get_extra_fields()
