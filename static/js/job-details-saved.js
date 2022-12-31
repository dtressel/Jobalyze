const additionalDetailsDiv = document.getElementById('additional-details');
const salaryMin = document.getElementById('salary-min');
const salaryMax = document.getElementById('salary-max');

const savedJobId = document.getElementById('details-wrapper').dataset.savedJobId;

additionalDetailsDiv.addEventListener('click', detailsDivClick);

function detailsDivClick(evt) {
  if (evt.target.localName === "button") {
    switch (evt.target.textContent) {
      case "Add":
        addButtonClick(evt.target);
        break;
      case "Save":
        saveButtonClick(evt.target);
        break;
      case "Cancel":
        cancelButtonClick(evt.target);
        break;
    }
  }
}

function addButtonClick(addButton) {
  addButton.classList.add('display-none');
  const detailsRowId = addButton.dataset.groupId;
  document.getElementById(`${detailsRowId}-input-group`).classList.remove('display-none');
  if (detailsRowId === "details-salary-range") {
    textInputToCurrency(document.getElementById('details-salary-range-1-input'));
    textInputToCurrency(document.getElementById('details-salary-range-2-input'));
  }
}

// ************************** add error handling and hide form when done *********************************
async function saveButtonClick(saveButton) {
  switch(saveButton.dataset.groupId) {
    case "details-company-size":
      console.log(document.getElementById('details-company-size-input').value);
      await postToServer({company_size: document.getElementById('details-company-size-input').value});
      break;
    case "details-salary-range":
      const salary_min_int = usLocaleStrToInt(document.getElementById('details-salary-range-1-input').value);
      const salary_max_int = usLocaleStrToInt(document.getElementById('details-salary-range-2-input').value);
      await postToServer({salary_min: salary_min_int, salary_max: salary_max_int});
      break;
    case "details-job-type": 
      await postToServer({job_type: document.getElementById('details-job-type-input').value});
      break;
    case "details-experience-level":
      await postToServer({experience_level: document.getElementById('details-experience-level-input').value})
      break;
    case "details-federal-contractor": 
      await postToServer({federal_contractor: document.getElementById('details-federal-contractor-input').value});
      break;
    case "details-user-notes": 
      await postToServer({user_notes: document.getElementById('details-user-notes-input').value});
      break;
  }
}

async function postToServer(dataObj) {
  const details = {saved_job_id: savedJobId, data: dataObj};
  const resp = await fetch('/saved-jobs/edit/json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(details)
  })
}

function cancelButtonClick(cancelButton) {
  const detailsRowId = cancelButton.dataset.groupId;
  if (detailsRowId === "details-salary-range") {
    document.getElementById('details-salary-range-1-input').value = '';
    document.getElementById('details-salary-range-2-input').value = '';
  } else {
    document.getElementById(`${detailsRowId}-input`).value = '';
  }
  document.getElementById(`${detailsRowId}-input-group`).classList.add('display-none');
  document.getElementById(`${detailsRowId}-add`).classList.remove('display-none');
}

function updateSalaryNums() {
  if (salaryMin.textContent !== 'None' && salaryMax.textContent !== 'None') {
    salaryMin.textContent = (+salaryMin.textContent).toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits: 0});
    salaryMax.textContent = (+salaryMax.textContent).toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits: 0});
    document.getElementById('details-salary-range-display').classList.remove('display-none');
  }
}

// On Page Load:
updateSalaryNums();