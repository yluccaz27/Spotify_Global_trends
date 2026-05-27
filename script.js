const codeShell = document.querySelector("#codeShell");
const codeToggle = document.querySelector("#codeToggle");

if (codeShell && codeToggle) {
  codeToggle.addEventListener("click", () => {
    const isExpanded = codeShell.classList.toggle("is-expanded");

    codeToggle.setAttribute("aria-expanded", String(isExpanded));
    codeToggle.textContent = isExpanded ? "Recolher código" : "Expandir código";

    if (isExpanded) {
      codeShell.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }
  });
}

const modal = document.querySelector("#imageModal");
const modalImage = document.querySelector("#modalImage");
const modalTitle = document.querySelector("#modalTitle");
const openButtons = document.querySelectorAll(".chart-open");
const closeButtons = document.querySelectorAll("[data-close-modal]");

function openModal(imageSrc, title, altText) {
  if (!modal || !modalImage || !modalTitle) return;

  modalImage.src = imageSrc;
  modalImage.alt = altText || title;
  modalTitle.textContent = title;

  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
}

function closeModal() {
  if (!modal || !modalImage) return;

  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");

  setTimeout(() => {
    if (!modal.classList.contains("is-open")) {
      modalImage.src = "";
      modalImage.alt = "";
    }
  }, 250);
}

openButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const imageSrc = button.dataset.image;
    const title = button.dataset.title;
    const img = button.querySelector("img");

    openModal(imageSrc, title, img?.alt);
  });
});

closeButtons.forEach((button) => {
  button.addEventListener("click", closeModal);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeModal();
  }
});
