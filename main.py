from PyQt5.QtWidgets import QApplication
import sys
from database import init_db
from gui.app import TourAgencyApp 

def main():

    init_db()
    

    app = QApplication(sys.argv)
    

    window = TourAgencyApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()