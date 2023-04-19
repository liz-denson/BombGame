from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import os
import pygame

# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Explosion")

# initialize pygame
pygame.init()

# create a frame to hold the explosion animation
explosion_frame = Frame(window)
explosion_frame.pack()

# load the explosion animation
explosion_path = os.path.join(os.getcwd(), "explosion.gif")
explosion_image = Image.open(explosion_path)
explosion_gif = ImageTk.PhotoImage(explosion_image)
explosion_gif.frame_num = 0  # add a frame_num attribute to the PhotoImage object

# get the number of frames in the animation
explosion_frames = []
for frame in ImageSequence.Iterator(explosion_image):
    explosion_frames.append(ImageTk.PhotoImage(frame))
explosion_gif.n_frames = len(explosion_frames)

# create a label to display the explosion animation
explosion_label = Label(explosion_frame, image=explosion_gif)
explosion_label.pack()

# animate the explosion
def animate_explosion():
    # update the animation if there are more frames to show
    if explosion_gif.frame_num < explosion_gif.n_frames - 1:
        # update the animation
        frame_num = (explosion_gif.frame_num + 1) % explosion_gif.n_frames
        explosion_gif.frame_num = frame_num
        explosion_label.configure(image=explosion_frames[frame_num])

        # schedule the next update
        window.after(50, animate_explosion)

# set up the animation and audio playback
def start_animation():
    # start the animation
    animate_explosion()

    # play the audio
    explosion_sound = os.path.join(os.getcwd(), "explosion.mp3")
    pygame.mixer.music.load(explosion_sound)
    pygame.mixer.music.play()

# wait for the window to close
window.protocol("WM_DELETE_WINDOW", pygame.quit)
window.after(0, start_animation)
window.mainloop()
