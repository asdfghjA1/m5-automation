import os
import shutil

def delete_videos_folder():
    # Get the current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path to the "videos" folder
    folder_path = os.path.join(current_dir, "./videos")
    
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            # Delete the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the folder: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist.")

# Call the function to delete the folder
delete_videos_folder()
