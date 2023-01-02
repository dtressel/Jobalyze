const saveButton = document.getElementById('save-button');

saveButton.addEventListener('click', saveButtonClick);

function saveButtonClick() {
  if (document.getElementById('job_type').value === '-') {
    document.getElementById('job_type').value = null;
  }
  if (document.getElementById('experience_level').value === '-') {
    document.getElementById('experience_level').value = null;
  }
  if (document.getElementById('company_size').value === '-') {
    document.getElementById('company_size').value = null;
  }
  document.getElementById('saved-job-add-form').submit();
}