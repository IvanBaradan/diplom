# main.py

from tkinter import Tk
from gui.app import TourAgencyApp
from database import init_db

def main():
    init_db()
    root = Tk()
    app = TourAgencyApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
