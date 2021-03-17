# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# # The ID of a sample document.
# DOCUMENT_ID = '1QxxVC5utakcVgwWttJK5u53v876k0irS'

# def main():
#     """Shows basic usage of the Docs API.
#     Prints the title of a sample document.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('docs', 'v1', credentials=creds)

#     # Retrieve the documents contents from the Docs service.
#     document = service.documents().get(documentId=DOCUMENT_ID).execute()

#     print('The title of the document is: {}'.format(document.get('title')))


# if __name__ == '__main__':
#     main()

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload
import shutil
import sys
import json


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata']

def main():
    """get the file in terms of docx...
    """
#     from pydrive.auth import GoogleAuth
#     from pydrive.drive import GoogleDrive
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()
#     drive = GoogleDrive(gauth)

#     file3 = drive.CreateFile({'id': '1QxxVC5utakcVgwWttJK5u53v876k0irS'})
#     file3.GetContentFile('world.docx')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    string = json.load('token.json')
    print(string)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    drive = build('drive', 'v3', credentials=creds)
    request = drive.files().export_media(fileId='1aKf0ffoL7XjR26npjBmNcKClULSlGDIrlQx_E8dNXxI',  mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    with open('CV.pdf', 'wb') as f: # it's only been loaded into RAM!
        shutil.copyfileobj(fh, f, length=131072)
    
if __name__ == '__main__':
    main()
    print('done!')
