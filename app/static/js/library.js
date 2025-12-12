/**
 * Library display functionality
 * Handles updating the library table and mood filter dropdown
 */

/**
 * Update the mood filter dropdown with available moods
 * @param {string[]} availableMoods - Array of mood strings
 * @param {string[]} selectedMoods - Array of currently selected moods
 */
function updateMoodFilter(availableMoods, selectedMoods = []) {
  const moodSelect = document.getElementById("mood_select");
  if (!moodSelect) return;

  moodSelect.innerHTML = availableMoods
    .map(
      (mood) =>
        `<option value="${mood}" ${
          selectedMoods.includes(mood) ? "selected" : ""
        }>${mood}</option>`
    )
    .join("");
}

/**
 * Update the library table with new song data
 * @param {Object[]} libraryData - Array of song objects with num, title, artist, mood, id
 */
function updateLibraryTable(libraryData) {
  const tbody = document.querySelector("#library-output table tbody");
  if (!tbody) return;

  tbody.innerHTML = libraryData
    .map(
      (song) => `
    <tr>
      <td>${song.num}</td>
      <td>${song.title}</td>
      <td>${song.artist}</td>
      <td>${song.mood}</td>
      <td>
        <form method="POST" class="delete-form" data-id="${song.id}">
          <input type="hidden" name="id-to-delete" value="${song.id}" />
          <button type="submit">Delete</button>
        </form>
      </td>
    </tr>
  `
    )
    .join("");

  // Re-attach delete handlers to new forms
  attachDeleteHandlers();
}
