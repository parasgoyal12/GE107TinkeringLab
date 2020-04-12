from tkinter import *
tk = Tk()

def toggle_fullscreen(state, event=None):
    state = not state  # Just toggling the boolean
    tk.attributes("-fullscreen", state)
    return "break"

def end_fullscreen(state, event=None):
    state = False
    tk.attributes("-fullscreen", False)
    return "break"

# self.tk = Tk()
tk.configure(background='black')
topFrame = Frame(tk, background = 'black')
bottomFrame = Frame(tk, background = 'black')
topFrame.pack(side = TOP, fill=BOTH, expand = YES)
bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
state = False
tk.bind("<Return>", toggle_fullscreen(state))
tk.mainloop()
# tk.bind("<Escape>", end_fullscreen(state))
