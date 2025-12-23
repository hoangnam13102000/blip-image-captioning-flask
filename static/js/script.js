const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');
const errorDiv = document.getElementById('error');
const successDiv = document.getElementById('success');
const imagePreview = document.getElementById('imagePreview');
const captionBox = document.getElementById('caption');

// Drag and drop handlers
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        uploadImage();
    }
});

uploadBox.addEventListener('click', selectFile);

function selectFile() {
    fileInput.click();
}

fileInput.addEventListener('change', uploadImage);

function uploadImage() {
    const file = fileInput.files[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, GIF, or BMP.');
        return;
    }

    // Show loading state
    loading.classList.add('show');
    resultSection.classList.remove('show');
    hideError();

    // Create form data
    const formData = new FormData();
    formData.append('file', file);

    // Send to server
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.remove('show');
        
        if (data.success) {
            imagePreview.innerHTML = `<img src="${data.image}" alt="Uploaded image">`;
            captionBox.textContent = data.caption;
            resultSection.classList.add('show');
            hideError();
        } else {
            showError(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        loading.classList.remove('show');
        showError('Error: ' + error.message);
    });
}

function clearAll() {
    fileInput.value = '';
    resultSection.classList.remove('show');
    loading.classList.remove('show');
    hideError();
    imagePreview.innerHTML = '';
    captionBox.textContent = '';
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

function hideError() {
    errorDiv.classList.remove('show');
}