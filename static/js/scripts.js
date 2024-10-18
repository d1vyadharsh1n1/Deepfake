document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();

  let formData = new FormData();
  let fileInput = document.getElementById("videoUpload");

  if (fileInput.files.length === 0) {
    alert("Please select a video file.");
    return;
  }

  formData.append("video", fileInput.files[0]);

  document.getElementById("progressSection").classList.remove("d-none");

  let progressBar = document.getElementById("progressBar");
  let progress = 0;

  let interval = setInterval(() => {
    progress += 10;
    progressBar.style.width = progress + "%";
    progressBar.setAttribute("aria-valuenow", progress);
    progressBar.innerText = progress + "%";

    if (progress >= 100) {
      clearInterval(interval);
    }
  }, 500);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      clearInterval(interval);
      progressBar.style.width = "100%";
      progressBar.setAttribute("aria-valuenow", "100");
      progressBar.innerText = "100%";

      setTimeout(() => {
        document.getElementById("progressSection").classList.add("d-none");
      }, 500);

      document.getElementById("resultsSection").classList.remove("d-none");

      document.getElementById("fakeStatus").innerText = data.fakeStatus;
      document.getElementById("confidenceScore").innerText =
        data.confidenceScore;

      let analysisDetails = document.getElementById("analysisDetails");
      analysisDetails.innerHTML = "";
      data.analysisDetails.forEach((detail) => {
        analysisDetails.innerHTML += `<li>${detail}</li>`;
      });
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred during the analysis.");
    });
});

document.getElementById("aboutButton").addEventListener("click", function (e) {
  e.preventDefault();

  document.getElementById("uploadSection").classList.add("d-none");
  document.getElementById("progressSection").classList.add("d-none");
  document.getElementById("resultsSection").classList.add("d-none");

  document.getElementById("aboutSection").classList.remove("d-none");
});

document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();

    document.getElementById("uploadSection").classList.add("d-none");
    document.getElementById("progressSection").classList.add("d-none");
    document.getElementById("resultsSection").classList.add("d-none");
    document.getElementById("aboutSection").classList.add("d-none");

    if (this.id === "aboutButton") {
      document.getElementById("aboutSection").classList.remove("d-none");
    } else {
      // Handle other sections if needed
    }
  });
});
