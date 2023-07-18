#imports
import os
import csv
from tkinter import *
import customtkinter as ctk
from tkinter import filedialog

#class creating a new window every time it is called.
class errors:
    def __init__(error):
        error = ctk.CTk()
        error.geometry('200x50')
        error.eval('tk::PlaceWindow . center')
        error_label = ctk.CTkLabel(error, text='Invalid Entry. Please Try Again.')
        error_label.pack(pady=5)
        error.mainloop()

#create a new window
win = ctk.CTk()
win.title('Waka-Ama Results Handling')
win.geometry("550x325")
ctk.set_appearance_mode("Dark")
win.eval('tk::PlaceWindow . center')

#opens file directory, once user has chosen the folder, moves to the next part of the code.
def end_folderselect():
    global folder_path
    folder_path = filedialog.askdirectory()
    select_button.destroy()
    ts_1()
select_button = ctk.CTkButton(win, corner_radius=10, text="Select Folder", command=lambda: [end_folderselect()])
select_button.pack()
win.update()
#function for finding files with keywords and storing them in a list
def Select_files_with_finals(folder_path: str, keyword: str, keyword_2: str) -> list:
    global folder_name, selected_files, file_name
    absolute_folder_path = os.path.abspath(folder_path)
    selected_files = []
    #parses through each file name and checks if keyword is in it.
    for root, dirs, files in os.walk(absolute_folder_path): 
        for file_name in files:
            if keyword in file_name:
                file_path = os.path.join(root, file_name)
                folder_name = os.path.dirname(file_path)
                for root, dirs, files in os.walk(folder_name):
                    #if it is in the folder name, append to selected_files
                    if keyword_2 in folder_name:
                        selected_files.append(file_path)
                    #else open window saying something is wrong
                    else:
                        break
#These are where the folder path and keywords are located
keyword = "Final"
#so i can control when this happens
def ts_1():
    keyword_2_entry = ctk.CTkEntry(win)
    #error handling, if it passes it moves to the next part of the code.
    def get_data():
        global keyword_2, selected_file
        keyword_2 = keyword_2_entry.get()
        try:
            int(keyword_2)
        except ValueError:
            errors()
        selected_file = Select_files_with_finals(folder_path, keyword, keyword_2)
        if len(selected_files) == 0:
            errors()
        else:
            keyword_2_entry.destroy()
            get_button.destroy()
            ts_2()
    #previous code will only run if this button is pressed
    get_button = ctk.CTkButton(win, command=get_data, text='Enter Year')
    keyword_2_entry.pack(pady=2)
    get_button.pack(pady=2)

as_name = []
t_score = []
def ts_2():
    #GUI part 2
    def read_files():
        count = 0
        count_2 = 0
        pg_val = 1/len(selected_files)
        pg_set = pg_val
        #progress bar
        progress_bar = ctk.CTkProgressBar(win, mode='determinate')
        progress_bar.set(0)
        progress_bar.pack(pady=20)
        #for every valid file path in selected files
        for file_path in selected_files:
            #showing file being read
            count_2 += 1
            file_num = ctk.CTkLabel(win, text=f'{count_2}/{len(selected_files)}')
            file_num.pack()
            file_show = ctk.CTkLabel(win, text=f'File being read:   {file_path}', font=('Roboto', 10))
            file_show.pack()
            progress_bar.set(pg_set)
            pg_set += pg_val
            win.update_idletasks()
            #open the file path as a file
            with open(file_path, 'r') as file: 
                while True:
                    file_content = file.readline()
                    if count != 0:
                        #if there are no more lines to read
                        if not file_content:
                            count = 0
                            break
                        step = file_content.split(",")
                        #error handling, if it isnt an integer, it will spit an arror out
                        try:
                            if int(step[0]) < 8:
                                f_score = 9 - int(step[0])
                            else:
                                f_score = 1
                        except:
                            f_score = 0
                        if step[5] != "":
                            #if the 6th column's item does not already exist
                            if step[5] not in as_name:
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
                        count = 0
                        break
            file_num.destroy()
            file_show.destroy()
            win.update()
        progress_bar.destroy()
        ts_3()
    #button to starts previous code
    pls_read_files = ctk.CTkButton(win, command=lambda: [read_files(), pls_read_files.destroy()], text='Read Files')
    pls_read_files.pack()
#sets up to be displayed later
def display_file():
    display_label = ctk.CTkEntry(win, width=220)
    display_label.insert(0, absolute_folder_path_2)
    display_label.pack(pady=4)
final_file = "results.csv"
def ts_3():
    global t_score, as_name, absolute_folder_path_2
    absolute_folder_path_2 = os.path.abspath(final_file)
    #sorts both lists at the same time
    t_score, as_name = zip(*sorted(zip(t_score, as_name), reverse=True))
    def csv_file():
        encodings = ["utf-16"]
        for encoding in encodings:
            #puts lists into a csv file
            try:
                with open("results.csv", "w", newline="", encoding=encoding) as file:
                    writer = csv.writer(file)
                    writer.writerow(["Association Name", "Total Score"])
                    for i in range(len(as_name)):
                        writer.writerow([as_name[i], t_score[i]])
            except OSError:
                continue
        files_button.destroy()
    files_button = ctk.CTkButton(win, text='Sort Data And Display File', command=lambda : [csv_file(), display_file()])
    files_button.pack(pady=8)
win.mainloop()
