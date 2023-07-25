import streamlit as st
import pytesseract
from PIL import Image
import re

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
        return highest_total_value, highest_total_line_num

    # If the total value is not found, return None
    return None, None

def main():
    st.title("Bill Details and Total Amount")

    uploaded_images = st.file_uploader("Upload multiple images", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"], accept_multiple_files=True)

    total_bills_value = 0

    if uploaded_images:
        for image in uploaded_images:
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Convert the uploaded image to a PIL image object
            pil_image = Image.open(image)

            # Extract text from the image
            extracted_text = extract_text_from_image(pil_image)

            if extracted_text:
                # Find the highest total value and its line number from the extracted text
                total_value, _ = find_highest_total_value(extracted_text)

                if total_value is not None:
                    st.write(f"Total value of the bill: ${total_value:.2f}")
                    total_bills_value += total_value
                else:
                    st.write("Total value not found in the bill.")
            else:
                st.write("Text extraction from the image failed.")

    st.write(f"\nTotal value of all bills: ${total_bills_value:.2f}")

if __name__ == "__main__":
    main()
