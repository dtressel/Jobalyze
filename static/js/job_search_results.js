// DOM objects right side
const jobTitle = document.getElementById('details-job-title');
const url = document.getElementById('details-url');
const companyName =document.getElementById('details-company-name');
const jobLocation = document.getElementById('details-location');
const datePosted = document.getElementById('details-date-posted');
const description = document.getElementById('details-description');

// DOM objects left side
const leftColumnList = document.getElementById('left-column-list');
const jobCards = document.getElementsByClassName('api-job-list-item');

// Save job details when accessed to object so that when re-acccessed
// it doesn't haven't to make a duplicate API request.
const savedJobDetails = {};
// Other variables:
let currentHighlightedCard = 0;

leftColumnList.addEventListener('click', jobListClick);

function jobListClick(evt) {
  console.log('in jobListClick');
  console.log(evt);
  if (evt.target.classList[0] === 'api-job-list-item') {
    console.log('in jobListClick if statement');
    const jobId = evt.target.dataset.jobId;
    const DomId = evt.target.id;
    highlightCard(DomId);
    showJobDetails(jobId, DomId);
  }
}

function highlightCard(DomId) {
  console.log('in highlightCard');
  jobCards[currentHighlightedCard].classList.remove('highlight-card');
  jobCards[DomId].classList.add('highlight-card');
  currentHighlightedCard = DomId;
}

async function showJobDetails(jobId, DomId) {
  console.log('in ShowJobDetails');
  const jobDetails = await getJobDetails(jobId, DomId);
  console.log(jobDetails);
}

async function getJobDetails(jobId, DomId) {
  console.log('in getJobDetails');
  if (DomId in savedJobDetails) {
    return savedJobDetails[DomId];
  }
  const resp = await fetch(`/jobs/details/${jobId}/json`);
  const json = await resp.json();
  savedJobDetails[DomId] = json;
  return json;
}