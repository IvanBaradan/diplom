to exe:
pyinstaller --onefile --windowed --name tour_agency --add-data "database/tour_agency.db;database" --add-data "receipts;receipts" --add-data "assets/images;assets/images" main.py