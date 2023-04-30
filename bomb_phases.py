######################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Liz Denson & Caroline Holland
######################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
import pygame
from time import sleep
import os
import sys
# import photimage class from tkinter module
from PIL import Image, ImageTk, ImageSequence

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        self._hint = False
        # setup the initial "boot" GUI
        self.setupBoot()

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="green", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the hint button (defuses a random phase and reduces strikes left by 2)
            self._bhint = tkinter.Button(self, bg="yellow", fg="black", font=("Courier New", 18), text="Hint", anchor=CENTER, command=self.hint)
            self._bhint.grid(row=6, column=1, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button
        
   # hint button method
    def hint(self):
        self._hint = True

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bhint.destroy()
            self._bquit.destroy()
            
        # add the quit and retry buttons
        self._bretry = tkinter.Button(self, bg="green", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

        # if success is true
        if success:
            # set the gif image file path for the success gif
            image_file = os.path.join(os.getcwd(), "success.gif")
            # set the sound file path for the success mp3
            sound_file = os.path.join(os.getcwd(), "success.mp3")
        else:
            # set the image file path for the explosion gif
            image_file = os.path.join(os.getcwd(), "explosion.gif")
            # set the sound file path for the explosion mp3
            sound_file = os.path.join(os.getcwd(), "explosion.mp3")
        # call the function to display the right gif and play the sound file
        self.display_animated_image(image_file, sound_file)

    # display an animated image
    def display_animated_image(self, image_file, sound_file):
        # create a frame to hold the animated image with a black background
        animation_frame = Frame(self, bg="black")
        # position the frame in the grid
        animation_frame.grid(row=0, column=0, columnspan=3, sticky=EW)

        # open the image file
        animation_image = Image.open(image_file)

        # create a list to store all the animation frames
        animation_frames = []
        # iterate through the frames of the animation image
        for frame in ImageSequence.Iterator(animation_image):
            # append the PhotoImage object for each frame to the animation_frames list
            animation_frames.append(ImageTk.PhotoImage(frame))
        # store the number of frames in the animation
        num_frames = len(animation_frames)

        # create a label to display the animation with a black background
        animation_label = Label(animation_frame, bg="black")
        # pack the label inside the frame
        animation_label.pack()

        # initialize pygame.mixer
        pygame.mixer.init()
        # load the sound file
        pygame.mixer.music.load(sound_file)
        # play the sound file
        pygame.mixer.music.play()

        # define an inner function to animate the gif
        def animate(frame_num=0):
            # make animation_label, animation_frames, and num_frames accessible inside the function
            nonlocal animation_label, animation_frames, num_frames

            # update the label's image to display the current frame
            animation_label.configure(image=animation_frames[frame_num])

            # check if there are more frames to display
            if frame_num < num_frames - 1:
                # update the frame number
                next_frame_num = frame_num + 1
                # call the animate function after 50ms to keep the animation going
                self.after(50, animate, next_frame_num)

        # start the animation
        animate()

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)
    
    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False
        
# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1
        
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)
                
    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)
        
    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)
        
    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                # the combination is correct -> phase defused
                if (self._value == self._target):
                    self._defused = True
                # the combination is incorrect -> phase failed (strike)
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
            sleep(0.1)
            
    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
        
    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            sleep(0.1)
            
    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")
        
# the toggle phase
class Toggles(PhaseThread):
    # initialize the toggles class
    def __init__(self, component, target, name = "Toggles"):
        # call the superclass constructor
        super().__init__(name, component, target)
        # get the initial value from the component
        self._value = self._get_value()
        # set the previous value as the initial value
        self._prev_value = self._value
    
    
    # runs the thread
    def run(self):
        # set running to true
        self._running = True
        # while thread is running
        while (self._running):
            # get the current value from the component
            self._value = self._get_value()
            # check if the current value matches the target value
            if (self._value == self._target):
                # set defused to true if target value is reached
                self._defused = True
            # check if the current value has changed
            elif (self._value != self._prev_value):
                # check if the current value is in a wrong state
                if (self._check_wrong_state()):
                    # set failed to True if wrong state
                    self._failed = True
                # update the previous value to the current value
                self._prev_value = self._value
            # sleep
            sleep(0.1)

    # get the current value from the component
    def _get_value(self):
        value = []
        # iterate through the component pins
        for pin in self._component:
            # append the pin value as a string to the value list
            value.append(str(int(pin.value)))
        # join the pin values into a single string
        value = "".join(value)
        # convert the string value to an integer
        value = int(value, 2)
        return value

    # check if the current state is wrong
    def _check_wrong_state(self):
        # convert the current value to binary string
        value = bin(self._value)[2:].zfill(4)
        # convert the previous value to binary string
        prev = bin(self._prev_value)[2:].zfill(4)
        # convert the target value to binary string
        target = bin(self._target)[2:].zfill(4)
        # iterate through the binary strings
        for i in range(len(value)):
            # if a bit is different from the previous state
            if (value[i] != prev[i]):
                # check if the bit is same as target bit
                if (value[i] == target[i]):
                    return False
                else:
                    return True

    # returns the toggle's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # return the current value as a binary string
            return bin(self._value)[2:].zfill(4)
        
# the wire phase
class Wires(PhaseThread):
    # initialize the Wires class
    def __init__(self, component, target, name = "Wires"):
        # call the superclass constructor
        super().__init__(name, component, target)
        # get the initial value from the component
        self._value = self._get_value()
        # set the previous value as the initial value
        self._prev_value = self._value

    # runs the thread
    def run(self):
        # set running to True
        self._running = True
        # while thread is running
        while (self._running):
            # get the current value from the component
            self._value = self._get_value()
            # check if the current value matches the target value
            if (self._value == self._target):
                # set defused to true if target value is reached
                self._defused = True
            # check if the current value has changed
            elif (self._value != self._prev_value):
                # check if the current value is in a wrong state
                if (self._check_wrong_state()):
                    # set failed to True if wrong state
                    self._failed = True
                # update the previous value to the current value
                self._prev_value = self._value
            # sleep
            sleep(0.1)

    # get the current value from the component
    def _get_value(self):
        value = []
        # iterate through the component pins
        for pin in self._component:
            # append the pin value as a string to the value list
            value.append(str(int(pin.value)))
        # join the pin values into a single string
        value = "".join(value)
        # convert the string value to an integer
        value = int(value, 2)
        return value

    # check if the current state is wrong
    def _check_wrong_state(self):
        # convert the current value to binary string
        value = bin(self._value)[2:].zfill(5)
        # convert the previous value to binary string
        prev = bin(self._prev_value)[2:].zfill(5)
        # convert the target value to binary string
        target = bin(self._target)[2:].zfill(5)
        # iterate through the binary strings
        for i in range(len(value)):
            # if a bit is different from the previous state
            if (value[i] != prev[i]):
                # check if the bit is same as target bit
                if (value[i] == target[i]):
                    return False
                else:
                    return True

    # returns the wire's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # return the current value as a binary string
            return bin(self._value)[2:].zfill(5)
