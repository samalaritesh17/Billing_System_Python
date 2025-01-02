from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from billing_helpers import *
from pdfurl import *

class BillingWindow(QtWidgets.QWidget):
    def __init__(self, emp_id):
        super().__init__()
        self.emp_id = emp_id

        # Window settings
        self.setWindowTitle(f"Billing - Employee ID: {self.emp_id}")
        self.setGeometry(150, 150, 800, 600)
        self.setStyleSheet("background-color: #f9f9f9;")

        # Layouts
        main_layout = QtWidgets.QVBoxLayout(self)

        # Title
        title = QtWidgets.QLabel("Billing Section")
        title.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        title.setStyleSheet("color: #3b5998; margin: 10px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)

        # Customer Details Section
        customer_layout = QtWidgets.QHBoxLayout()
        customer_name_label = QtWidgets.QLabel("Customer Name:")
        customer_name_label.setFont(QtGui.QFont("Arial", 14))
        customer_name_label.setStyleSheet("color: #333;")
        customer_layout.addWidget(customer_name_label)

        self.customer_name_input = QtWidgets.QLineEdit()
        self.customer_name_input.setFont(QtGui.QFont("Arial", 14))
        self.customer_name_input.setPlaceholderText("Enter customer name")
        self.customer_name_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        customer_layout.addWidget(self.customer_name_input)

        contact_label = QtWidgets.QLabel("Contact:")
        contact_label.setFont(QtGui.QFont("Arial", 14))
        contact_label.setStyleSheet("color: #333;")
        customer_layout.addWidget(contact_label)

        self.contact_input = QtWidgets.QLineEdit()
        self.contact_input.setFont(QtGui.QFont("Arial", 14))
        self.contact_input.setPlaceholderText("Enter contact number")
        self.contact_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        customer_layout.addWidget(self.contact_input)

        main_layout.addLayout(customer_layout)

        # Product Search Section
        search_layout = QtWidgets.QHBoxLayout()
        product_label = QtWidgets.QLabel("Product Name:")
        product_label.setFont(QtGui.QFont("Arial", 14))
        product_label.setStyleSheet("color: #333;")
        search_layout.addWidget(product_label)

        self.product_input = QtWidgets.QLineEdit()
        self.product_input.setFont(QtGui.QFont("Arial", 14))
        self.product_input.setPlaceholderText("Enter product name")
        self.product_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        search_layout.addWidget(self.product_input)

        quantity_label = QtWidgets.QLabel("Quantity:")
        quantity_label.setFont(QtGui.QFont("Arial", 14))
        quantity_label.setStyleSheet("color: #333;")
        search_layout.addWidget(quantity_label)

        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setFont(QtGui.QFont("Arial", 14))
        self.quantity_input.setMinimum(1)
        self.quantity_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        search_layout.addWidget(self.quantity_input)

        add_button = QtWidgets.QPushButton("Add to Bill")
        add_button.setFont(QtGui.QFont("Arial", 14))
        add_button.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;"
                                 "hover {background-color: #218838;}")
        add_button.clicked.connect(self.add_to_bill)
        search_layout.addWidget(add_button)

        main_layout.addLayout(search_layout)

        # Items Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Product Name", "Price", "Quantity", "Total"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 4px;")
        main_layout.addWidget(self.table)

        # Actions Section
        actions_layout = QtWidgets.QHBoxLayout()
        total_button = QtWidgets.QPushButton("Calculate Total")
        total_button.setFont(QtGui.QFont("Arial", 14))
        total_button.setStyleSheet("background-color: #ffc107; color: white; padding: 8px; border-radius: 4px;"
                                   "hover {background-color: #e0a800;}")
        total_button.clicked.connect(self.calculate_total)
        actions_layout.addWidget(total_button)

        remove_button = QtWidgets.QPushButton("Remove Item")
        remove_button.setFont(QtGui.QFont("Arial", 14))
        remove_button.setStyleSheet("background-color: #dc3545; color: white; padding: 8px; border-radius: 4px;"
                                    "hover {background-color: #c82333;}")
        remove_button.clicked.connect(self.remove_item)
        actions_layout.addWidget(remove_button)

        generate_button = QtWidgets.QPushButton("Generate Bill")
        generate_button.setFont(QtGui.QFont("Arial", 14))
        generate_button.setStyleSheet("background-color: #007bff; color: white; padding: 8px; border-radius: 4px;"
                                      "hover {background-color: #0056b3;}")
        generate_button.clicked.connect(self.generate_bill)
        actions_layout.addWidget(generate_button)

        main_layout.addLayout(actions_layout)

        # Total Amount Label
        self.total_label = QtWidgets.QLabel("Total: $0.00")
        self.total_label.setFont(QtGui.QFont("Arial", 16))
        self.total_label.setStyleSheet("color: #3b5998; margin: 10px; text-align: right;")
        self.total_label.setAlignment(QtCore.Qt.AlignRight)
        main_layout.addWidget(self.total_label)


    def add_to_bill(self):
        product_name = self.product_input.text().strip()
        quantity = self.quantity_input.value()

        price = get_product_price(product_name, quantity)

        if isinstance(price, float):
            total = price * quantity
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(product_name))
            self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(quantity)))
            self.table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"{total:.2f}"))

            self.product_input.clear()
            self.quantity_input.setValue(1)

        elif isinstance(price, str):
            QtWidgets.QMessageBox.warning(self, "Insufficient Stock", price)

        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Product", "The entered product name does not exist!")

    def calculate_total(self):
        total_amount = 0
        for row in range(self.table.rowCount()):
            total_item = float(self.table.item(row, 3).text())
            total_amount += total_item

        self.total_label.setText(f"Total: ${total_amount:.2f}")

    def remove_item(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.table.removeRow(selected_row)

    def generate_bill(self):
        customer_name = self.customer_name_input.text().strip()
        contact = self.contact_input.text().strip()
        emp_id = self.emp_id
        emp_name = get_employee_name(emp_id)
        total_bill = float(self.total_label.text().split("$")[1])

        if customer_name and contact:
            # Collect items from the table
            bill_items = []
            for row in range(self.table.rowCount()):
                product_name = self.table.item(row, 0).text()
                quantity = int(self.table.item(row, 2).text())
                price = float(self.table.item(row, 1).text())
                bill_items.append({"product_name": product_name, "quantity": quantity, "price": price})

            # Save customer and sales details
            customer_id = save_customer_details(customer_name, contact)
            sale_id = save_sales(customer_id, emp_id, total_bill)

            # Generate Bill Receipt
            pdf_path = generate_supermarket_bill_pdf(sale_id, emp_name, bill_items, total_bill)
            print(pdf_path)

            # Upload the generated PDF to S3 and get the URL
            uploaded_pdf_url = upload_pdf_to_s3(pdf_path, bucket_name='billingsystemdata', folder_name='Bills')

            # Show a message box with the S3 URL
            QtWidgets.QMessageBox.information(self, "Bill Generated",
                                              f"Bill has been successfully generated and saved at:\n{uploaded_pdf_url}")

            # Update product quantities
            update_product_quantities(bill_items)

            #send sms to mobile number


            # Reset fields
            reset_billing_fields(self)
        else:
            QtWidgets.QMessageBox.warning(self, "Missing Details", "Please fill in customer name and contact.")


# Main execution
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    billing_window = BillingWindow()
    billing_window.show()
    sys.exit(app.exec_())
