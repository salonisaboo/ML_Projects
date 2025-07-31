import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import os
from easygui import buttonbox
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

# ---- GIF Display Class ----
class ImageLabel(tk.Label):
    """A label that displays GIFs (animated or static)."""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        try:
            for i in count(0):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc = (self.loc + 1) % len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


# ---- Build dynamic GIF phrase list ----
def get_gif_phrases(folder="ISL_Gifs"):
    phrases = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(".gif"):
                phrases.append(os.path.splitext(file)[0].lower())
    return phrases


isl_gif = get_gif_phrases()

def show_gif(gif_path):
    """Open and play a GIF in Tkinter."""
    if os.path.exists(gif_path):
        root = tk.Tk()
        root.title("Sign Language GIF")
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(gif_path)
        root.mainloop()
    else:
        print(f"[!] GIF not found: {gif_path}")


def func():
    r = sr.Recognizer()
    arr = string.ascii_lowercase

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("I am Listening...")
            try:
                audio = r.listen(source, phrase_time_limit=5)
                a = r.recognize_google(audio).lower()
                a = ''.join(ch for ch in a if ch not in string.punctuation)
                print(f"You Said: {a}")

                if a in ["goodbye", "good bye", "bye"]:
                    print("👋 Goodbye! Ending session.")
                    break

                elif a in isl_gif:
                    gif_path = os.path.join("ISL_Gifs", f"{a}.gif")
                    print(f"[GIF] Displaying {gif_path}")
                    show_gif(gif_path)

                else:
                    for char in a:
                        if char in arr:
                            img_path = os.path.join("letters", f"{char}.jpg")
                            if os.path.exists(img_path):
                                img = Image.open(img_path)
                                plt.imshow(np.asarray(img))
                                plt.axis("off")
                                plt.draw()
                                plt.pause(0.8)
                            else:
                                print(f"[!] Letter image not found: {img_path}")
                    plt.close()

            except sr.UnknownValueError:
                print("⚠️ Could not understand audio.")
            except sr.RequestError as e:
                print(f"⚠️ Could not request results; {e}")
            except Exception as e:
                print(f"⚠️ Error: {e}")


# ---- Main Menu ----
while True:
    image = "signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == choices[0]:
        func()
    elif reply == choices[1]:
        quit()
