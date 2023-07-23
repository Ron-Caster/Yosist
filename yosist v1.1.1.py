import speech_recognition as sr
import os
import sys
import webbrowser
import psutil
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
        print('Could not understand audio.')
        return get_command()
def open_app(program):
    if program.lower() == 'explorer':
        os.system('explorer.exe')
    else:
        os.system('start "" "' + program + '"')
def search_and_open_app(program):
    os.system('start ms-settings:')
    with sr.Microphone() as source:
        print('Searching for app...')
        r.pause_threshold = 1
        r.phrase_threshold = 1
        audio = r.listen(source)
    try:
        print('Speech to text : ')
        app_name = r.recognize_google(audio)
        print(app_name)
        os.system('start ms-settings:search?query=' + app_name)
    except sr.UnknownValueError:
        print('Could not understand audio.')
def close_app(program):
    closed = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == program.lower() + '.exe':
            proc.kill()
            closed = True
    if closed:
        print(program + ' closed successfully.')
    else:
        print('Could not find ' + program + '.exe running.')
if __name__ == '__main__':
    file_explorer_opened = False
    while True:
        command = get_command()
        if 'open' in command:
            program = command.replace('open ', '')
            open_app(program)
            if program.lower() == 'explorer':
                file_explorer_opened = True
            else:
                file_explorer_opened = False
        elif 'search' in command:
            program = command.replace('search ', '')
            search_and_open_app(program)
        elif 'close' in command:
            program = command.replace('close ', '')
            close_app(program)
        elif 'exit' in command:
            sys.exit()