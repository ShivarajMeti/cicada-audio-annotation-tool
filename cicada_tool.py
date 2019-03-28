import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import glob
import subprocess
from pygame import mixer
from tkinter import messagebox
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import glob
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pickle
import numpy as np
import matplotlib.animation as animation


###############################################################
              #Constants defined#
###############################################################

HEADER_FONT_STYLE = ("Arial Bold", 30, "bold")
FONT_STYLE_BUTTON = ("Arial Bold", 20, "bold")

# On increasing these values window size shrinks
INITIAL_HEIGHT_ADJUST = 250
INITIAL_WIDTH_ADJUST = 80

# On increasing these values window size enlarges
FINAL_HEIGHT_ADJUST = 100
FINAL_WIDTH_ADJUST = 500

#Height and width of buttons
BUTTONS_HEIGHT = 2
BUTTONS_WIDTH = 20

###############################################################
           #Initaliazing Tkinter  Window#
###############################################################
root = tk.Tk()

proc = subprocess.Popen(["xrandr  | grep \* | cut -d' ' -f4"], stdout=subprocess.PIPE, shell=True)
(OUT, ERR) = proc.communicate()
OUT = str(OUT).split("x")
HEIGHT_SIZE = str(int(int(OUT[0])/2)-INITIAL_HEIGHT_ADJUST)
WIDTH_SIZE = str(int(int(OUT[1])/2)-INITIAL_WIDTH_ADJUST)
root.geometry(HEIGHT_SIZE+"x"+WIDTH_SIZE)
root.title("Cicada")
root.resizable(0,0)

HEADER = Label(root,text="Audio Annotation Tool", underline=0, font=HEADER_FONT_STYLE).grid(row=0, column=10, pady=10)
CURRENT_INDEX = 0
ANNOTATION_ENTRY_VAR = StringVar(root)
mixer.init()



###############################################################
               #Audio Files Folder#
###############################################################
def browse_wav_files():
    """
	Get the folder path of .wav files
	"""
    filename = filedialog.askdirectory()
    global FOLDER_WAV_FILES
    FOLDER_WAV_FILES = glob.glob(filename+"/*.WAV")
    if len(FOLDER_WAV_FILES) == 0:
        messagebox.showerror("Error", "No Wav Files in Given path")
    else:
        SPECTROGRAM_TYPE_BUTTON.configure(state="normal")
        plot_wav_file(CURRENT_INDEX, SPEC_VAR.get())
        Label(root, text=FOLDER_WAV_FILES[0].split("/")[-1], font=FONT_STYLE_BUTTON).grid(row=4, column=10, sticky=(N, S, W, E), pady=10)
ASK_FOR_WAVFILE_DIR = Button(root, text="Audio Files Folder", fg="green", bd=3, relief="raised",
	                            command=browse_wav_files, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH,
	                            font=FONT_STYLE_BUTTON)
ASK_FOR_WAVFILE_DIR.grid(row=2, column=0, pady=10)


###############################################################
               #Annotations to Save#
###############################################################

def browse_folder_to_save_annotations():
    """
    Get the folder path to save the annotations
    """
    filename = filedialog.askdirectory()
    global FOLDER_TO_SAVE_ANNOTATIONS
    FOLDER_TO_SAVE_ANNOTATIONS = filename
ASK_FOR_ANNOTATION_DIR = Button(root, text="Annotations to save", bd=3, relief="raised", fg="green",
	                               command=browse_folder_to_save_annotations, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH,
	                               font=FONT_STYLE_BUTTON)
ASK_FOR_ANNOTATION_DIR.grid(row=3, column=0, pady=10)


###############################################################
                    #QUIT#
###############################################################
def _quit():
    """
	Function to quit the application
	"""
    root.quit()
    root.destroy()
quit_button = Button(root, text="Quit", bd=3, fg="green", relief="raised", command=_quit,
	                    font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
quit_button.grid(row=2, column=12, pady=10)


###############################################################
                #Spectrogram Area#
###############################################################
# Label text
SPEC_AREA = Label(root, text="Spectrogram Area",fg="green",
	                 font=FONT_STYLE_BUTTON).grid(row=3, column=10, pady=10)
Label(root, text="File name Appears here", fg="green",
	     font=("Arial Bold", 10, "bold")).grid(row=4, column=10, sticky=(N, S, W, E), pady=10)



###############################################################
                 #Details Button#
###############################################################
def get_details():
    try:
        total_annotations = len(glob.glob(FOLDER_TO_SAVE_ANNOTATIONS+"/*.pkl"))
        remaining_files = len(FOLDER_WAV_FILES) - (total_annotations)
        messagebox.showinfo("Details", "Total Annotations : " +str(total_annotations)+
                            "\n Total Remaining wav files: "+str(remaining_files))
    except NameError:
        messagebox.showerror("Path not specified", "Give path for saving annotations")


DETAILS_BUTTON = Button(root, text="Details", bd=3, relief="raised", fg="green", command=get_details,
	                       font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
DETAILS_BUTTON.grid(row=3, column=12, pady=10)



###############################################################
               #Embedding spectrogram onto Tkinter#
###############################################################
def plot_wav_file(index_value, type_spec):
    """
	Embedding the spectrogram
	"""
    HEIGHT_SIZE = str(int(int(OUT[0])/2)+FINAL_HEIGHT_ADJUST)
    WIDTH_SIZE = str(int(int(OUT[1])/2)+FINAL_WIDTH_ADJUST)
    root.geometry(HEIGHT_SIZE+"x"+WIDTH_SIZE)

    # root.geometry("1540x1450")
    fig = Figure(figsize=(9, 8), dpi=100)
    wav_file = FOLDER_WAV_FILES[index_value]
    sample_rate, samples = wavfile.read(wav_file)
    try:
        if samples.shape[1] == 2:
            samples = np.array([i[0] for i in samples])
    except:
        samples = samples
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    global AXES1
    AXES1 = fig.add_subplot(111)
    AXES1.specgram(samples[:], Fs=sample_rate, xextent=(0, int(len(samples)/sample_rate)),
    	              mode=type_spec, cmap=plt.get_cmap('hsv'), noverlap=5, scale_by_freq=True)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=10, pady=10)


###############################################################
               #Previous Audio Button#
###############################################################
def previous_audio_update_index():
    try:
        check_folder = len(FOLDER_WAV_FILES)
        global CURRENT_INDEX
        if CURRENT_INDEX == 0:
            return CURRENT_INDEX
        else:
            CURRENT_INDEX = CURRENT_INDEX - 1
            ANNOTATION_ENTRY_VAR.set("")
            Label(root, text=FOLDER_WAV_FILES[CURRENT_INDEX].split("/")[-1],
            	     font=FONT_STYLE_BUTTON).grid(row=4, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
            plot_wav_file(CURRENT_INDEX, SPEC_VAR.get())
            if mixer.music.get_busy():
                mixer.music.stop()

    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")



previous_audio_button = Button(root, text="<< Previous",bd=3,relief="raised",fg="green",
	                              command=previous_audio_update_index, font=FONT_STYLE_BUTTON,
	                              height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
previous_audio_button.grid(row=5, column=0, pady=10)



###############################################################
               #Next Audio Button
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
            Label(root, text=FOLDER_WAV_FILES[CURRENT_INDEX].split("/")[-1],
            	     font=FONT_STYLE_BUTTON).grid(row=4, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
            plot_wav_file(CURRENT_INDEX, SPEC_VAR.get())
            if mixer.music.get_busy():
                mixer.music.stop()
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="Next >>", bd=3, relief="raised", fg="green",
	                          command=next_audio_update_index, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=5, column=12, pady=10)


###############################################################
               #Play Audio Button#
###############################################################
def play_audio(index_value):
    """
	Play audio
	"""
    try:
        mixer.music.load(FOLDER_WAV_FILES[index_value])
        mixer.music.play()
    except NameError:
        messagebox.showerror("No Wav file", "No audio file to Play")

PLAY_BUTTON = Button(root, text="Play Audio", bd=3, fg="green",
	                    command=lambda: play_audio(CURRENT_INDEX), font=FONT_STYLE_BUTTON,
	                    height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
PLAY_BUTTON.grid(row=7, column=10, pady=10)


###############################################################
               #Annotation Entry Field#
###############################################################
ANNOTATIONS_ENTRY = Entry(root, textvariable=ANNOTATION_ENTRY_VAR, bd=5, relief="raised",
	                         font=("Arial Bold", 30, "bold")).grid(row=8, column=10)

Label(root, text="Spectrogram Type: ", fg="green",
	     font=FONT_STYLE_BUTTON).grid(row=7, column=12, sticky=(N, S, W, E), pady=10)


###############################################################
        #Dropdown for Seclecting Spectrogram type#
###############################################################
def change_spec(SPEC_VAR):
    """
    Function to change the spectrogram based on dropdown selection
    """
    plot_wav_file(CURRENT_INDEX, SPEC_VAR)

SPEC_TYPES = [
    'psd',
    'magnitude',
    'phase'
    ]

SPEC_VAR = StringVar(root)
SPEC_VAR.set(SPEC_TYPES[0])

SPECTROGRAM_TYPE_BUTTON = OptionMenu(root, SPEC_VAR, command=change_spec, *SPEC_TYPES)
SPECTROGRAM_TYPE_BUTTON.grid(row=8, column=12, pady=10)
SPECTROGRAM_TYPE_BUTTON.configure(font=30, height=3, width=30, state="disabled")


###############################################################
               #Save Annotations#
###############################################################
def save_annotations(index_value):
    """
	Function to save the annotations
	"""
    try:
        with open(FOLDER_TO_SAVE_ANNOTATIONS+"/"+FOLDER_WAV_FILES[index_value].split("/")[-1][:-4]+".pkl", "wb") as file_obj:
            pickle.dump(ANNOTATION_ENTRY_VAR.get().split(","), file_obj)
        next_audio_update_index()
    except NameError:
        messagebox.showerror("No Path", "Specify path to save annotations!")


def save_and_next_audio(event):
    """
	Binding the submit button to <Return> key
	"""
    save_annotations(CURRENT_INDEX)
    next_audio_update_index()
    play_audio(CURRENT_INDEX)

SUBMIT_BUTTON = Button(root, text="Submit", bd=3, relief="raised", fg="green",
	                      command=lambda: save_annotations(CURRENT_INDEX),
	                      font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
SUBMIT_BUTTON.grid(row=9, column=10, pady=10)
root.bind('<Return>', save_and_next_audio)

root.mainloop()


