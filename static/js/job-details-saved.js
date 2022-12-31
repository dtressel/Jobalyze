const additionalDetailsDiv = document.getElementById('additional-details');
const salaryMin = document.getElementById('details-salary-min-value-display');
const salaryMax = document.getElementById('details-salary-max-value-display');

const companySizeTranslator = [null, '1-10 employees', '11-50 employees', '51-200 employees', '201-500 employees',
  '501-1,000 employees', '1,001-5,000 employees', '5,001-10,000 employees', '10,001+ employees'];
const jobTypeTranslator = {f: 'Full-time', p: 'Part-time', c: 'Contract', i: 'Internship', v: 'Volunteer'};
const federalContractorTranslator = {True: 'Yes', False: 'No'};
const experienceLevelTransloator = {i: 'Internship', e: 'Entry level', a: 'Associate',
  m: 'Mid-Senior level', d: 'Director', x: 'Executive'}

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
  let resp;
  const detailsRowId = saveButton.dataset.groupId;
  switch(detailsRowId) {
    case "details-company-size":
      resp = await postToServer({company_size: document.getElementById('details-company-size-input').value});
      if (resp.status === 200) {
        const csValue = companySizeTranslator[document.getElementById('details-company-size-input').value];
        document.getElementById('details-company-size-value-display').textContent = csValue;
      }
      break;
    case "details-salary-range":
      const salary_min_int = usLocaleStrToInt(document.getElementById('details-salary-range-1-input').value);
      const salary_max_int = usLocaleStrToInt(document.getElementById('details-salary-range-2-input').value);
      resp = await postToServer({salary_min: salary_min_int, salary_max: salary_max_int});
      if (resp.status === 200) {
        document.getElementById('details-salary-min-value-display').textContent = document.getElementById('details-salary-range-1-input').value;
        document.getElementById('details-salary-max-value-display').textContent = document.getElementById('details-salary-range-2-input').value;
        document.getElementById('details-salary-range-display').classList.remove('display-none');
      }
      break;
    case "details-job-type": 
      resp = await postToServer({job_type: document.getElementById('details-job-type-input').value});
      if (resp.status === 200) {
        const jtValue = jobTypeTranslator[document.getElementById('details-job-type-input').value];
        document.getElementById('details-job-type-value-display').textContent = jtValue;
      }
      break;
    case "details-experience-level":
      resp = await postToServer({experience_level: document.getElementById('details-experience-level-input').value});
      if (resp.status === 200) {
        const elValue = experienceLevelTransloator[document.getElementById('details-experience-level-input').value];
        document.getElementById('details-experience-level-value-display').textContent = elValue;
      }
      break;
    case "details-federal-contractor": 
      resp = await postToServer({federal_contractor: document.getElementById('details-federal-contractor-input').value});
      if (resp.status === 200) {
        const fcValue = federalContractorTranslator[document.getElementById('details-federal-contractor-input').value];
        document.getElementById('details-federal-contractor-value-display').textContent = fcValue;
      }
      break;
    case "details-user-notes": 
      resp = await postToServer({user_notes: document.getElementById('details-user-notes-input').value});
      if (resp.status === 200) {
        document.getElementById('details-user-notes-value-display').textContent = document.getElementById('details-user-notes-input').value;
      }
      break;
  }
  document.getElementById(`${detailsRowId}-input-group`).classList.add('display-none');
  if (resp.status !== 200) {
    document.getElementById(`${detailsRowId}-add`).classList.remove('display-none');
    alert(resp.body.message);
  } 
}

async function postToServer(dataObj) {
  const details = {saved_job_id: savedJobId, data: dataObj};
  const resp = await fetch('/saved-jobs/edit/json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(details)
  })

  return resp;
}

function cancelButtonClick(cancelButton) {
  const detailsRowId = cancelButton.dataset.groupId;
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