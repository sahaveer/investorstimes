import os
import shutil
source_directory = './pickl/'

def move_to_pick(source_path):


all_files = os.listdir(source_directory)
for file_name in all_files :
    if file_name.endswith(".pkl"):  # Check if it's a pickle file
        first_letter = file_name[0].upper()  # Get the first letter and convert it to uppercase
        folder_path = os.path.join(source_directory, first_letter)
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Move the pickle file to the corresponding folder
        source_path = os.path.join(source_directory, file_name)
        destination_path = os.path.join(folder_path, file_name)
        shutil.move(source_path, destination_path)

