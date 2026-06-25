document.addEventListener("DOMContentLoaded", () => {
  const explorer = document.getElementById("style-explorer");

  if (!explorer) return;

  const imageBase = "/assets/projects/ebh/style_grid/";

  const resultImage = explorer.querySelector("#style-result-image");
  const selectionText = explorer.querySelector("#style-selection-text");

  const backgroundButtons = explorer.querySelectorAll("[data-background]");
  const foregroundButtons = explorer.querySelectorAll("[data-foreground]");

  let selectedBackground = 1;
  let selectedForeground = 1;

  function updateResult() {
    const filename =
      `bg${selectedBackground}_fg${selectedForeground}.png`;

    resultImage.src = imageBase + filename;

    resultImage.alt =
      `Generated result with Background ${selectedBackground} and Foreground ${selectedForeground}`;

    selectionText.textContent =
      `Background ${selectedBackground} × Foreground ${selectedForeground}`;
  }

  backgroundButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedBackground = Number(button.dataset.background);

      backgroundButtons.forEach((item) => {
        item.classList.toggle("is-active", item === button);
      });

      updateResult();
    });
  });

  foregroundButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedForeground = Number(button.dataset.foreground);

      foregroundButtons.forEach((item) => {
        item.classList.toggle("is-active", item === button);
      });

      updateResult();
    });
  });
});
