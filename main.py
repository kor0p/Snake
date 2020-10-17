from pynput import keyboard
from Snake import *

options = 'finite=False, chance=25, foodLevel=1'
snake = main(options)

def on_press(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc:
        snake.stop()
    if k in snake.keys:
        snake.setnext(k)
    elif k == 'p':
        snake.pause()
    elif k == 'r':
        # lis.stop()
        snake.restart(options)
        # lis.start()

lis = keyboard.Listener(on_press=on_press)
lis.start() # start to listen on a separate threppad
#lis.join() # no this if main thread is polling self.keys

print('Press Esc to end game          ^C, ^D or enter .exit to exit\nPress any arrow key to start\n', up)
snake.start()
