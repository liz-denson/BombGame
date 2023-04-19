from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import os
import pygame

# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Success")

# initialize pygame
pygame.init()

# create a frame to hold the success animation
success_frame = Frame(window)
success_frame.pack()

# load the success animation
success_path = os.path.join(os.getcwd(), "success.gif")
success_image = Image.open(success_path)
success_gif = ImageTk.PhotoImage(success_image)
success_gif.frame_num = 0  # add a frame_num attribute to the PhotoImage object

# get the number of frames in the animation
success_frames = []
for frame in ImageSequence.Iterator(success_image):
    success_frames.append(ImageTk.PhotoImage(frame))
success_gif.n_frames = len(success_frames)

# create a label to display the success animation
success_label = Label(success_frame, image=success_gif)
success_label.pack()

# animate the success
def animate_success():
    # update the animation if there are more frames to show
    if success_gif.frame_num < success_gif.n_frames - 1:
        # update the animation
        frame_num = (success_gif.frame_num + 1) % success_gif.n_frames
        success_gif.frame_num = frame_num
        success_label.configure(image=success_frames[frame_num])

        # schedule the next update
        window.after(50, animate_success)

# set up the animation and audio playback
def start_animation():
    # start the animation
    animate_success()

    # play the audio
    success_sound = os.path.join(os.getcwd(), "success.mp3")
    pygame.mixer.music.load(success_sound)
    pygame.mixer.music.play()

# wait for the window to close
window.protocol("WM_DELETE_WINDOW", pygame.quit)
window.after(0, start_animation)
window.mainloop()
