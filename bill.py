import streamlit as st
import pytesseract
from PIL import Image
import re
import math
import pandas as pd

# Function to extract text from an image using pytesseract
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

# Main function to run the Streamlit app
def main():
    st.title("AI Bill Assistant")

    # Move the upload button to the sidebar
    uploaded_images = st.sidebar.file_uploader("Upload multiple images", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"], accept_multiple_files=True)

    total_bills_value = 0
    bill_details = []

    if uploaded_images:
        # List to store the extracted texts from all images
        extracted_texts = []

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
                    total_bills_value += total_value
                    bill_details.append((f"Bill {len(bill_details)+1}", format_currency(total_value)))

        # Display the bill details in a table
        if bill_details:
            st.subheader("Bill Details")
            # Create a DataFrame for bill details
            bills_df = pd.DataFrame(bill_details, columns=["Bill Title", "Amount"])

            # Display the editable table for bill details
            selected_bill = st.selectbox("Select Bill to Edit", bills_df["Bill Title"])
            new_title = st.text_input("Edit the Bill Title", selected_bill)

            if st.button("Update"):
                # Update the bill title in the DataFrame
                bills_df.loc[bills_df["Bill Title"] == selected_bill, "Bill Title"] = new_title

            st.table(bills_df)

        # Display the total value of all bills
        st.write(f"Total value of all bills: {format_currency(total_bills_value)}")

if __name__ == "__main__":
    main()
