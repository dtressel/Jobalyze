const newJobHuntButton = document.getElementById('new-job-hunt-button');
const jobHuntSelect = document.getElementById('job-hunt-select');
const expandJobSearchIcon = document.getElementById('expand-job-search-icon');
const apiSearchExpandForm = document.getElementById('api-search-expand-form');

newJobHuntButton.addEventListener('click', newJobHuntClick);
if (expandJobSearchIcon) {
  expandJobSearchIcon.addEventListener('click', () => apiSearchExpandForm.submit());
}
jobHuntSelect.addEventListener('change', jobHuntSelectChange);

function jobHuntSelectChange() {
  window.location.href = `/dashboard/${jobHuntSelect.value}`;
}