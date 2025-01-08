document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) {
        alert("Please select an image to upload.");
        return;
    }
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8001/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result); 
        document.getElementById("result").style.display = "block";
        document.getElementById("class").textContent = `Class: ${result.class}`;
        document.getElementById("confidence").textContent = `Confidence: ${(result.confidence * 100).toFixed(2)}%`;
    } catch (error) {
        console.error("Error during prediction:", error);
        alert("Error during prediction: " + error.message);
    }
});
