document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const submitButton = form.querySelector("button");
    const fileInput = form.querySelector("input[type='file']");
    const uploadingMessage = document.createElement("div");
    const progressBar = document.createElement("progress");
    const fileNameDisplay = document.createElement("div");

    // Create elements for feedback
    uploadingMessage.id = "uploading-message";
    uploadingMessage.textContent = "Загрузка файла...";
    uploadingMessage.style.display = "none";

    progressBar.id = "upload-progress";
    progressBar.value = 0;
    progressBar.max = 100;
    progressBar.style.display = "none";

    fileNameDisplay.id = "file-name-display";
    fileNameDisplay.style.marginTop = "10px";
    fileNameDisplay.style.fontSize = "0.9em";
    fileNameDisplay.style.color = "#666";

    // Append elements to the form
    form.appendChild(uploadingMessage);
    form.appendChild(progressBar);
    form.appendChild(fileNameDisplay);

    // Display the selected file name
    fileInput.addEventListener("change", function() {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Выбран файл: ${fileInput.files[0].name}`;
        } else {
            fileNameDisplay.textContent = "";
        }
    });

    // Handle form submission
    form.addEventListener("submit", function(event) {
        if (fileInput.files.length === 0) {
            alert("Пожалуйста, выберите файл для загрузки.");
            event.preventDefault();
            return;
        }

        // Show uploading message and progress bar
        uploadingMessage.style.display = "block";
        progressBar.style.display = "block";
        submitButton.disabled = true;
        submitButton.textContent = "Загрузка...";

        // Simulate file upload progress
        let progress = 0;
        const interval = setInterval(() => {
            if (progress >= 100) {
                clearInterval(interval);
                submitButton.textContent = "Перевести"; // Reset button text
                submitButton.disabled = false; // Re-enable the button
            } else {
                progress += 5;
                progressBar.value = progress;
            }
        }, 100);
    });

    // Handle download link click
    const downloadLink = document.querySelector(".result-link");
    if (downloadLink) {
        downloadLink.addEventListener("click", function(event) {
            event.preventDefault();
            const userConfirmed = confirm("Вы уверены, что хотите скачать переведённый PDF?");
            if (userConfirmed) {
                window.location.href = downloadLink.href;
            }
        });
    }
});
