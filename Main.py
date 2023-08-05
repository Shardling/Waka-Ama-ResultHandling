#import modules
import os
import csv
from tkinter import *
import customtkinter as ctk
from tkinter import filedialog
import subprocess
ctk.set_appearance_mode("Dark")
#defining variables
as_name = []
t_score = []
keyword = 'Final'
final_file = "results.csv"
def file_selector():
    global folder_path
    folder_path = filedialog.askdirectory()
#new window for flagging errors
class errors:
    def __init__(error):
        error = ctk.CTk()
        error.geometry('200x50')
        error.eval('tk::PlaceWindow . center')
        error_label = ctk.CTkLabel(error, text='Invalid Entry. Please Try Again.')
        error_label.pack(pady=5)
        error.mainloop()
#main window
class window(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #set up buttons and entries for use later
        self.title('Waka-Ama Results Handling')
        self.geometry('350x325')
        self.eval('tk::PlaceWindow . center')
        self.button_1 = ctk.CTkButton(self, corner_radius=10, text="Select Folder", command=lambda: [file_selector()])
        self.button_1.pack(pady=10)
        self.label = ctk.CTkLabel(self, text='Enter Year')
        self.label.pack()
        self.entry = ctk.CTkEntry(self)
        self.entry.pack()
        #error handling
        def error_handling():
            global as_name, t_score
            try:
                keyword_2 = self.entry.get()
                if len(keyword_2) != 0:
                    int(keyword_2)                  
                    #uses function. the name explains it.
                    Select_files_with_finals(folder_path, keyword, keyword_2)
                    if len(selected_files) == 0:
                        errors()
                    else:
                        #uses another function and then regulates the output
                        read_files()
                        self.output.delete(0, END)
                        self.output.insert(0, absolute_folder_path_2)
                        if os.name == 'nt':  # For Windows
                            os.startfile(final_file)
                        elif os.name == 'posix':  # For macOS and Linux
                            subprocess.Popen(["open", final_file])
                        as_name = []
                        t_score = []
            except (OSError, csv.Error):
                print('error')
            except ValueError:
                errors()
                    
        #buttton letting user use the error handling. that is not the main purpose of the function though
        self.button_2 = ctk.CTkButton(self, text='Generate Output File', command=lambda: [error_handling()])
        self.button_2.pack(pady=20)
        self.output = ctk.CTkEntry(self, width=300)
        self.output.pack()
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
                    if len(keyword_2) == 4:
                        if keyword_2 in folder_name:
                            selected_files.append(file_path)
                        else:
                            break
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
    write_file()
def write_file():
    global t_score, as_name, absolute_folder_path_2
    absolute_folder_path_2 = os.path.abspath(final_file)
    #sorts both lists at the same time
    t_score, as_name = zip(*sorted(zip(t_score, as_name), reverse=True))
    #puts lists into a csv file
    with open("results.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Association Name", "Total Score"])
        for i in range(len(as_name)):
            writer.writerow([as_name[i], t_score[i]])
#main loop
win = window()
win.mainloop()
