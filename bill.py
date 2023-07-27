
import streamlit as st
import pytesseract
from PIL import Image
import re
import pandas as pd
import sqlite3
import base64


# Custom caching mechanism for the extract_text_from_image function
@st.cache(allow_output_mutation=True)
def extract_text_from_image(image):
    try:
        # Convert the image to RGB format
        image = image.convert("RGB")

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)

        return extracted_text
    except Exception as e:
        st.error(f"Error: {e}")
        return None


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

# Function to format currency values as a string
def format_currency(amount):
    return "${:,.2f}".format(amount)

# Function to create the SQLite database table if it doesn't exist
def create_table():
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY,
            image TEXT NOT NULL,
            amount REAL NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()

# Function to insert bill details into the database
def insert_bill_details(image_base64, amount):
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bills (image, amount) VALUES (?, ?)", (image_base64, amount))
    connection.commit()
    connection.close()

# Function to retrieve bill details from the database
def get_bill_details():
    connection = sqlite3.connect("bill_details.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bills")
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

    # Move the upload button to the sidebar
    uploaded_images = st.sidebar.file_uploader(
        "Upload multiple images",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"],
        accept_multiple_files=True,
    )

    clear_all = st.sidebar.button("Clear All")

    # Initialize extracted_texts list
    extracted_texts = []

    if uploaded_images:
        # List to store the extracted texts from all images

        for image in uploaded_images:
            # Convert the uploaded image to a PIL image object
            pil_image = Image.open(image)

            # Extract text from the image
            extracted_text = extract_text_from_image(pil_image)

            if extracted_text:
                extracted_texts.append(extracted_text)

                # Find the highest total value from the current text
                total_value = find_highest_total_value(extracted_text)

                if total_value is not None:
                    # Save the image as a base64 string
                    image_base64 = base64.b64encode(image.read()).decode("utf-8")

                    # Insert bill details into the database
                    insert_bill_details(image_base64, total_value)

        # Clear the uploaded images
        uploaded_images.clear()

    if clear_all:
        # Delete all bill details from the database
        delete_all_bill_details()
        # Clear the extracted texts
        extracted_texts.clear()

    # Get bill details from the database
    bill_details = get_bill_details()

    if bill_details:
        # Create a DataFrame for bill details
        bill_df = pd.DataFrame(bill_details, columns=["ID", "Image", "Amount"])

        # Calculate and display the total value of all bills
        total_value = bill_df["Amount"].sum()
        st.write(f"Total value of all bills: {format_currency(total_value)}")

        # Rename the ID column to "Bill Number" and display the bill details in a table
        bill_df.rename(columns={"ID": "Bill Number"}, inplace=True)
        bill_df["Bill Number"] = bill_df.index + 1
        st.table(bill_df[["Bill Number", "Amount"]])

    else:
        st.write("No bill details found in the uploaded images.")

if __name__ == "__main__":
    main()
