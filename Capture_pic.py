from tkinter import Toplevel, Label


class CaptureClass:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title('Capture')
        self.window.geometry('320x120')
        Label(self.window, text='Capture is disabled in this local run.', font=('Arial', 12)).pack(expand=True)
        self.window.grab_set()
        self.window.focus_set()
