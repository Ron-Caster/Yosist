import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import os
import win32com.client as wincl
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Assistant')
        panel = wx.Panel(self)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5), size=(350, 50), style=wx.TE_PROCESS_ENTER)
        self.text_ctrl.SetFont(font)
        self.text_ctrl.SetValue('Say something!')
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_press_enter)

        self.response_text = wx.StaticText(panel, label='', pos=(5, 100))
        self.response_text.SetFont(font)

    def on_press_enter(self, event):
        text = self.text_ctrl.GetValue()
        self.text_ctrl.SetValue('')

        # Use Google's speech recognition service to recognize the audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            # Listen for audio input
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said: ", text)

            # Use TextBlob to perform sentiment analysis
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            if sentiment > 0:
                response = "I'm glad to hear that!"
            elif sentiment < 0:
                response = "I'm sorry to hear that."
            else:
                response = "Hmm, I'm not sure what to say."

            # Use gTTS to generate a spoken response
            tts = gTTS(text=response, lang='en')
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")

            # Use PyWin32 to interact with Windows APIs
            if "open" in text:
                app = text.split("open")[1].strip()
                shell = wincl.Dispatch("WScript.Shell")
                shell.Run(app)
            elif "close" in text:
                app = text.split("close")[1].strip()
                os.system("taskkill /f /im " + app + ".exe")
                response = "Closing " + app
                tts = gTTS(text=response, lang='en')
                tts.save("response.mp3")
                os.system("mpg321 response.mp3")

            # Update the response text in the GUI
            self.response_text.SetLabelText(response)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()
