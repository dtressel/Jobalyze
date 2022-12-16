// DOM objects right side
const jobTitle = document.getElementById('details-job-title');
const url = document.getElementById('details-url');
const companyName =document.getElementById('details-company-name');
const jobLocation = document.getElementById('details-location');
const datePosted = document.getElementById('details-date-posted');
const description = document.getElementById('details-description');

const rightColumn = document.getElementById('right-column');
const saveButton = document.getElementById('save-button');
const savedIcon = document.getElementById('saved-icon');
const fullScreenDetailsLink = document.getElementById('full-screen-details-link')

// DOM objects left side
const leftColumn = document.getElementById('left-column');
const jobCards = document.getElementsByClassName('api-job-list-item');

// Cache job details when accessed to object so that when re-acccessed
// it doesn't haven't to make a duplicate API request.
const cachedJobDetails = {};

// Other variables:
let currentHighlightedCard = 0;
let selectedJobSaved = false;

// Event Listeners:
leftColumn.addEventListener('click', jobListClick);
saveButton.addEventListener('click', saveButtonClick);

function jobListClick(evt) {
  console.log('in jobListClick');
  console.log(evt);
  if (evt.target.classList[0] === 'api-job-list-item') {
    console.log('in jobListClick if statement');
    const jobId = evt.target.dataset.jobId;
    const domId = evt.target.id;
    highlightCard(domId);
    showJobDetails(jobId, domId);
  }
}

function highlightCard(domId) {
  // called by jobListClick and showFirstDetails
  console.log('in highlightCard');
  jobCards[currentHighlightedCard].classList.remove('highlight-card');
  jobCards[domId].classList.add('highlight-card');
  currentHighlightedCard = domId;
}

async function showJobDetails(jobId, domId) {
  // called by jobListClick and showFirstDetails
  console.log('in ShowJobDetails');
  rightColumn.classList.add('display-none');
  const jobDetails = await getJobDetails(jobId, domId);
  console.log(jobDetails);
  updateDom(jobDetails, jobId);
  rightColumn.classList.remove('display-none');
}

async function getJobDetails(jobId, domId) {
  // called by showJobDetails
  console.log('in getJobDetails');
  if (domId in cachedJobDetails) {
    return cachedJobDetails[domId];
  }
  const resp = await fetch(`/cos-jobs/details/${jobId}/json`);
  const jobDetails = await resp.json();
  cachedJobDetails[domId] = jobDetails;
  return jobDetails;
}

function updateDom(jobDetails, jobId) {
  // called by showJobDetails
  jobTitle.textContent = jobDetails.JobTitle;
  url.setAttribute('href', jobDetails.URL);
  fullScreenDetailsLink.setAttribute('href', `/cos-jobs/details/${jobId}`)
  companyName.textContent = jobDetails.Company;
  jobLocation.textContent = jobDetails.Location;
  datePosted.textContent = `Date Posted: ${jobDetails.DatePosted}`;
  description.innerHTML = jobDetails.Description;
  // If the saved status of the newly selected job (jobDetails) does not match the saved 
  // status of the previously selected job (selectedJobSaved), then toggle DOM elements and variable:
  if (!jobDetails.saved === selectedJobSaved) {
    toggleSaved();
  }
}

function toggleSaved() {
  // called by updateDom
  saveButton.classList.toggle('display-none');
  savedIcon.classList.toggle('display-none');
  selectedJobSaved = !selectedJobSaved;
}

function showFirstDetails() {
  highlightCard(0);
  showJobDetails(jobCards[0].dataset.jobId, 0);
}

async function saveButtonClick() {
  domId = currentHighlightedCard;
  details = getDetailsFromSearch(domId);
  const resp = await saveJob(details);
  console.log(resp);
  if (resp.status === 200) {
    cachedJobDetails[domId].saved = 'true';
    toggleSaved();
  }
  // ************************ADD ERROR HANDLING***********************************
}

function getDetailsFromSearch() {
  // called by saveButtonClick
  const details = cachedJobDetails[domId];
  const jobCard = jobCards[domId];
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

// On Load:
showFirstDetails();

// ****ADD JS media query for mobile view to view job details on separate page****