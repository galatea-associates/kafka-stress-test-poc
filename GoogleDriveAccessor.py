from DataGenerator import DataGenerator

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import io
import os
import argparse

SCOPES = 'https://www.googleapis.com/auth/drive'

class GoogleDriveAccessor(DataGenerator):
    def __init__(self, folder_id=None, output_folder="out"):
        self.__folder_ID = folder_id
        self.__output_folder = self.__process_path(path=output_folder)
        self.__service = None

    def __auth_gdrive(self):

        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.__service = build('drive', 'v3', http=creds.authorize(Http()))

    def __get_files_in_folder(self, folder):
        results = self.__service.files().list(
            q=' "'+folder+'" in parents',fields="files(*)").execute()
        return(results.get('files', []))

    def __download_items(self, items):
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                file_id = item['id']
                file_name = item['name']
                request = self.__service.files().get_media(fileId=file_id)
                fh = io.FileIO(self.__output_folder + file_name, 'w')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))

    def __process_path(self, path):
        if not path.endswith(os.path.sep):
            path += os.path.sep
        return path

    def __process_args(self, args):
        if args is None:
            return

        if "Folder ID" in args.keys():
            self.__folder_ID = args["Folder ID"]
        
        if "Output Directory" in args.keys():
            self.__output_folder = self.__process_path(path=args["Output Directory"])


    # In DataConfiguration.py, 'Data Args' field should look like:
    # {"Output Directory": "out",
    #  "Folder ID": "2342342341fsdfs342sdf"}
    def run(self, args=None):
        data = None

        self.__process_args(args=args)
        self.__auth_gdrive()

        items = self.__get_files_in_folder(folder=self.__folder_ID)

        self.__download_items(items=items)
        
        return data



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_id', type=str, required=True, help="")
    parser.add_argument('--output_folder', type=str, default="out", help="")
    return parser.parse_args()

def format_args(output_dir, folder_id):
    return {
        "Output Directory": output_dir,
        "Folder ID": folder_id
    }

if __name__ == "__main__":
    args=get_args()
    formatted_args = format_args(output_dir=args.output_folder, folder_id=args.folder_id)
    GoogleDriveAccessor().run(args=formatted_args)
    