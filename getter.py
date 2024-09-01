from mega import Mega
from pathlib import Path
import concurrent
import os
import json
import logging
import time


#04.08.24 : Key Features achieved, Idiot proofing still left


class mega_manager():

    def __init__(self):
        self.mg = Mega()
        self.sleep_time = 30
        self.uploads_folder = "./videos/" 
        self.threads = 8
        creds_path = "./mega_creds.json"

        if os.path.exists(creds_path):
            with open(creds_path,'r') as file:
                data = json.load(file)
                email=data['email']
                pwrd = data['password']
        else:
            print('No')
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.StreamHandler()])
        self.mega = self.mg.login(email,pwrd)



    def upload_file(self, dir_or_file_name, mega_folder_name, extensions=None):
        if extensions is None:
            extensions = []

        if not dir_or_file_name:
            # Default to uploads folder if dir_or_file_name is not provided
            dir_or_file_name = self.uploads_folder

        num_threads = self.threads
        folder_locate = self.mega.find(mega_folder_name)
        file_path = Path(dir_or_file_name)
        
        if folder_locate is None:
            cloud_folder = self.mega.create_folder(mega_folder_name)
            logging.info("Folder not found, creating folder!")
        else:
            cloud_folder = folder_locate[0]

        if not file_path.exists():
            logging.error(f"Error! Couldn't locate the specified path: {file_path}")
            return

        if file_path.is_dir():
            files_to_upload = []
            for extension in extensions:
                extension = ('.' + extension.lower()) if not extension.startswith('.') else extension.lower()
                for file in file_path.rglob('*'):
                    if file.is_file() and file.suffix.lower() == extension:
                        files_to_upload.append(file)
           
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                results = list(executor.map(lambda file: self.upload_individual_file(file, cloud_folder), files_to_upload))

            for result in results:
                if result:
                    logging.info(f"Uploaded: {result}")
                else:
                    logging.error("Failed to upload a file.")
                    
        else:
            logging.info("File found! Uploading specified file...")
            self.mega.upload(str(file_path), cloud_folder)
            logging.info("File has been uploaded successfully!")

    def upload_individual_file(self, file, cloud_folder):
        try:
            self.mega.upload(str(file.absolute()), cloud_folder)
            return file.name
        except Exception as e:
            logging.error(f"Failed to upload {file.name}: {e}")
            return None


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

    def download_file(self,folder_name):
        folder_descriptor = self.mega.find_path_descriptor(folder_name)
        if not folder_descriptor:
            logging.error("The Specified File couldn't be found.")
            return
        files = self.mega.get_files_in_node(folder_descriptor)
        logging.info(f"Found Folder '{folder_name}'!")
        file_names = []
        for file_id, file_info in files.items():
            if 'a' in file_info:
                logging.info(f"Found '{file_info['a']['n']}' in folder '{folder_name}'.ID : {file_id}")
                file_names.append(file_info['a']['n'])
        for name in file_names:
            logging.warning(f"Downloading '{name}'........")
            file = self.mega.find(name)
            link = self.mega.get_link(file)
            self.mega.download_url(url=link,dest_path=self.download_folder)
            logging.info(f"'{name}' Downloaded.")
        logging.info("All Files have been downloaded!")


    def folder_clean_up(self,folder_name):
        file_names = [] 
        folder_descriptor = self.mega.find_path_descriptor(folder_name)
        files = self.mega.get_files_in_node(folder_descriptor)
        delete_data = {
            "files":[]
        }
        for file_id, file_info in files.items():
            if 'a' in file_info:
                logging.info(f"Found '{file_info['a']['n']}' in folder '{folder_name}'.ID : {file_id}")
                file_names.append(file_info['a']['n'])
                file_data = {
                    "name" : file_info['a']['n'],
                    "id": file_id
                }
                delete_data['files'].append(file_data)
            
        logging.info(f"Found {len(delete_data['files'])} files in the folder '{folder_name}'!")
        
        for file in delete_data['files']:
            logging.warn(f"Downloading '{file['name']}'..........")
            file_in_node = self.mega.find(file['name'])
            link = self.mega.get_link(file_in_node)
            self.mega.download_url(url=link,dest_path=self.download_folder)
            logging.info(f"'{file['name']}' Downloaded..........")

        logging.info(f"All files from '{folder_name}' Downloaded!")
        logging.info(f"Sleeping for {self.sleep_time} seconds before deleting ")
        time.sleep(self.sleep_time)
        logging.warning(f"Files are being Deleted Now!")

        for file in delete_data['files']:
            logging.warning(f"Deleting {file['name']} Now!")
            self.mega.delete(file['id'])
            logging.info(f"'{file['name']}' Deleted!")
        logging.info(f'All Files have been deleted Successfully from {folder_name}')

        logging.info(f"Sleeping for {self.sleep_time} seconds before emptying the Recycle Bin")
        time.sleep(self.sleep_time)
        logging.warning("Emptying Recycle Bin Now!")
        self.mega.empty_trash()
        
mega_manager().upload_file(mega_folder_name="ThisIsAtest",extensions=['mp4' , 'wav'] , dir_or_file_name = None)

