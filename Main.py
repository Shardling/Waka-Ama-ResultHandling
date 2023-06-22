#imports
import os
import csv
from tkinter import *
from tkinter import ttk
import time
#create a new window
win = Tk()
win.geometry("700x350")
#no toolbar
win.overrideredirect(True)
win.config(bg='gray10')

#when click starts or is moving window pos = mouse pos
def start_move(event):
    win.x = event.x
    win.y = event.y

#when click stops, however this creates an error but does not make the code stop running
def stop_move():
    win.x = None
    win.y = None

#move window
def do_move(event):
    deltax = event.x - win.x
    deltay = event.y - win.y
    x = win.winfo_x() + deltax
    y = win.winfo_y() + deltay
    win.geometry(f"+{x}+{y}")
def quitt(e):
    win.destroy()
#create a new title bar
title_bar = Frame(win, bg='gray4', relief="raised", bd=0)
title_bar.pack(expand=0, fill=X, side= TOP)
#if click on title bar, move with mouse
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", do_move)
#simulate normal title
title_label = Label(title_bar, text='Waka-Ama Results',bg='gray4', fg='white')
title_label.pack(side=LEFT, pady= 4, padx= 4)
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<ButtonRelease-1>", stop_move)
title_label.bind("<B1-Motion>", do_move)
#THE, the X button
close_label = Label(title_bar, text='  X  ',bg='gray4', fg='red', relief='sunken', bd=1)
close_label.pack(side=RIGHT, pady=4)
close_label.bind('<Button-1>', quitt)

win.update()
#function for finding files with keywords and storing them in a list
def Select_files_with_finals(folder_path: str, keyword: str, keyword_2: str) -> list:
    #looks for the path
    global folder_name
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
                    #else open window saying something is wrong
                    else:
                        break
    #so I can use this outside of the function
    return selected_files, other_files
#These are where the folder path and keywords are located
folder_path = "C:/Users/mtvpo/Code/.vscode/3.7B resource files"
keyword = "Final"
prompt_1 = Label(win, text="Enter The Year You Want the Data From:")
keyword_2_entry = Entry(win)
def get_data():
    global keyword_2, selected_file
    keyword_2 = keyword_2_entry.get()
    selected_file = Select_files_with_finals(folder_path, keyword, keyword_2)
    if keyword_2 not in folder_name:
        error = Tk()
        error_label = Label(error, text='Invalid Year or Year Not in Files. Please Try Again')
        error_label.pack()
get_button = Button(win, command=get_data)
prompt_1.pack()
keyword_2_entry.pack()
get_button.pack()
as_name = []
t_score = []

#GUI part 2
prompt_2 = Label(text="Click Button to Read Files Present", bg='gray10', fg='white')
prompt_2.pack()
def read_files():
    count = 0
    #Tells the user if their folders have the necessary files in them, this is subject to change
    if selected_file:
        #progress bar
        win.config(bg='gray10')
        progress_bar = ttk.Progressbar(win, orient='horizontal', length=200, mode='determinate')
        progress_bar.pack(pady=20)
        #for every valid file path in selected files
        for file_path in selected_files:
            #showing file being read
            file_show = Label(text=f'File being read:   {file_path}', bg='gray10', fg='white')
            file_show.pack()
            progress_bar['value'] += 100/len(selected_files)
            win.update_idletasks()
            time.sleep(0.1)
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
            file_show.destroy()
            win.update()
        progress_bar.destroy()
    else: 
        print(f"No files with the keyword '{keyword}' found in the folder.")
#button to starts previous code
border = LabelFrame(win, bg='blue', bd=1, relief=FLAT)
border.pack()
pls_read_files = Button(border, command=lambda: [read_files(), border.destroy(), prompt_2.destroy()] , bg='gray4', height=1, width= 10, relief=FLAT)
pls_read_files.pack()

#sorts both lists at the same time
def file_time():
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
    csv_file()

win.mainloop()
