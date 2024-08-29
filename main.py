import PySimpleGUI as sg
import fitz  # PyMuPDF
from PIL import Image
import io
import base64

def get_image_base64(image_bytes):
    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def display_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    
    layout = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        html_content = page.get_text("html")

        # Extract images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert image bytes to Base64
            img_url = get_image_base64(image_bytes)
            
            # Replace image placeholders in the HTML with actual image URLs
            img_placeholder = f'data:image/jpeg;base64,{base_image["image"].decode("utf-8")}'
            html_content = html_content.replace(img_placeholder, img_url)

        # Display HTML content as a part of the GUI layout
        layout.append([sg.Text(f"Page {page_num + 1}", font='Any 15')])
        layout.append([sg.Text(html_content, size=(80, 20))])

    doc.close()

    # Create the PySimpleGUI window
    window = sg.Window("Interactive PDF Reader", layout)

    # Event loop for window interaction
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    window.close()

def main():
    layout = [
        [sg.Text("Upload your PDF file")],
        [sg.Input(), sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
        [sg.Button("Load PDF")]
    ]
    
    window = sg.Window("PDF Reader", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Load PDF":
            pdf_path = values[0]
            if pdf_path:
                display_pdf_content(pdf_path)

    window.close()

if __name__ == "__main__":
    main()
