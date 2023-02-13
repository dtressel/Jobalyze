const deleteButton = document.getElementById('delete-button');

deleteButton.addEventListener('click', deleteButtonClick);

function deleteButtonClick(evt) {
  const text = 'Delete this application report?';
  if (confirm(text)) {
    evt.target.parentElement.submit();
  }
}