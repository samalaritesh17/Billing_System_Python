import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

# Helper function to generate unique IDs
def generate_unique_id(file_path):
    if not os.path.exists(file_path):
        return 1
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Reverse the lines to find the last valid line
        for line in reversed(lines):
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Ensure the line is not empty
                try:
                    last_id = line.split(",")[0]
                    return int(last_id) + 1
                except ValueError:
                    continue  # Skip lines that cannot be converted to int
    return 1  # If no valid lines are found

# Save customer details
def save_customer_details(name, contact, file_path='files/customers.txt'):
    customer_id = generate_unique_id(file_path)
    with open(file_path, 'a') as file:
        file.write(f"{customer_id},{name},{contact}\n")
    return customer_id

# Save sales details
def save_sales(customer_id, emp_id, total_bill, file_path='files/sales.txt'):
    sale_id = generate_unique_id(file_path)
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, 'a') as file:
        file.write(f"{sale_id},{customer_id},{emp_id},{total_bill},{current_datetime}\n")
    return sale_id

# Reset GUI fields
def reset_billing_fields(gui):
    gui.customer_name_input.clear()
    gui.contact_input.clear()
    gui.product_input.clear()
    gui.quantity_input.setValue(1)
    gui.table.setRowCount(0)
    gui.total_label.setText("Total: $0.00")

def update_product_quantities(bill_items):
    try:
        # Load the CSV into a DataFrame
        products_df = pd.read_csv("files/products.csv")

        for item in bill_items:
            product_name = item["product_name"].capitalize() if item['product_name'][0].islower() else item["product_name"]
            quantity_bought = item['quantity']

            # Check if the product exists in the file
            if product_name in products_df['name'].values:
                # Update the quantity
                products_df.loc[products_df['name'] == product_name, 'quantity'] = (
                    products_df.loc[products_df['name'] == product_name, 'quantity'] - quantity_bought
                )
            else:
                print(f"Product '{product_name}' not found in the inventory.")

        # Ensure no negative quantities
        products_df['quantity'] = products_df['quantity'].clip(lower=0)

        # Write back to the CSV file
        products_df.to_csv("files/products.csv", index=False)
        print("Product quantities updated successfully.")

    except FileNotFoundError:
        print("Error: 'products.csv' file not found.")
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
    except Exception as e:
        print(f"Error updating product quantities: {e}")


def generate_supermarket_bill_pdf(sale_id, emp_name, bill_items, total_amount, file_path='files/bills'):
    # Ensure the bills folder exists
    os.makedirs(file_path, exist_ok=True)

    # File path for the PDF (force forward slashes)
    pdf_path = os.path.normpath(os.path.join(file_path, f"bill_{sale_id}.pdf")).replace("\\", "/")

    # Create the PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 16
    title_style.alignment = 1  # Center alignment

    normal_style = styles['Normal']
    normal_style.fontSize = 10

    bold_style = styles['Normal']
    bold_style.fontSize = 10
    bold_style.fontName = 'Helvetica-Bold'

    # Header Section
    elements.append(Paragraph("SUPERMARKET GODAVARIKHANI", title_style))
    elements.append(Paragraph("Laxminagar Godavarikhani, 505209, Opposite to Roopsangam Dresses", normal_style))
    elements.append(Spacer(1, 12))

    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elements.append(Paragraph(f"<b>Sale ID:</b> {sale_id}", bold_style))
    elements.append(Paragraph(f"<b>Employee Name:</b> {emp_name}", bold_style))
    elements.append(Paragraph(f"Date & Time: {date_time}", normal_style))
    elements.append(Spacer(1, 12))

    # Items Table Header
    table_data = [["S.No", "Product Name", "Quantity", "Unit Price", "Total Price"]]

    # Populate the Table with Items
    for i, item in enumerate(bill_items, start=1):
        product_name = item["product_name"]
        quantity = item["quantity"]
        price = item["price"]
        total = quantity * price
        table_data.append([str(i), product_name, str(quantity), f"{price:.2f}", f"{total:.2f}"])

    # Add Total Row
    table_data.append(["", "", "", "Total", f"{total_amount:.2f}"])

    # Create and Style the Table
    table = Table(table_data, colWidths=[30, 200, 50, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Footer Section
    thank_you_msg = Paragraph("Thank You! Visit Again!", title_style)
    elements.append(thank_you_msg)
    elements.append(Spacer(1, 12))

    notes = Paragraph("""Notes:<br/>
    1. No exchange or return of products once the bill is generated.<br/>
    2. Market is closed every Wednesday.<br/>
    3. For any queries, please reach us at supermarketgdk@gmail.com""", normal_style)
    elements.append(notes)

    # Build the PDF
    doc.build(elements)

    return pdf_path




# Get products from the file
def read_products(file_path='files/products.csv'):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return [line.strip().split(',') for line in file.readlines()]

# Get product price by name
def get_product_price(product_name, quantity, file_path='files/products.csv'):
    products = read_products(file_path)
    for product in products:
        if product[1].strip().lower() == product_name.strip().lower():  # Match product name (case insensitive)
            available_quantity = int(product[3])  # Stock quantity
            if available_quantity >= quantity:  # Sufficient quantity
                return float(product[2])  # Return price as float
            else:  # Insufficient quantity
                return f"Only {available_quantity} available in the mart!"
    return None  # Product not found

# Remove a product from the list
def remove_product(product_name, file_path='files/products.csv'):
    products = read_products(file_path)
    new_products = [p for p in products if p[0].lower() != product_name.lower()]
    with open(file_path, 'w') as file:
        for product in new_products:
            file.write(",".join(product) + "\n")

def get_employee_name(emp_id, file_path="files/employees.txt"):
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Assuming each line is in the format: empId,name,contact
                data = line.strip().split(",")
                if len(data) >= 2 and data[0] == emp_id:
                    return data[1]  # Return the name
        return None  # Return None if the emp_id is not found
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None