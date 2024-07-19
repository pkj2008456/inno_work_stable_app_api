const uploadForm = document.getElementById('upload-form');

uploadForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById('update-container').innerHTML = data.update_message;
    } else {
      alert('Error uploading file.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Error uploading file.');
  }
});