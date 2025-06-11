from tkinter import Tk
from gui.app import TourAgencyApp


def main():
    root = Tk()
    app = TourAgencyApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
