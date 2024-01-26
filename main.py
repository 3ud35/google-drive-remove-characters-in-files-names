import os
from dotenv import load_dotenv
from clients.drive import Drive_Rename

load_dotenv()

characters_to_replace_by_space = ["_", "-"]


def main(parent_folder_id, characters):
    drive_client = Drive_Rename()

    drive_client.remove_separators(parent_folder_id, characters)


if __name__ == "__main__":
    main(os.getenv("GOOGLE_DRIVE_PARENT_FOLDER_ID"), characters_to_replace_by_space)
