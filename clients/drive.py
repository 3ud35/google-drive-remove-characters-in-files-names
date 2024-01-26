import logging
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/drive"]


class Drive:
    """
    Initialize the drive service with default credentials
    """

    def __init__(self, credentials=None):
        if not credentials:
            # We get the default credentials
            credentials, _ = google.auth.default()
            try:
                # We try to generate the credentials with scopes (for local execution)
                credentials = credentials.with_scopes(SCOPES)
            except Exception as e:
                pass
        # We return the drive service
        self.service = build("drive", "v3", credentials=credentials, cache_discovery=False)

    """
    List files in a folder that have been created since x hours
    """

    def get_files_from_folder(self, parent_folder_id: str, mimeType: str) -> list:
        query = f"\"{parent_folder_id}\" in parents and trashed = false and mimeType contains '{mimeType}'"

        files = []
        try:
            continuation_token = ""
            while True:
                # https://developers.google.com/drive/api/reference/rest/v3/files/list
                response = (
                    self.service.files()
                    .list(
                        q=query,
                        pageToken=continuation_token,
                        supportsAllDrives=True,
                    )
                    .execute()
                )
                files.extend(response.get("files", []))
                continuation_token = response.get("nextPageToken", "")

                if not continuation_token:
                    break
            return files

        except HttpError as error:
            logging.error(f"An error occured while listing the files in the folder: {error}")
            return False

    def rename_file(self, file_id: str, new_name: str):
        try:
            request_body = {"name": new_name}
            self.service.files().update(fileId=file_id, body=request_body).execute()

        except HttpError as error:
            logging.error(f"An error occured while renaming a file: {error}")
            return False


class Drive_Rename(Drive):
    def remove_separators(self, folder_id: str, characters: list):
        images = self.get_files_from_folder(folder_id, "image")

        if len(images) > 0:
            counter = 0
            for image in images:
                for character in characters:
                    file_name = image.get("name")
                    if character in file_name:
                        new_name = file_name.replace(character, " ")
                        self.rename_file(image.get("id"), new_name)
                        logging.info(f"{file_name}   =>   {new_name}")
                        counter+= 1

            if counter > 0:
                logging.info(f"Images successfuly renamed in the folder {folder_id}")

        folders = self.get_files_from_folder(folder_id, "folder")
        if len(folders) > 0:
            for folder in folders:
                logging.info(f"##### FOLDER: {folder.get("name")}")
                self.remove_separators(folder.get("id"), characters)
