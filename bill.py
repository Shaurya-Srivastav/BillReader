import pytesseract
from PIL import Image
import re

def extract_text_from_image(image_path):
    try:
        # Load the image using PIL (Python Imaging Library)
        image = Image.open(image_path)

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)

        return extracted_text
    except Exception as e:
        print(f"Error: {e}")
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

if __name__ == "__main__":
    # Replace the list below with the actual paths to your image files
    image_paths = [
        "bill1.png",
        "bill2.png",
        "bill3.webp",
        "bill4.webp",
        # Add more image file paths if needed
    ]

    total_bills_value = 0

    for image_path in image_paths:
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)

        if extracted_text:
            # Find the highest total value and its line number from the extracted text
            total_value, _ = find_highest_total_value(extracted_text)

            if total_value is not None:
                print(f"Total value of the bill in {image_path}: ${total_value:.2f}")
                total_bills_value += total_value
            else:
                print(f"Total value not found in the bill: {image_path}")
        else:
            print(f"Text extraction from the image failed: {image_path}")

    print(f"\nTotal value of all bills: ${total_bills_value:.2f}")
