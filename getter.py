from pathlib import Path
from mega import Mega
import os 
import json
import logging


class mega_manager():

    def __init__(self):
        self.mg = Mega()
        self.uploads_folder = "/home/smol/Contests/te/" 
        creds_path = "/home/smol/Contests/te/mega_creds.json"
        if os.path.exists(creds_path):
            with open(creds_path,'r') as file:
                data = json.load(file)
                email=data['email']
                pwrd = data['password']
        else:
            print('No')
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.StreamHandler()])
        self.mega = self.mg.login(email,pwrd)

# Uploads FIle  area 
    def upload_file(self, dir_or_file_name, mega_folder_name, extensions):
        folder_locate = self.mega.find(mega_folder_name)
        file_path = Path(self.uploads_folder) / dir_or_file_name

        if folder_locate is None:
            cloud_folder = self.mega.create_folder(mega_folder_name)
            logging.info("Folder not found, creating folder!")
        else:
            cloud_folder = folder_locate[0]

        if not file_path.exists():
            logging.error(f"Error! Couldn't locate the specified path: {file_path}")
            return

        if file_path.is_dir():
            for extension in extensions:
                extension = ('.' + extension.lower()) if not extension.startswith('.') else extension.lower()
                for file in file_path.rglob('*'):
                    if file.is_file() and file.suffix.lower() == extension:
                        self.mega.upload(str(file.absolute()), cloud_folder)
                        logging.info(f"Uploaded: {file.name}")
        else:
            logging.info("File found! Uploading specified file...")
            self.mega.upload(str(file_path), cloud_folder)
            logging.info("File has been uploaded successfully!")


    def delete_file(self, file_name, folder_name):
        file_to_delete = None
        folder_descriptor = self.mega.find_path_descriptor(folder_name)
        if not folder_descriptor:
            logging.error(f"Error! Specified Folder '{folder_name}' Couldn't be Located")
            return
        files = self.mega.get_files_in_node(folder_descriptor)
        for file_id, file_info in files.items():
            if 'a' in file_info and file_info['a']['n'] == file_name:
                file_to_delete = file_id
                break

        if file_to_delete:
            logging.info(f'File Specified : {file_name}, Found on Mega!')
            logging.warning(f"Deleting {file_name}")
            self.mega.delete(file_to_delete)
            logging.info(f'File {file_name} deleted successfully.')
        else:

            logging.error(f"Error! Specified File '{file_name}' Couldn't be Located in Folder '{folder_name}'")

mega_manager().upload_file(dir_or_file_name='videos' , mega_folder_name='clips', extensions=['mp3' , 'mp4'])
