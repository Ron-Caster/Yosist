import speech_recognition as sr
import os
import sys
import webbrowser
import tkinter as tk

r = sr.Recognizer()
def get_command():
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.phrase_threshold = 1
        audio = r.listen(source)
    try:
        print('Speech to text : ')
        command = r.recognize_google(audio)
        print(command)
        return command.lower()
    except sr.UnknownValueError:
        print('....')
        return get_command()
def open_program():
    program = program_entry.get()
    os.system('explorer.exe')
    webbrowser.open(program)
def close_program():
    program = program_entry.get()
    os.system(f"TASKKILL /F /IM {program}.exe")
def exit_program():
    sys.exit()
root = tk.Tk()
root.title("Voice Recognition")
program_label = tk.Label(root, text="Program to open/close:")
program_label.pack()
program_entry = tk.Entry(root, width=30)
program_entry.pack()
open_button = tk.Button(root, text="Open program", command=open_program)
open_button.pack()
close_button = tk.Button(root, text="Close program", command=close_program)
close_button.pack()
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()
root.mainloop()
if __name__ == '__main__':
    while True:
        command = get_command()
        if 'open' in command:
            root.deiconify()
        elif 'close' in command:
            root.deiconify()
        elif 'exit' in command:
            sys.exit()