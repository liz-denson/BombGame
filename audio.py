import pygame.mixer

pygame.mixer.init()

def play_audio():
    pygame.mixer.music.load('ticking.mp3')
    pygame.mixer.music.play(-1)

def pause_audio():
    pygame.mixer.music.pause()

def resume_audio():
    pygame.mixer.music.unpause()

def stop_audio():
    pygame.mixer.music.stop()
