/**
 * Form handling functionality
 * Handles AJAX submissions for add, delete, and filter operations
 */

/**
 * Attach delete handlers to all delete forms
 * Handles song deletion via AJAX
 */
function attachDeleteHandlers() {
  document
    .querySelectorAll(".delete-form, #library-output form[method='POST']")
    .forEach((form) => {
      // Remove existing listeners by cloning
      const newForm = form.cloneNode(true);
      form.parentNode.replaceChild(newForm, form);

      newForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const button = this.querySelector("button");
        const originalText = button.textContent;

        button.textContent = "...";
        button.disabled = true;

        try {
          const response = await fetch("/api/delete-song", {
            method: "POST",
            body: formData,
          });

          const data = await response.json();

          if (data.success) {
            updateLibraryTable(data.library);
            // Update the mood filter dropdown
            if (data.availableMoods) {
              updateMoodFilter(data.availableMoods);
            }
          } else {
            alert(data.error || "Failed to delete song");
            button.textContent = originalText;
            button.disabled = false;
          }
        } catch (error) {
          console.error("Error:", error);
          alert("An error occurred while deleting the song");
          button.textContent = originalText;
          button.disabled = false;
        }
      });
    });
}

/**
 * Initialize the add song form with AJAX submission
 */
function initAddSongForm() {
  const form = document.getElementById("song-form");
  const checkmark = document.getElementById("checkmark");

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const submitBtn = document.getElementById("submit-insertion");
      const originalValue = submitBtn.value;

      submitBtn.value = "Adding...";
      submitBtn.disabled = true;

      try {
        const response = await fetch("/api/add-song", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          // Update the library table
          updateLibraryTable(data.library);

          // Update the mood filter dropdown
          if (data.availableMoods) {
            updateMoodFilter(data.availableMoods);
          }

          // Show checkmark
          if (checkmark) {
            checkmark.classList.add("visible");
            setTimeout(() => {
              checkmark.classList.remove("visible");
            }, 1500);
          }

          // Clear the form
          form.reset();
        } else {
          alert(data.error || "Failed to add song");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while adding the song");
      } finally {
        submitBtn.value = originalValue;
        submitBtn.disabled = false;
      }
    });
  }
}

/**
 * Initialize the mood filter form with AJAX submission
 */
function initMoodFilterForm() {
  const filterForm = document.getElementById("mood-filter-form");

  if (filterForm) {
    filterForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const selectedMoods = Array.from(
        document.getElementById("mood_select").selectedOptions
      ).map((opt) => opt.value);

      const params = new URLSearchParams();
      selectedMoods.forEach((mood) => params.append("filter_moods", mood));

      const filterBtn = document.getElementById("filter-apply");
      const originalText = filterBtn.textContent;
      filterBtn.textContent = "Filtering...";
      filterBtn.disabled = true;

      try {
        const response = await fetch(`/api/filter-songs?${params.toString()}`);
        const data = await response.json();

        if (data.success) {
          updateLibraryTable(data.library);
        } else {
          alert(data.error || "Failed to filter songs");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while filtering");
      } finally {
        filterBtn.textContent = originalText;
        filterBtn.disabled = false;
      }
    });
  }
}

/**
 * Initialize all form handlers
 */
function initAllForms() {
  initAddSongForm();
  initMoodFilterForm();
  attachDeleteHandlers();
}
