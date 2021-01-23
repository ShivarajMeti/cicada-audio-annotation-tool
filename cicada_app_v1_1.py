"""
Tkinter GUI App to annotate auddio file('wav')
Author: Shivaraj Meti
"""

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import glob
import matplotlib
import os
import json
import csv
from pygame import mixer
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox



###############################################################
           #Initaliazing Tkinter  Window#
###############################################################
root = tk.Tk()

# Make a frame and having it fill the whole root window using pack
mainframe = tk.Frame(root)
mainframe.pack(fill=tk.BOTH, expand=1)


###############################################################
        #Reading configurations from JSON file#
###############################################################
with open("config_app.json",'r') as jsonfile_obj:
    data_json = jsonfile_obj.read()
datajson_obj = json.loads(data_json)
BUTTONS_HEIGHT = datajson_obj['ButtonsParams']['Height']
BUTTONS_WIDTH = datajson_obj['ButtonsParams']['Width']
CSV_FILENAME_ALREADY = datajson_obj['AnnotationsFile']['ExistingAnnotationFile']
CURRENT_CSV_FILENAME = datajson_obj['AnnotationsFile']['NewAnnotationFile']




###############################################################
           #Initialising constants#
###############################################################
CURRENT_INDEX = 0
FOLDER_WAV_FILES = []
FILES_LEFT_TO_ANNOTATE = []
FOLDER_TO_SAVE_ANNOTATIONS = ""
ANNOTATION_ENTRY_VAR = tk.StringVar(mainframe)
mixer.init()
if os.path.exists(CURRENT_CSV_FILENAME):
    with open(CURRENT_CSV_FILENAME, "w") as file_object:
        wavfile_information_object_initial = csv.writer(file_object)
        wavfile_information_object_initial.writerow(["Filename","Label1","Label2","Label3","Label4"])


###############################################################
           #Spectrogram Function#
###############################################################
def plot_wav_file(path_wavfile, type_spec):
    """
    Embedding the spectrogram
    """

    fig = Figure(figsize=(5, 2))
    wav_file = path_wavfile
    sample_rate, samples = wavfile.read(wav_file)
    try:
        if samples.shape[1] == 2:
            samples = samples[:,0]
    except:
        samples = samples
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    global AXES1
    AXES1 = fig.add_subplot(111)
    AXES1.specgram(samples[:], Fs=sample_rate, xextent=(0, int(len(samples)/sample_rate)),
                      mode=type_spec, cmap=plt.get_cmap('hsv'), noverlap=5, scale_by_freq=True)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    canvas = FigureCanvasTkAgg(fig, master=mainframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=3)


###############################################################
           #Quits Tkinter  Window#
###############################################################
def _quit():
    """
    Function to quit the application
    """
    mainframe.quit()
    mainframe.destroy()


###############################################################
           #Selects Folder to save#
###############################################################
def browse_folder_to_save_annotations():
    """
    Get the folder path to save the annotations
    """
    filename = filedialog.askdirectory()
    global FOLDER_TO_SAVE_ANNOTATIONS
    FOLDER_TO_SAVE_ANNOTATIONS = filename
    messagebox.showinfo("Folder Selected", "Annotations will be saved at: "+"\n"+os.path.join(filename,CURRENT_CSV_FILENAME))



###############################################################
           #Next Audio Update#
###############################################################
def next_audio_update_index():
    """
    Loop over the next audio if the directory
    """
    try:
        global CURRENT_INDEX
        if CURRENT_INDEX == len(FOLDER_WAV_FILES)-1:
            return CURRENT_INDEX
        else:
            CURRENT_INDEX = CURRENT_INDEX + 1
            ANNOTATION_ENTRY_VAR.set("")
            tk.Label(mainframe, text=os.path.basename(FILES_LEFT_TO_ANNOTATE[CURRENT_INDEX])).grid(row=1, column=3,pady=10)
            plot_wav_file(FILES_LEFT_TO_ANNOTATE[CURRENT_INDEX],'psd')
            if mixer.music.get_busy():
                mixer.music.stop()
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")


###############################################################
           #Previous Audio#
###############################################################
def previous_audio_update_index():
    check_folder = len(FOLDER_WAV_FILES)
    global CURRENT_INDEX
    if CURRENT_INDEX == 0:
        return CURRENT_INDEX
    else:
        CURRENT_INDEX = CURRENT_INDEX - 1
        ANNOTATION_ENTRY_VAR.set("")
        tk.Label(mainframe, text=os.path.basename(FILES_LEFT_TO_ANNOTATE[CURRENT_INDEX])).grid(row=1, column=3,pady=10)
        plot_wav_file(FILES_LEFT_TO_ANNOTATE[CURRENT_INDEX], 'psd')
        if mixer.music.get_busy():
            mixer.music.stop()



###############################################################
           #Browse Wav file folder#
###############################################################
def browse_wav_files():
    """
    Get the folder path of .wav files
    """
    filename = filedialog.askdirectory()
    print(filename)
    global FILES_LEFT_TO_ANNOTATE
    list_files = list(os.walk(filename))
    for root, dirs, files in list_files:
        for file in files:
            if file.endswith((".wav","WAV")):
                FOLDER_WAV_FILES.append(os.path.join(root,file))
            else:
                pass
    if len(FOLDER_WAV_FILES) == 0:
        messagebox.showerror("Error", "No Wav Files in Given path")
    else:
        FILES_LEFT_TO_ANNOTATE = FOLDER_WAV_FILES[:]
        plot_wav_file(FOLDER_WAV_FILES[0], 'psd')
        tk.Label(mainframe, text=os.path.basename(FOLDER_WAV_FILES[0])).grid(row=1, column=3)
    if os.path.exists(CSV_FILENAME_ALREADY):
        annotated_files = pd.read_csv(CSV_FILENAME_ALREADY, error_bad_lines=False)
        annotated_files = annotated_files['Filename'].values.tolist()
        track_annotated = 0
        for i in FILES_LEFT_TO_ANNOTATE:
            if os.path.basename(i) in annotated_files:
                track_annotated=track_annotated+1
                FILES_LEFT_TO_ANNOTATE.remove(i)
        print(len(FILES_LEFT_TO_ANNOTATE))
        messagebox.showinfo("Files Found:", "No. of audio files found: "+str(len(FOLDER_WAV_FILES))+ "\n"+"Files already Annotated: "+str(len(track_annotated)))

    else:
        messagebox.showinfo("Files Found:", "No. of audio files found: "+str(len(FOLDER_WAV_FILES)))


###############################################################
           #More Details# ( not implemented)
###############################################################
def get_details():
    try:
        # total_annotations = len(glob.glob(FOLDER_TO_SAVE_ANNOTATIONS+"/*.pkl"))
        total_annotations = pd.read_csv(CSV_FILENAME_ALREADY, error_bad_lines=False)
        total_annotations = len(total_annotations['Filename'].values.tolist())
        remaining_files = len(FILES_LEFT_TO_ANNOTATE) - (total_annotations)
        messagebox.showinfo("Details", "Total Annotations : " +str(total_annotations)+
                            "\n Total Remaining wav files: "+str(remaining_files))
    except (NameError, FileNotFoundError):
        messagebox.showerror("Path not specified", "Give path for saving annotations")


###############################################################
           #Play Audio#
###############################################################
def play_audio(index_value):
    """
    Play audio
    """
    try:
        mixer.music.load(FILES_LEFT_TO_ANNOTATE[index_value])
        mixer.music.play()
    except NameError:
        messagebox.showerror("No Wav file", "No audio file to Play")


###############################################################
           #Saves Annotations: Currently (csv only)#
###############################################################
def save_annotations(index_value):
    """
    Function to save the annotations
    """
    try:
        if os.path.exists(CURRENT_CSV_FILENAME):
            with open(CURRENT_CSV_FILENAME, "a") as file_object:
                wavfile_information_object = csv.writer(file_object)
                wavfile_information_object.writerow([os.path.basename(FILES_LEFT_TO_ANNOTATE[index_value])]+ ANNOTATION_ENTRY_VAR.get().split(","))
                print(os.path.basename(FILES_LEFT_TO_ANNOTATE[index_value])+" - " '{}'.format(ANNOTATION_ENTRY_VAR.get().split(",")))
        else:
            with open(CURRENT_CSV_FILENAME, "w") as file_object:
                wavfile_information_object = csv.writer(file_object)
                wavfile_information_object.writerow(["Filename","Label1","Label2","Label3","Label4"])
                wavfile_information_object.writerow([os.path.basename(FILES_LEFT_TO_ANNOTATE[index_value])]+ANNOTATION_ENTRY_VAR.get().split(","))
    except NameError:
        messagebox.showerror("No Path", "Specify path to save annotations!")


###############################################################
           #Binding Key Action#
###############################################################
def save_and_next_audio(event):
    """
    Binding the submit button to <Return> key
    """
    save_annotations(CURRENT_INDEX)
    next_audio_update_index()
    play_audio(CURRENT_INDEX)



###############################################################
           #Header and Title#
###############################################################
header_name = tk.Label(mainframe,text="Audio Annotation Tool", underline=0, font=5)
header_name.grid(row=0, column=3, sticky='s')



###############################################################
           #Row 1#
###############################################################
audio_files_folder = tk.Button(mainframe, text="Audio Files Folder", fg="green", bd=3, relief="raised",command=browse_wav_files, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
audio_files_folder.grid(row=1, column=1,sticky='s',padx=5, pady=5)
quit_option = tk.Button(mainframe, text="Quit", fg="green", bd=3, relief="raised",command=_quit, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
quit_option.grid(row=1, column=6,sticky='s',padx=5, pady=5)


###############################################################
           #Row 2#
###############################################################
annotations_to_save = tk.Button(mainframe, text="Annotations to Save", fg="green", bd=3, relief="raised",command=browse_folder_to_save_annotations, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
annotations_to_save.grid(row=2, column=1,sticky='n',padx=5, pady=5)
file_details = tk.Button(mainframe, text="File Details", fg="green", bd=3, relief="raised",command=get_details, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
file_details.grid(row=2, column=6,sticky='n',padx=5, pady=5)


###############################################################
           #Row 4#
###############################################################
next_button = tk.Button(mainframe, text=" Next >> ", fg="green", bd=3, relief="raised",command=next_audio_update_index, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
next_button.grid(row=4, column=6,padx=5, pady=5)
prev_button = tk.Button(mainframe, text=" << Previous ", fg="green", bd=3, relief="raised",command=previous_audio_update_index, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
prev_button.grid(row=4, column=1,padx=5, pady=5)




###############################################################
           #Row 7 Text#
###############################################################
annotation_text = tk.Entry(mainframe, textvariable=ANNOTATION_ENTRY_VAR, bd=5, relief="raised",font=("Arial Bold", 30, "bold"))
annotation_text.grid(row=7, column=3, sticky='s')


###############################################################
           #Play & submit button#
###############################################################
play_button = tk.Button(mainframe, text="Play Audio", bd=3, fg="green",command=lambda: play_audio(CURRENT_INDEX),height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
play_button.grid(row=4, column=3, padx=5, pady=5)


submit_button = tk.Button(mainframe, text="Submit to Save", bd=3, relief="raised", fg="green",command=lambda: save_annotations(CURRENT_INDEX),
                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
submit_button.grid(row=8, column=3)


###############################################################
           #Configuring row and columns#
###############################################################
for each_row in range(0,10,1):
    mainframe.grid_rowconfigure(each_row, weight=1)


for each_col in range(0,7,1):
    mainframe.grid_columnconfigure(each_col, weight=1)


root.bind('<Return>', save_and_next_audio)
###############################################################
           #Main Loop#
###############################################################
root.mainloop()