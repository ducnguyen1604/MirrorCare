import keyboard

# Record events until 'Esc' is pressed
recorded = keyboard.record(until="esc")

# Replay the recorded events at three times the speed
keyboard.play(recorded, speed_factor=3)


#