// DOM elements to modify
// regarding Save click
const saveButton = document.getElementById('save-button');
const savedIcon = document.getElementById('saved-icon');
const iAppliedButton = document.getElementById('i-applied-button');

// Regarding show job details
const detailsWrapper = document.getElementById('details-wrapper');
const jobTitle = document.getElementById('details-job-title');
const url = document.getElementById('details-url');
const companyName = document.getElementById('details-company-name');
const jobLocation = document.getElementById('details-location');
const datePosted = document.getElementById('details-date-posted');
const description = document.getElementById('details-description');

// Variable to store job details to avoid second API request when saving
// variable populated in getJobDetails()
let cachedJobDetails;

// Other variables
const cosId = detailsWrapper.dataset.cosId;
const fc = detailsWrapper.dataset.fc;

saveButton.addEventListener('click', saveButtonClick);
if (iAppliedButton) {
  iAppliedButton.addEventListener('click', iAppliedButtonClick);
}

async function showJobDetails() {
  const jobDetails = await getJobDetails(cosId);
  updateDom(jobDetails);
  detailsWrapper.classList.remove('display-none');
}

async function getJobDetails() {
  // called by showJobDetails
  const resp = await fetch(`/cos-jobs/details/${cosId}/json`);
  const jobDetails = await resp.json();
  cachedJobDetails = jobDetails;
  return jobDetails;
}

function updateDom(jobDetails) {
  // called by showJobDetails
  jobTitle.textContent = jobDetails.JobTitle;
  url.setAttribute('href', jobDetails.URL);
  companyName.textContent = jobDetails.Company;
  jobLocation.textContent = jobDetails.Location;
  datePosted.textContent = `Date Posted: ${jobDetails.DatePosted}`;
  description.innerHTML = jobDetails.Description;
}

async function saveButtonClick() {
  details = getDetailsFromCached();
  const resp = await saveJob(details);
  const savedJobId = await resp.json();
  if (resp.status === 200) {
    saveButton.classList.toggle('display-none');
    savedIcon.classList.toggle('display-none');
  }
  // ************************ADD ERROR HANDLING***********************************
  return savedJobId;
}

function getDetailsFromCached() {
  // called by saveButtonClick
  return {
    company: cachedJobDetails.Company,
    title: cachedJobDetails.JobTitle,
    date_posted: cachedJobDetails.DatePosted,
    location: cachedJobDetails.Location,
    job_description: cachedJobDetails.Description,
    application_link: cachedJobDetails.URL,
    cos_id: cosId,
    federal_contractor: fc
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

async function iAppliedButtonClick() {
  const savedJobId = await saveButtonClick();
  window.location.href = `/job-apps/add/${savedJobId}`;
}

// On load:
showJobDetails();