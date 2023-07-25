import streamlit as st
import pdfplumber
import openai

# Configure OpenAI API
openai.api_key = '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'

# Streamlit app code
def main():
    st.title("PDF Chat with ChatGPT")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        # Read PDF and extract text
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        st.write("PDF successfully uploaded and processed.")
        st.write("Text content from the PDF:")
        st.write(text)

        st.subheader("Chat with ChatGPT")
        prompt = st.text_input("Enter your prompt or question")
        if prompt:
            # Generate response from ChatGPT
            response = generate_response(prompt)
            st.write("Response:")
            st.write(response)


# Generate response from ChatGPT model
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
    )
    
    return response.choices[0].text.strip()


if __name__ == '__main__':
    main()
