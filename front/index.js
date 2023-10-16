import 'regenerator-runtime/runtime';
import axios from 'axios';

const progressBar = document.querySelector('#progressBar');

const alert = (message, type) => {
  const alertContainer = document.querySelector('#alertContainer');
  alertContainer.innerHTML = `
    <div class="alert alert-${type}">
      ${message}
    </div>
    `;
};

const setProgress = (percentCompleted) => {
  progressBar.style.width = percentCompleted + '%';
  progressBar.setAttribute('aria-valuenow', percentCompleted);
};
const uploadFile = (file) => {
  const apiUrl = 'http://127.0.0.1:8000/api/upload/';

  const formData = new FormData();
  // "file" is the key that our endpoint expects for the uploaded file.
  formData.append('file', file);

  // To send binary data (content of a file) we need
  // to set the Content-Type of the request header to
  // multipart/form-data.
  return axios.post(apiUrl, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      const { loaded, total } = progressEvent;
      const percentCompleted = Math.round((loaded / total) * 100);
      setProgress(percentCompleted);
    },
  });
};

const handleFileSelect = (event) => {
  const button = document.querySelector('#upload');
  button.disabled = event.target.files.length == 0;
};

const handleSubmit = async (event) => {
  event.preventDefault();

  // Show the progress bar
  setProgress(0);
  progressBar.parentElement.classList.remove('d-none');

  try {
    const fileInput = document.querySelector('#file');
    const response = await uploadFile(fileInput.files[0]);
    alert('File successfully uploaded!', 'success');
  } catch (err) {
    if (err.response) alert(err.response.data.file[0], 'danger');
    else if (err.request) alert('Could not reach the server!', 'danger');
    else alert('An unexpected error occurred!', 'danger');
  }

  // Hide the progress bar
  progressBar.parentElement.classList.add('d-none');
};

const form = document.querySelector('form');
form.addEventListener('submit', handleSubmit);


const fileInput = document.querySelector('#file');
fileInput.addEventListener('change', handleFileSelect);

const fileList = document.querySelector('#fileList');
const showFilesButton = document.querySelector('#showFiles');

let isFileListVisible = false;

const toggleFileList = () => {
  isFileListVisible = !isFileListVisible; 

  if (isFileListVisible) {
    showFilesButton.textContent = 'Hide Files';
    listFiles();
  } else {
    showFilesButton.textContent = 'See All Files';
  }

  fileList.style.display = isFileListVisible ? 'block' : 'none';
};

showFilesButton.addEventListener('click', toggleFileList);

const listFiles = async () => {
  if (!isFileListVisible) {
    return;
  }

  const apiUrl = 'http://127.0.0.1:8000/api/files/';

  try {
    const response = await axios.get(apiUrl);
    const files = response.data;

    if (files.length > 0) {
      fileList.innerHTML = '';
      files.forEach((file) => {
        const listItem = document.createElement('li');

        listItem.innerHTML = `<pre>${JSON.stringify(file, null, 2)}</pre>`;
        fileList.appendChild(listItem);
      });
    } else {
      fileList.innerHTML = 'No files available.';
    }
  } catch (err) {
    console.error(err);
    alert('An error occurred while listing files.', 'danger');
  }
};
