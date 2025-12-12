/**
 * Collapsible section functionality
 * Handles expand/collapse animations for accordion-style sections
 */

function toggleCollapsible(contentDiv, arrowElement = null) {
  if (!contentDiv) return;

  const isActive = contentDiv.classList.contains("active");
  contentDiv.style.transition =
    "max-height 0.5s ease, opacity 0.5s ease, padding 0.5s ease";

  if (!isActive) {
    expandElement(contentDiv, arrowElement);
  } else {
    collapseElement(contentDiv, arrowElement);
  }
}

function expandElement(element, arrowElement) {
  element.style.maxHeight = "";
  const naturalHeight = element.scrollHeight;
  element.style.maxHeight = "0px";
  element.style.opacity = "0";
  element.style.paddingTop = "0";
  element.style.paddingBottom = "0";
  element.offsetHeight;
  element.classList.add("active");
  element.style.maxHeight = naturalHeight + "px";
  element.style.opacity = "1";
  element.style.paddingTop = "20px";
  element.style.paddingBottom = "20px";
  if (arrowElement) arrowElement.textContent = "▲";
  const newHandler = function handler() {
    if (element.classList.contains("active")) {
      element.style.maxHeight = "none";
    }
    element.removeEventListener("transitionend", handler);
    delete element.dataset.transitionEndHandler;
  };
  element.addEventListener("transitionend", newHandler);
  element.dataset.transitionEndHandler = newHandler;
}

function collapseElement(element, arrowElement) {
  element.style.maxHeight = element.scrollHeight + "px";
  element.offsetHeight;
  element.classList.remove("active");
  element.style.maxHeight = "0px";
  element.style.opacity = "0";
  element.style.paddingTop = "0";
  element.style.paddingBottom = "0";
  if (arrowElement) arrowElement.textContent = "▼";
}

/**
 * Initialize collapsible section click handlers
 */
function initCollapsibleSections() {
  const headers = document.querySelectorAll(".section h4");
  headers.forEach((header) => {
    header.addEventListener("click", () => {
      const section = header.closest(".section");
      const content = section.querySelector(".content");
      const arrow = header.querySelector(".arrow");
      if (section.querySelector("#library-output")) {
        const wasOpen = content.classList.contains("active");
        toggleCollapsible(content, arrow);
        if (wasOpen) {
          sessionStorage.setItem("openLibrary", "0");
        } else {
          sessionStorage.setItem("openLibrary", "1");
        }
      } else {
        toggleCollapsible(content, arrow);
      }
    });
  });
}

/**
 * Restore section states from sessionStorage
 */
function restoreSectionStates() {
  // Restore library open state
  if (sessionStorage.getItem("openLibrary") === "1") {
    const libraryContent = document.querySelectorAll(".content")[1];
    const libraryArrow = document.querySelectorAll(".section .arrow")[1];
    if (libraryContent) {
      expandElement(libraryContent, libraryArrow);
    }
  }
}
