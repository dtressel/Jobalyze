additionalDetailsDiv = document.getElementById('additional-details');

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

async function saveButtonClick(saveButton) {
  switch(saveButton.dataset.groupId) {
    case "details-company-size":
      console.log(document.getElementById('details-company-size-input').value);
      await postToServer({company_size: document.getElementById('details-company-size-input').value});
      break;
    case "details-salary-range": 
      await postToServer({salary_min: document.getElementById('details-salary-range-1-input').value,
        salary_max: document.getElementById('details-salary-range-2-input').value});
      break;
    case "details-job-type": 
      await postToServer({job_type: document.getElementById('details-job-type-input').value});
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