// Configure PDF.js
const url = 'https://mozilla.github.io/pdf.js/build/pdf.worker.js';
pdfjsLib.GlobalWorkerOptions.workerSrc = url;

const fileInput = document.getElementById('file-input');
const pdfViewer = document.getElementById('pdf-viewer');
const pageNumSpan = document.getElementById('page-num');
const pageCountSpan = document.getElementById('page-count');
const zoomInput = document.getElementById('zoom-level');
const searchInput = document.getElementById('search-input');

let pdfDoc = null;
let currentPage = 1;
let zoomLevel = 1;

fileInput.addEventListener('change', handleFileSelect);
document.getElementById('prev-page').addEventListener('click', prevPage);
document.getElementById('next-page').addEventListener('click', nextPage);
zoomInput.addEventListener('change', handleZoomChange);
searchInput.addEventListener('input', handleSearch);

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const fileReader = new FileReader();
        fileReader.onload = function () {
            const arrayBuffer = fileReader.result;
            renderPDF(arrayBuffer);
        };
        fileReader.readAsArrayBuffer(file);
    }
}

function renderPDF(arrayBuffer) {
    pdfjsLib.getDocument({ data: arrayBuffer }).promise.then(pdf => {
        pdfDoc = pdf;
        pageCountSpan.textContent = pdf.numPages;
        renderPage(currentPage);
    }).catch(error => {
        console.error('Error rendering PDF:', error);
    });
}

function renderPage(num) {
    pdfDoc.getPage(num).then(page => {
        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-page';
        pdfViewer.innerHTML = ''; // Clear previous content
        pdfViewer.appendChild(canvas);

        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: zoomLevel });
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        page.render({
            canvasContext: context,
            viewport: viewport
        }).promise.then(() => {
            pageNumSpan.textContent = num;
            if (searchInput.value) {
                searchInPage(page);
            }
        });
    });
}

function prevPage() {
    if (pdfDoc && currentPage > 1) {
        currentPage--;
        renderPage(currentPage);
    }
}

function nextPage() {
    if (pdfDoc && currentPage < pdfDoc.numPages) {
        currentPage++;
        renderPage(currentPage);
    }
}

function handleZoomChange() {
    zoomLevel = parseFloat(zoomInput.value);
    if (pdfDoc) {
        renderPage(currentPage);
    }
}

function handleSearch() {
    if (pdfDoc && searchInput.value) {
        pdfDoc.getPage(currentPage).then(page => {
            searchInPage(page);
        });
    }
}

function searchInPage(page) {
    page.getTextContent().then(textContent => {
        const textItems = textContent.items;
        const searchText = searchInput.value.toLowerCase();
        const pageText = textItems.map(item => item.str).join(' ').toLowerCase();
        
        if (pageText.includes(searchText)) {
            // Highlight search results (basic implementation, you may need to improve this)
            // You can use a library or custom logic to highlight text within the canvas.
            console.log(`Found "${searchText}" on page ${currentPage}`);
        } else {
            console.log(`"${searchText}" not found on page ${currentPage}`);
        }
    });
}
