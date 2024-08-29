import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import base64  # Import base64 for encoding image data

def display_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text and HTML structure
        html_content = page.get_text("html")
        
        # Extract images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert image bytes to Base64
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Generate an image URL for the Base64 image data
            img_url = f"data:image/png;base64,{img_base64}"
            
            # Replace image placeholders in the HTML with actual image URLs
            # Adjust the placeholder to match actual format used in your HTML
            img_placeholder = f'data:image/jpeg;base64,{base_image["image"].decode("utf-8")}'
            html_content = html_content.replace(img_placeholder, img_url)
        
        # Display the HTML content
        st.components.v1.html(html_content, height=800, scrolling=True)

    doc.close()

def main():
    st.title("Interactive PDF Reader")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("PDF uploaded successfully!")
        st.write("Rendering PDF...")

        # Display the PDF content
        display_pdf_content(pdf_path)

if __name__ == "__main__":
    main()
