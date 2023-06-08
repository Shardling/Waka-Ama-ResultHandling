import os
#function for finding files with keywords and storing them in a list
def Select_files_with_finals(folder_path: str, keyword: str, keyword_2: str) -> list:
    #looks for the path
    global folder_name, selected_files, file_name
    absolute_folder_path = os.path.abspath(folder_path)
    #the list(s)
    selected_files = []
    other_files = []
    #parses through each file name and checks if keyword is in it.
    for root, dirs, files in os.walk(absolute_folder_path): 
        for file_name in files: 
            if keyword in file_name: 
                file_path = os.path.join(root, file_name)
                #from those files, check if the folder they are in have keyword_2 
                folder_name = os.path.dirname(file_path)
                for root, dirs, files in os.walk(folder_name):
                    #if it is in the folder name, append to selected_files
                    if keyword_2 in folder_name:
                        if os.path.isfile(file_path):
                            selected_files.append(file_path)
                    #else append to other_files list
                    else:
                        if os.path.isfile(file_path):
                            other_files.append(file_path)
    #so I can use this outside of the function
    return selected_files, other_files
#These are where the folder path and keywords are located
folder_path = "/Users/mtvpo/Downloads/3.7B resource files"
keyword = "Final" 
keyword_2 = "2017"
as_name = []
t_score = []
count = 0

#Tells the user if their folders have the necessary files in them, this is subject to change
selected_file = Select_files_with_finals(folder_path, keyword, keyword_2)
if selected_file: 
    #for every valid file path in selected files
    for file_path in selected_files:
        #open the file path as a file
        with open(file_path, 'r') as file: 
            #loop that reads line by line
            while True:
                file_content = file.readline()
                #skips the first line
                if count != 0:
                    #if there are no more lines to read
                    if not file_content:
                        #reset count so next file the first line can be skipped
                        count = 0
                        #bake
                        break
                    #splits line onto a list
                    step = file_content.split(",")
                    #error handling, if it isnt an integer, it will spit an arror out
                    try:
                        if int(step[0]) < 8:
                            f_score = 9 - int(step[0])
                        else:
                            f_score = 1
                    except:
                        f_score = 0
                    #if the 6th column's item does not already exist
                    if step[5] not in as_name:
                        #appends to list
                        as_name.append(step[5])
                        t_score.append(f_score)
                    #if the 6th column's item is already present within the list
                    else:
                        #get position of the item within list and then add new score to place in list that holds scores
                        a = as_name.index(step[5])
                        t_score[a] = t_score[a] + f_score
                else:
                    #first line skipped
                    count += 1
                #if there are no more lines to read
                if not file_content:
                    #reset count so next file the first line can be skipped
                    count = 0
                    #bake
                    break
else: 
    print(f"No files with the keyword '{keyword}' found in the folder.")

t_score, as_name = zip(*sorted(zip(t_score, as_name)))
brain = len(as_name)
while brain > 0:
    brain -= 1
    print(as_name[brain], t_score[brain])
