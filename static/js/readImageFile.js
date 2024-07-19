
readImageFile()
function readImageFile() {
    const imageContainer = document.getElementById('imageContainer');
  
    // 使用 fetch API 讀取資料夾內容
    fetch('/get_control_pose')
      .then(response => response.json())
      .then(data => {

          let rowDiv = null;
          let columnCount = 0;

          data.forEach(path => {

            if (columnCount === 0) {
              rowDiv = document.createElement('div');
              rowDiv.classList.add('row');
              imageContainer.appendChild(rowDiv);
            }
   
            // 創建一個新的 img 元素並設置 src 屬性
            const img = document.createElement('img');
            img.src = "data:image/png;base64,"+path["base64"];
            img.style.maxWidth = '200px';
            img.classList.add('col-3', 'my-2');
            rowDiv.appendChild(img);
  
            columnCount = (columnCount + 1) % 4;
          });

      })
      .catch(error => {
        console.error('Error reading folder:', error);
        imageContainer.textContent = '讀取資料夾時發生錯誤';
      });
  }