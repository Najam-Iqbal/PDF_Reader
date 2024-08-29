document.getElementById('pdf-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const pdfViewer = document.getElementById('pdf-viewer');
            pdfViewer.innerHTML = '';
            if (data.texts) {
                data.texts.forEach((text, index) => {
                    const div = document.createElement('div');
                    div.className = 'pdf-page';
                    div.innerHTML = `<h2>Page ${index + 1}</h2><pre>${text}</pre>`;
                    pdfViewer.appendChild(div);
                });
            } else {
                alert(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please upload a valid PDF file.');
    }
});
