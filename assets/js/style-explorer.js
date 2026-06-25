document.addEventListener("DOMContentLoaded", () => {
  const explorer = document.getElementById("style-explorer");

  if (!explorer) return;

  const imageBase = explorer.dataset.imageBase;

  const resultImage = explorer.querySelector("#style-result-image");
  const selectionText = explorer.querySelector("#style-selection-text");

  const backgroundButtons = explorer.querySelectorAll("[data-background]");
  const foregroundButtons = explorer.querySelectorAll("[data-foreground]");

  let selectedBackground = "03";
  let selectedForeground = "03";

  function getActiveIndex(buttons) {
    return [...buttons].findIndex(
      (button) => button.classList.contains("is-active")
    ) + 1;
  }

  function updateResult() {
    const filename =
      `output_${selectedBackground}_${selectedForeground}.png`;

    resultImage.src = imageBase + filename;

    const backgroundIndex = getActiveIndex(backgroundButtons);
    const foregroundIndex = getActiveIndex(foregroundButtons);

    resultImage.alt =
      `Generated result with Background ${backgroundIndex} and Foreground ${foregroundIndex}`;

    selectionText.textContent =
      `Background ${backgroundIndex} × Foreground ${foregroundIndex}`;
  }

  backgroundButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedBackground = button.dataset.background;

      backgroundButtons.forEach((item) => {
        const isActive = item === button;

        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-pressed", isActive ? "true" : "false");
      });

      updateResult();
    });
  });

  foregroundButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedForeground = button.dataset.foreground;

      foregroundButtons.forEach((item) => {
        const isActive = item === button;

        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-pressed", isActive ? "true" : "false");
      });

      updateResult();
    });
  });
});
