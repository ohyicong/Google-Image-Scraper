from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from os import getenv
from os.path import join, basename
import platform


class GoogleDriveService:
    def __init__(self):
        self.current_os: str = platform.system()
        SCOPES = ["https://www.googleapis.com/auth/drive"]

        if self.current_os == "Windows":
            appdata_dir = getenv("APPDATA")
            self.credentials_path = join(appdata_dir, "gspread", "service_account.json")
        credentials = Credentials.from_service_account_file(
            self.credentials_path, scopes=SCOPES
        )
        self.drive_service = build("drive", "v3", credentials=credentials)

    def get_folder_id(self, folder_name):
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        results = (
            self.drive_service.files()
            .list(q=query, spaces="drive", fields="files(id, name)")
            .execute()
        )
        folders = results.get("files", [])

        if not folders:
            print(f"No folder found with name: {folder_name}")
            return None
        else:
            return folders[0]["id"]

    def upload_image_to_drive(self, image_path, folder_id):
        # file_name = image_path.split('/')[-1]
        file_name = basename(image_path)
        file_metadata = {
            "name": file_name,  # Use the file's name
            "parents": [folder_id],  # The folder where the image will be uploaded
        }
        media = MediaFileUpload(image_path, mimetype="image/jpeg")
        file = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")

    def set_file_public(self, file_id):
        permission = {"type": "anyone", "role": "reader"}
        self.drive_service.permissions().create(
            fileId=file_id, body=permission
        ).execute()
        return f"https://drive.google.com/uc?id={file_id}"


if __name__ == "__main__":
    service = GoogleDriveService()

    folder_id = service.get_folder_id("inventario")

    img_path = r"C:\Users\luis9\Documents\GitHub\Google-Image-Scraper\photos\AMD Ryzen 5800X3D\0_AMD_Ryzen_5800X3D.jpeg"
    file_id = service.upload_image_to_drive(img_path, folder_id)
    print(service.set_file_public(file_id))
