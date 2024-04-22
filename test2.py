import os
import pygame

def play_mp3(filename):
    # Initialize pygame
    pygame.mixer.init()

    try:
        # Load the mp3 file
        pygame.mixer.music.load(filename)

        # Play the mp3 file
        pygame.mixer.music.play()

        # Wait until music has finished playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error:
        print("Could not load or play the file.")

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Name of the mp3 file to play
    mp3_file = "kahoot.mp3"
    
    # Path to the mp3 file
    mp3_path = os.path.join(current_dir, mp3_file)

    # Play the mp3 file
    play_mp3(mp3_path)
