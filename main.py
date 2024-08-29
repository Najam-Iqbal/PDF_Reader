import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import base64  # Import base64 for encoding image data

# Function to display PDF content with selectable text and images
def display_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text and HTML structure
        html_content = page.get_text("html")
        
        # Extract and render images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img = Image.open(io.BytesIO(image_bytes))
            
            # Use an in-memory buffer instead of saving to disk
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_data = buf.getvalue()
            
            # Generate an image URL for the in-memory image
            img_url = f"data:image/png;base64,{base64.b64encode(img_data).decode()}"
            
            # Replace image placeholders in the HTML with actual image URLs
            html_content = html_content.replace(f'src="data:image/jpeg;base64,{base_image["image"].decode()}"', f'src="{img_url}"')
        
        # Display the HTML content
        st.components.v1.html(html_content, height=800, scrolling=True)

    doc.close()

# Streamlit app
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
