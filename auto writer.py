import keyboard
import random
from time import sleep
import sys
# text: the text to be typed
# wpm: average typing speed, measured in words per minute
# accuracy: float between 0 and 1, higher accuracy means less typos
# backspace_duration: time taken for backspace to be pressed
# correction_coefficient: determines how many typos are made before correcting them,
#                         lower coefficient means typos are caught quicker
# wait_key: press this key to start typing
# break_key: press this key to stop typing


def typoses(text,total_time=None, wpm = random.randint(15, 30), accuracy = 1, backspace_duration = 0.1, correction_coefficient = 0.4, wait_key = '', break_key = 'escape'):
    
    # Clean leading/trailing whitespaces from each line, preserve line breaks
    text = '\n'.join(line.lstrip() for line in text.splitlines())
    chars = list('abcdefghijklmnopqrstuvwxyz')

    total_chars = len(text)
    if total_time:
        spc = total_time / total_chars
    else:
    # seconds per character
        spc = 12 / wpm
    # determines how much the spc varies between characters
    spc_range = 0.8
    # as humans don't type at a constant rate, allow sleep duration between chars to vary
    spc_low = spc * (1 - spc_range)
    spc_high = spc * (1 + spc_range)

    i = 0
    typos = 0

    if wait_key:
        keyboard.wait(wait_key)

    while i < len(text):

        if keyboard.is_pressed(break_key):
            return

        # correct typos
        if typos and (i + typos >= len(text) or random.random() < 1 - correction_coefficient ** typos):
            sleep(backspace_duration)
            for _ in range(typos):
                keyboard.press_and_release('backspace')
                sleep(backspace_duration)
            typos = 0
        # make typo
        if random.random() > accuracy: 
            keyboard.write(random.choice(chars))
            typos += 1
        # type correct char
        else: 
            keyboard.write(text[i + typos])
            if typos:
                typos += 1
            else:
                i += 1

        duration = random.uniform(spc_low, spc_high)

        sleep(duration)

if __name__ == '__main__':
    print("Paste your text then press Ctrl+Z then Enter on Windows:")
    text = sys.stdin.read()
    total_time = float(input("Enter total time in seconds: "))
    typoses(text, total_time=total_time, wpm= random.randint(15,30), accuracy= 0.85, wait_key='f4')
