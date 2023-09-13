# AI Bill Assistant - Technical Documentation

The "AI Bill Assistant" is a Python application designed to provide advanced bill management capabilities using Streamlit. This technical documentation provides a detailed overview of the application's architecture, functionality, and features, catering to technical audiences.

## Features

### 1. OCR Text Extraction

- **Text Extraction Engine**: The application leverages Tesseract OCR (Optical Character Recognition) for robust text extraction from bill images.

- **Highest Total Detection**: It intelligently identifies the highest total value within the extracted text, typically representing the total amount on a bill.

### 2. SQLite Database Integration

- **Database Creation**: The application dynamically creates an SQLite database table to store bill details if it doesn't exist, ensuring data persistence.

- **Data Insertion**: Bill details, including the bill's name, date, comment, image (as a BLOB), and the calculated amount, are efficiently inserted into the database.

- **Data Retrieval**: Users can effortlessly retrieve bill details from the database, enabling easy access to historical billing information.

### 3. Streamlit User Interface

- **User-Friendly Interface**: The Streamlit-based interface simplifies user interactions, allowing users to input bill details seamlessly.

- **Form Input**: Users can conveniently provide bill-specific information, including the bill's name, date, a descriptive comment, and even upload an image of the bill directly through the user interface.

- **Interactive Bill Management**: Users can view their bill history, including the ID, name, date, comment, and amount, in a tabular format. An option to clear all bill details is also provided.

## Prerequisites

Before running the application, ensure the following dependencies are installed:

- `streamlit`: The primary framework for building the user interface.
- `pytesseract`: The OCR engine used for text extraction.
- `Pillow` (PIL): A Python Imaging Library for image processing.
- `re`: The Python regular expressions library.
- `pandas`: For handling and displaying bill details.
- `sqlite3`: The standard library for SQLite database integration.
- `base64`: Required for binary data handling.

You can install these dependencies using `pip`:

```bash
pip install streamlit pytesseract Pillow pandas
```

### Tesseract OCR

The application relies on the Tesseract OCR engine for text extraction from images. It's imperative to have Tesseract installed on your system. You can obtain it from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract) or install it using a package manager.

## Application Architecture

The AI Bill Assistant is organized into a series of functions, each contributing to a specific aspect of the application. Here's a breakdown of these functions and their roles:

### Text Extraction (`find_highest_total_value`)

- This function utilizes Tesseract OCR to extract text from bill images.
- It employs regular expressions to identify and extract the highest total value from the extracted text, commonly representing the bill's total amount.

### Database Management (`create_table`, `insert_bill_details`, `get_bill_details`, `delete_all_bill_details`)

- `create_table`: Dynamically generates an SQLite database table for storing bill details, ensuring data persistence and organization.
- `insert_bill_details`: Inserts bill details, including the bill's name, date, comment, image (as a binary large object, or BLOB), and the calculated amount, into the database.
- `get_bill_details`: Facilitates seamless retrieval of bill details from the database, enabling users to access historical billing information.
- `delete_all_bill_details`: Provides a functionality to clear all bill details from the database.

### Main Function (`main`)

- Serving as the application's entry point, the `main` function orchestrates the Streamlit-based user interface and application logic.
- It constructs a user-friendly interface, allowing users to input bill details via a form.
- Upon submission, the following steps are performed:
  1. Conversion of the uploaded image into a PIL image object.
  2. Extraction of text from the image using Tesseract OCR.
  3. Identification of the highest total value within the extracted text.
  4. Preservation of the uploaded image as a binary large object (BLOB) in the database.
  5. Insertion of the complete bill details, including the bill's name, date, comment, image BLOB, and amount, into the database.

- The application proceeds to retrieve bill details from the database, calculate the total value of all bills, and present the bill details in a tabular format.
- Users have the option to clear all bill details from the database via a "Clear All" button.

## Running the Application

To execute the AI Bill Assistant, execute the following command in your terminal:

```bash
streamlit run app.py
```

This command launches the Streamlit app in your default web browser, providing an interactive environment for managing bill details.

## Customization and Extension

The application is highly modular and can be extended to include additional features or improved user interfaces. Consider enhancing error handling, introducing user authentication, or integrating external APIs to augment functionality.

## Note

This application is intended for

 educational purposes and serves as a proof-of-concept. It can be further extended for comprehensive bill management and OCR capabilities. When using external libraries and APIs such as Tesseract OCR and Streamlit, be sure to adhere to relevant terms of service or usage guidelines.
