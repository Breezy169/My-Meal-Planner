import tkinter as tk
from tkinter import messagebox
from MyMealPlanner import MyMealPlanner
import sys
import socket

# Instance-Check
def check_single_instance():
    global lock_socket
    lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock_socket.bind(("127.0.0.1", 65432))
    except socket.error:
        messagebox.showwarning("Warning", "The application is already running.")
        sys.exit()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My Meal Planner")
        self.geometry("1320x900")
        self.current_frame = None
        self.switch_frame(MyMealPlanner)

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    check_single_instance()
    app = App()
    app.mainloop()