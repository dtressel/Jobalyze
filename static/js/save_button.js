const saveButton = document.getElementById('save-button');
const savedIcon = document.getElementById('saved-icon');

let selectedJobSaved = false;

saveButton.addEventListener('click', saveButtonClick);

async function saveButtonClick() {
  details = getDetailsFromSearch();
  const resp = await saveJob(details);
  console.log(resp);
  if (resp.status === 200) {
    toggleSaved();
  }
  // ************************ADD ERROR HANDLING***********************************
}

function getDetailsFromSearch() {
  // called by saveButtonClick
  const details = cachedJobDetails[currentHighlightedCard];
  const jobCard = jobCards[currentHighlightedCard];
  return {
    company: details.Company,
    title: details.JobTitle,
    date_posted: details.DatePosted,
    location: details.Location,
    job_description: details.Description,
    application_link: details.URL,
    cos_id: jobCard.dataset.jobId,
    federal_contractor: jobCard.dataset.fc
  }
}

async function saveJob(details) {
  // called by saveButtonClick
  const resp = await fetch('/saved-jobs/add/cos', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(details)
  })

  return resp
} 

function toggleSaved() {
  // called by updateDom
  saveButton.classList.toggle('display-none');
  savedIcon.classList.toggle('display-none');
  selectedJobSaved = !selectedJobSaved;
}