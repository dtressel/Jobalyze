const newJobHuntButton = document.getElementById('new-job-hunt-button');
const jobHuntSelect = document.getElementById('job-hunt-select');

newJobHuntButton.addEventListener('click', newJobHuntClick);

jobHuntSelect.addEventListener('change', jobHuntSelectChange);

function jobHuntSelectChange() {
  window.location.href = `/dashboard/${jobHuntSelect.value}`;
}