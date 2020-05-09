# copied and adapted from 
# https://raw.githubusercontent.com/unfor19/mg-tools/master/mgtools/get_key_pressed.py

from tkinter import Tk, Frame


def __set_key(e, root, key_pressed):
    if e.char:
        key_pressed['value'] = e.char
        root.destroy()


def get_key(msg="Press any key ...", time_to_sleep=3):
    if msg:
        print(msg)
    key_pressed = {"value": ''}
    root = Tk()
    root.overrideredirect(True)
    frame = Frame(root, width=0, height=0)
    frame.bind("<KeyRelease>", lambda f: __set_key(f, root, key_pressed))
    frame.pack()
    root.focus_set()
    frame.focus_set()
    frame.focus_force()  # doesn't work in a while loop without it
    root.after(time_to_sleep * 1000, func=root.destroy)
    try:
        root.mainloop()
    except KeyboardInterrupt as e:
            root.destroy()
            key_pressed['value'] = None
    root = None  # just in case
    return key_pressed['value']


def __main():
        c = ''
        while c == '':
                c = get_key("Choose your weapon ... ", 2)
        print(c)

if __name__ == "__main__":
    __main()
