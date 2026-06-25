$("form").on("change", ".file-upload-field", function () {
  $(this)
    .parent(".file-upload-wrapper")
    .attr(
      "data-text",
      $(this)
        .val()
        .replace(/.*(\/|\\)/, "")
    );
});

document.getElementById("know-more-btn").addEventListener("click", function () {
  var diseaseInfo = document.getElementById("disease-info");

  if (diseaseInfo.classList.contains("hidden")) {
    // Show the details with the fade-in animation
    diseaseInfo.classList.remove("hidden");
    diseaseInfo.classList.add("expanded", "fade-in");
    this.textContent = "Hide Details";
  } else {
    // Hide the details with the fade-out animation
    diseaseInfo.classList.remove("expanded", "fade-in");
    diseaseInfo.classList.add("fade-out");
    this.textContent = "Know More";

    // Wait for the fade-out animation to finish, then hide the details
    setTimeout(() => {
      diseaseInfo.classList.remove("fade-out");
      diseaseInfo.classList.add("hidden");
    }, 400); // The delay duration should match the fade-out animation duration
  }
});
