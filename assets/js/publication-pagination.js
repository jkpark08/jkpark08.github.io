document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById("publication-list");
  const pagination = document.getElementById("publication-pagination");
  const pageStatus = document.getElementById("publication-page-status");

  if (!list || !pagination) return;

  const cards = Array.from(
    list.querySelectorAll(".publication-card")
  );

  const pageSize = Number(list.dataset.pageSize || 5);
  const totalPages = Math.ceil(cards.length / pageSize);

  if (totalPages <= 1) {
    pagination.hidden = true;
    return;
  }

  function renderPage(page) {
    const currentPage = Math.max(1, Math.min(page, totalPages));
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const visibleEnd = Math.min(end, cards.length);

    if (pageStatus) {
      pageStatus.textContent =
        `Showing ${start + 1}–${visibleEnd} of ${cards.length} · Page ${currentPage} of ${totalPages}`;
    }
    
    cards.forEach((card, index) => {
      card.hidden = index < start || index >= end;
    });

    pagination.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
      const button = document.createElement("button");

      button.type = "button";
      button.className = "publication-pagination__button";
      button.textContent = i;

      if (i === currentPage) {
        button.classList.add("is-active");
        button.setAttribute("aria-current", "page");
      }

      button.addEventListener("click", () => {
        renderPage(i);

        list.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      });

      pagination.appendChild(button);
    }
  }

  renderPage(1);
});
