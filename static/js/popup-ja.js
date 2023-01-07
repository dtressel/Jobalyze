const popupJa = document.getElementById('popup-ja');
const popupJaSubmitButton = document.getElementById('popup-ja-submit-button');
const popupJaCancelButton = document.getElementById('popup-ja-cancel-button');
const popupJaScreens = document.getElementsByClassName('popup-ja-screen');

const addFactorInput = document.getElementById('add-factor-input');
const addFactorButton = document.getElementById('add-factor-button');
const factorCheckboxForm = document.getElementById('factor-checkbox-form');

popupJaSubmitButton.addEventListener('click', submitButtonClick);
popupJaCancelButton.addEventListener('click', cancelButtonClick);

let popupJaWindowNum = 0;
let currentJhFactors;
  // Defined in submitJobApp()
let chosenJhId;
let savedJobId;
  // Both defined in retrieveDetails()

function submitButtonClick() {
  switch(popupJaWindowNum) {
    case 0:
      submitJobApp();
      break;
    case 1: 
      introduceFactors();
      break;
    case 2: 
      submitFactors();
      break;
    case 3:
      successMessage();
      break;
  }
}

async function submitJobApp() {
  const details = retrieveDetails();
  console.log(details);
  resp = await sendAddJobAppRequest(details);
  console.log(resp)
  if (resp.status === 200) {
    currentJhFactors = await resp.json();
    console.log(currentJhFactors);
    popupJaWindowNum++;
    iAppliedButton.classList.add('display-none');
    youAppliedIcon.classList.remove('display-none');
    hideAllScreens();
    // prepare and reveal next screen
    popupJaSubmitButton.textContent = 'Add Now';
    popupJaCancelButton.textContent = 'Add Later';
    popupJaScreens[popupJaWindowNum].classList.remove('display-none');
  } else {
    // ******************* add error handling **************************
  }
}

function retrieveDetails() {
  const jobAppReportForm = document.getElementById('job-app-report-form');
  savedJobId = jobAppReportForm.dataset.savedJobId;
  const user_id = jobAppReportForm.dataset.userId;
  const date_applied = document.getElementById('applied-date-input').value;
  chosenJhId = document.getElementById('job-hunt-select').value;
  return {id: savedJobId, user_id, date_applied, job_hunt_id: chosenJhId};
}

async function sendAddJobAppRequest(details) {
  const resp = await fetch('/job-apps/add/json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(details)
  })

  return resp
}

function introduceFactors() {
  popupJaWindowNum++;
  hideAllScreens();
  // prepare and reveal next screen
  popupJaSubmitButton.textContent = 'Submit';
  popupJaCancelButton.textContent = 'Cancel';
  populateFactorsToPopup2();
  addFactorButton.addEventListener('click', addFactorButtonClick);
  popupJaScreens[popupJaWindowNum].classList.remove('display-none');
}

function populateFactorsToPopup2() {
  for (const factor of currentJhFactors) {
    addFactorToForm(factor);
  }
}

function addFactorButtonClick() {
  const factorName = addFactorInput.value;
  if (factorName === '') {
    return;
  }
  const factorObj = {name: factorName, id: factorName, new: true};
  addFactorToForm(factorObj);
  addFactorInput.value = '';
}

function addFactorToForm(factor) {
  const checkbox = document.createElement('input');
  checkbox.setAttribute('type', 'checkbox');
  checkbox.setAttribute('value', factor.id);
  checkbox.classList.add('factor-checkbox');
  if (factor.new) {
    checkbox.classList.add('new-factor');
    checkbox.checked = true;
  } else {
    checkbox.classList.add('old-factor');
  }
  const checkboxLabel = document.createElement('label');
  checkboxLabel.textContent = factor.name;
  const containerDiv = document.createElement('div');
  containerDiv.classList.add('factor-checkbox-div');
  containerDiv.append(checkbox);
  containerDiv.append(checkboxLabel);
  factorCheckboxForm.append(containerDiv);
}

async function submitFactors() {
  const factorsToAdd = collectFactors();
  const newFactorPostResp = await postNewFactorsToFactorTable(factorsToAdd);
  if (newFactorPostResp.status !== 200) {
    alert('Attempt to add factors failed. Please try again later');
    return;
  }
  const newFactorsIdArray = await newFactorPostResp.json();
  const allFactorsIdArray = [...newFactorsIdArray, ...factorsToAdd.chosenOldFactorsIdArr];
  const associateFactorsObj = {savedJobId, allFactorsIdArray};
  await postAllFactorsToAppFactorTable(associateFactorsObj);

  // prepare and reveal next screen
  popupJaWindowNum++;
  hideAllScreens();
  popupJaSubmitButton.classList.add('display-none');
  popupJaCancelButton.textContent = 'Close';
  document.getElementById('new-job-app-link').setAttribute('href', `/job-apps/${savedJobId}`)
  popupJaScreens[popupJaWindowNum].classList.remove('display-none');
}

function collectFactors() {
  const oldFactorsCheckedInputs = document.querySelectorAll('.old-factor:checked');
  const newFactorsCheckedInputs = document.querySelectorAll('.new-factor:checked');
  const chosenOldFactorsIdArr = [...oldFactorsCheckedInputs].map((input) => input.value);
  const chosenNewFactorsObjArr = [...newFactorsCheckedInputs].map((input) => {
    return {name: input.value, job_hunt_id: chosenJhId};
  });
  return {chosenOldFactorsIdArr, chosenNewFactorsObjArr};
}

async function postNewFactorsToFactorTable(factorsToAdd) {
  const resp = await fetch('/factors/add/json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(factorsToAdd.chosenNewFactorsObjArr)
  })

  return resp
}

async function postAllFactorsToAppFactorTable(associateFactorsObj) {
  const resp = await fetch('/factors/associate/json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(associateFactorsObj)
  })

  return resp
}

function cancelButtonClick() {
  popupJa.classList.add('display-none');
}

function hideAllScreens() {
  for (const screen of popupJaScreens) {
    screen.classList.add('display-none');
  }
}





// const jobHuntSelect = document.getElementById('job-hunt-select');
// const jobHuntHiddenInput = document.getElementById('job_hunt_id');

// jobHuntSelect.addEventListener('change', jobHuntSelectChange);

// function jobHuntSelectChange() {
//   jobHuntSelect.value = jobHuntHiddenInput.value;
// }