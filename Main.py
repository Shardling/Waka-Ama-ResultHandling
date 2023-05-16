#importing modules
import os

#function for finding files with keywords and storing them in a list
def Select_files_with_finals(folder_path: str, keyword: str) -> list:
    #looks for the path
    absolute_folder_path = os.path.abspath(folder_path)
    #the list
    selected_files = []
    for root, dirs, files in os.walk(absolute_folder_path): 
        for file_name in files: 
            if keyword in file_name: 
                file_path = os.path.join(root, file_name) 
                if os.path.isfile(file_path):
                    selected_files.append(file_path) 
    #so I can use this outside of the function
    return selected_files

#These are where the folder path and keywords are located
folder_path = "/Users/mtvpo/Downloads/3.7B resource files"
keyword = "Final" 

#Tells the user if their folders have the necessary files in them, this is subject to change
selected_files = Select_files_with_finals(folder_path, keyword) 
if selected_files: 
    for file_path in selected_files: 
        with open(file_path, 'r') as file: 
            file_content = file.read() 
            print(f"File: '{file_path}':") 
else: 
    print(f"No files with the keyword '{keyword}' found in the folder.") 
