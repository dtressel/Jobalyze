// DOM elements to modify
// regarding Save click
const saveButton = document.getElementById('save-button');
const savedIcon = document.getElementById('saved-icon');

// Regarding I applied button
const iAppliedButton = document.getElementById('i-applied-button');
const youAppliedIcon = document.getElementById('you-applied-icon');

// Regarding show job details
const detailsWrapper = document.getElementById('details-wrapper');
const jobTitle = document.getElementById('details-job-title');
const url = document.getElementById('details-url');
const companyName = document.getElementById('details-company-name');
const jobLocation = document.getElementById('details-location');
const datePosted = document.getElementById('details-date-posted');
const description = document.getElementById('details-description');

// Variable to store job details to avoid second API request when saving
// variable populated on page load in getJobDetails()
let cachedJobDetails;

// Other variables
const cosId = detailsWrapper.dataset.cosId;
const fc = detailsWrapper.dataset.fc;
let savedJobId;

if (saveButton) {
  saveButton.addEventListener('click', saveButtonClick);
}
if (iAppliedButton) {
  iAppliedButton.addEventListener('click', iAppliedButtonClick);
}


// #1: Functionality that loads job details on page load

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


// #2: Functionality that saves a job on Save Button Click
//     (also sometimes called when clicking iApplied)

async function saveButtonClick() {
  details = getDetailsFromCached();
  const resp = await saveJob(details);
  savedJobId = await resp.json();
  if (resp.status === 200) {
    saveButton.classList.toggle('display-none');
    savedIcon.classList.toggle('display-none');
  }
  // ************************ADD ERROR HANDLING***********************************
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

  return resp;
}

async function iAppliedButtonClick() {
  console.log('in iAppliedButtonClick')
  console.log('savedJobId:', iAppliedButton.dataset.savedJobId);
  console.log('jobHunt', iAppliedButton.dataset.jobHunt);
  if (iAppliedButton.dataset.savedJobId === 'none') {
    await saveButtonClick();
    console.log('savedJobId:', savedJobId);
    // backend checks (in models.py) if the job is already saved and avoids duplicate saves.
  } else {
    savedJobId = iAppliedButton.dataset.savedJobId;
  }
  if (iAppliedButton.dataset.jobHunt === 'none') {
    iAppliedToJhPopup();
  } else {
    addDetailsToJaPopup(savedJobId);
    document.getElementById('popup-ja').classList.remove('display-none');
  }
}

function addDetailsToJaPopup(savedJobId) {
  const jobTitleSpans = document.getElementsByClassName('job-title-spans');
  const companySpans = document.getElementsByClassName('company-spans');
  for (const span of jobTitleSpans) {
    span.textContent = cachedJobDetails.JobTitle;
  }
  for (const span of companySpans) {
    span.textContent = cachedJobDetails.Company;
  }
  document.getElementById('job-app-report-form').setAttribute('data-saved-job-id', savedJobId);
}

// On load:
showJobDetails();