# google-drive-remove-characters-in-files-names

## Goal
Go through all files of a Google Drive folder and replace specific characters in the names of all of the image files and then repeat the process through all subfolders.

## Context
In some search cases (in my case in Forge VTT / Foundry VTT modules), words aren't properly identified if they're concatenated with other characters.
- "photo_kitten.png" may not show up on a kitten search
- "photo kitten.png" will show up on a kitten search 

# Setup
- Rename the .env-template into .env
- Update the parent folder id
- You'll need a GCP project

# Dev
### Commands
- Virtual environment creation
```bash
python3 -m venv .venv
```
- Virtual environment activation
```bash
source .venv/bin/activate
```
- Installation of the requirements
```bash
pip install -r requirements.txt
```
- Update requirements.txt
```bash
pip freeze > requirements.txt
```
- Local GCP authentication (to avoid the use of a service account)
```bash
gcloud auth application-default login --scopes https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/cloud-platform 
```
- Authenticate with a relevant account
```bash
gcloud auth login
```

# TODO
- Obviously batch update
- See if I can connect directly to Forge to update the Asset Library