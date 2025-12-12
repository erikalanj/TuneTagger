const toggleSwitch = document.querySelector(
  "#lighting-mode-toggle input[type='checkbox']"
);
const headerText = document.getElementById("lighting-mode-header");
const documentLighting = document.body;

toggleSwitch.addEventListener("change", () => {
  if (toggleSwitch.checked) {
    headerText.textContent = "Light Mode";
    documentLighting.classList.add("light-mode");
  } else {
    headerText.textContent = "Dark Mode";
    documentLighting.classList.remove("light-mode");
  }
});
