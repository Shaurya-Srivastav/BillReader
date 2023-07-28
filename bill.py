import streamlit as st
import pytesseract
from PIL import Image
import re
import pandas as pd
import sqlite3
import base64

# Function to find the highest total value from the extracted text
def find_highest_total_value(text):
    # Define regular expression to match currency values
    num_regex = r"\$?(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)"

    # Define keywords that indicate the total value
    total_keywords = ["total"]

    # Create a dictionary to store total values along with their line numbers
    total_values_dict = {}

    # Iterate through lines and find the line with the total value
    lines = text.split('\n')
    for line_num, line in enumerate(lines, 1):
        if any(keyword in line.lower() for keyword in total_keywords):
            # Extract numeric values from the line using regex
            numeric_values = re.findall(num_regex, line)

            # Convert the numeric values to floating-point numbers
            total_values = [float(value.replace(",", "")) for value in numeric_values]

            # Find the largest numeric value, which is likely the total amount
            if total_values:
                total_value = max(total_values)
                total_values_dict[total_value] = line_num

    # If the total value is found, return the highest total value and its line number
    if total_values_dict:
        highest_total_value = max(total_values_dict)
        highest_total_line_num = total_values_dict[highest_total_value]
        return highest_total_value

    # If the total value is not found, return None
    return None

# Function to create the SQLite database table if it doesn't exist
def create_table():
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            comment TEXT NOT NULL,
            image BLOB NOT NULL,
            amount REAL NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()

# Function to insert bill details into the database
def insert_bill_details(name, date, comment, image, amount):
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bills (name, date, comment, image, amount) VALUES (?, ?, ?, ?, ?)", (name, date, comment, image, amount))
    connection.commit()
    connection.close()

# Function to retrieve bill details from the database
def get_bill_details():
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, date, comment, amount FROM bills")
    bill_details = cursor.fetchall()
    connection.close()
    return bill_details

# Function to delete all bill details from the database
def delete_all_bill_details():
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bills")
    connection.commit()
    connection.close()

# Main function to run the Streamlit app
def main():
    st.title("AI Bill Assistant")

    # Create the database table if it doesn't exist
    create_table()

    # Collect bill details from the user using a form
    with st.form("bill_form"):
        name = st.text_input("Bill Name")
        date = st.date_input("Bill Date")
        comment = st.text_area("Comment")
        image = st.file_uploader("Upload Bill Image", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"])

        submitted = st.form_submit_button("Submit")

    if submitted and name and comment and image is not None:
        # Convert the uploaded image to a PIL image object
        pil_image = Image.open(image)
        # Extract text from the image
        extracted_text = pytesseract.image_to_string(pil_image)

        if extracted_text:
            # Find the highest total value from the current text
            total_value = find_highest_total_value(extracted_text)

            if total_value is not None:
                # Save the image as a binary large object (BLOB)
                image_binary = image.read()

                # Insert bill details into the database
                insert_bill_details(name, date, comment, image_binary, total_value)

    # Get bill details from the database
    bill_details = get_bill_details()

    if bill_details:
        # Create a DataFrame for bill details
        bill_df = pd.DataFrame(bill_details, columns=["ID", "Name", "Date", "Comment", "Amount"])

        # Calculate and display the total value of all bills
        total_value = bill_df["Amount"].sum()
        st.write(f"Total value of all bills: ${total_value:.2f}")

        # Display the bill details in a table
        st.table(bill_df[["ID", "Name", "Date", "Comment", "Amount"]])

        # Add a "Clear All" button to delete all bill details
        if st.button("Clear All"):
            # Delete all bill details from the database
            delete_all_bill_details()

    else:
        st.write("No bill details found.")

if __name__ == "__main__":
    main()
