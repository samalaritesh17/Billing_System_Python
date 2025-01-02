from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from billing_ui import BillingWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.emp_id = None
        self.billing_window = None
        self.setWindowTitle("Supermarket Billing System")
        self.setGeometry(100, 100, 900, 700)
        self.emp = ""

        # Set gradient background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(85, 98, 112, 255), stop:1 rgba(255, 107, 107, 255));
            }
        """)

        # Add Title
        title = QtWidgets.QLabel("Supermarket Billing System", self)
        title.setFont(QtGui.QFont("Arial", 26, QtGui.QFont.Bold))
        title.setGeometry(150, 50, 600, 70)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
        """)

        # Add Buttons
        billing_button = QtWidgets.QPushButton("Start Billing", self)
        billing_button.setGeometry(350, 200, 200, 60)
        billing_button.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        billing_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 12px;
                padding: 10px;
                font-weight: bold;
                border: 2px solid #2980b9;
                transition: background-color 0.3s, box-shadow 0.3s;
            }
            QPushButton:hover {
                background-color: #2980b9;
                box-shadow: 0px 0px 12px rgba(52, 152, 219, 0.8);
            }
        """)
        billing_button.clicked.connect(self.check_employee_id)

        exit_button = QtWidgets.QPushButton("Exit Application", self)
        exit_button.setGeometry(320, 300, 250, 60)
        exit_button.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 12px;
                padding: 10px;
                font-weight: bold;
                border: 2px solid #c0392b;
                transition: background-color 0.3s, box-shadow 0.3s;
            }
            QPushButton:hover {
                background-color: #c0392b;
                box-shadow: 0px 0px 12px rgba(231, 76, 60, 0.8);
            }
        """)
        exit_button.clicked.connect(self.close)

        # Add Footer
        footer = QtWidgets.QLabel("Powered by PyQt5", self)
        footer.setFont(QtGui.QFont("Arial", 12, italic=True))
        footer.setGeometry(0, 650, 900, 30)
        footer.setAlignment(QtCore.Qt.AlignCenter)
        footer.setStyleSheet("color: rgba(255, 255, 255, 0.7);")

    def check_employee_id(self):
        emp_id, ok = QtWidgets.QInputDialog.getText(self, "Employee ID", "Enter Employee ID:")

        if ok:
            emp_id = emp_id.strip()
            if self.is_valid_employee_id(emp_id):
                self.emp_id = emp_id
                self.open_billing(emp_id)
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid Employee ID", "The entered Employee ID does not exist.")

    def is_valid_employee_id(self, emp_id):
        try:
            with open('files/employees.txt', 'r') as f:
                Ids = []
                lines = f.readlines()
                for line in lines[1:]:
                    row = line.split(",")
                    Ids.append(int(row[0]))
            if int(emp_id) in Ids:
                return True
            return False
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error reading employee file: {e}")
            return False

    def open_billing(self, emp_id):
        print(f"Valid Employee ID: {emp_id}")
        self.billing_window = BillingWindow(self.emp_id)
        self.billing_window.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # Optional: Apply Fusion Style for a modern look
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
