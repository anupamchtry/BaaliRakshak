// script.js
// Handle the drag & drop events
const dropArea = document.getElementById("drag-drop");
dropArea.addEventListener("click", () =>
  document.getElementById("fileInput").click()
);

dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.backgroundColor = "#ecf4f9";
});

dropArea.addEventListener(
  "dragleave",
  () => (dropArea.style.backgroundColor = "#f9f9f9")
);

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  document.getElementById("fileInput").files = e.dataTransfer.files;
  previewImage();
});

// Function to show image preview
function previewImage() {
  const file = document.getElementById("fileInput").files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const image = new Image();
      image.src = event.target.result;
      image.onload = function () {
        document.getElementById("resultImage").src = event.target.result;
        document.getElementById("uploadedImage").style.display = "block";
        document.getElementById("predictButton").style.display = "inline-block"; // Show the Predict button
      };
    };
    reader.readAsDataURL(file);
  }
}

// Submit form for prediction
function submitForm() {
  const form = new FormData();
  form.append("file", document.getElementById("fileInput").files[0]);

  fetch("/predict", {
    method: "POST",
    body: form,
  })
    .then((response) => response.text())
    .then((data) => {
      const parser = new DOMParser();
      const htmlDoc = parser.parseFromString(data, "text/html");

      // Update prediction details
      const predictedLabel =
        htmlDoc.querySelector("#predictedLabel").textContent;
      const confidence = htmlDoc.querySelector("#confidence").textContent;
      document.getElementById(
        "diseaseResult"
      ).textContent = `Disease: ${predictedLabel}`;
      document.getElementById(
        "confidenceResult"
      ).textContent = `Confidence: ${confidence}%`;
      document.getElementById("predictionDetails").style.display = "block";
    })
    .catch((err) => console.error(err));
}
