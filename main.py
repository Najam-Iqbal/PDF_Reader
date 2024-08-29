import streamlit as st
import fitz  # PyMuPDF

# Function to display PDF
def display_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = pix.tobytes("png")
        st.image(img, caption=f'Page {page_num + 1}', use_column_width=True)
    doc.close()

# Streamlit app
def main():
    st.title("Simple PDF Reader")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.success("PDF uploaded successfully!")
        st.write("Opening PDF...")
        
        # Display the PDF
        display_pdf(pdf_path)

if __name__ == "__main__":
    main()
