const newJobHuntButton = document.getElementById('new-job-hunt-button');
const jobHuntSelect = document.getElementById('job-hunt-select');
const deleteButton = document.getElementById('delete-button');

newJobHuntButton.addEventListener('click', newJobHuntClick);

jobHuntSelect.addEventListener('change', jobHuntSelectChange);

deleteButton.addEventListener('click', deleteButtonClick);

function jobHuntSelectChange() {
  window.location.replace(`/job-hunts/${jobHuntSelect.value}`);
}

function deleteButtonClick(evt) {
  const text = 'Delete this job hunt and all job application reports associated with it?';
  if (confirm(text)) {
    evt.target.parentElement.submit();
  }
}