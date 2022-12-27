additionalDetailsDiv = document.getElementById('additional-details');

additionalDetailsDiv.addEventListener('click', detailsDivClick);

function detailsDivClick(evt) {
  if (evt.target.localName === "button") {
    console.log(evt);
    switch (evt.target.textContent) {
      case "Add":
        addButtonClick(evt.target);
        break;
      case "Save":
        saveButtonClick();
        break;
      case "Cancel":
        cancelButtonClick(evt.target.parentElement.parentElement.id);
        break;
    }

  }
}

function addButtonClick(addButton) {
  addButton.classList.add('display-none');
  const detailsRowId = addButton.dataset.groupId;
  console.log(`${detailsRowId}-input-group`);
  document.getElementById(`${detailsRowId}-input-group`).classList.remove('display-none');
  switch(detailsRowId) {
    case "details-company-size": 
      addCompanySize();
      break;
    case "details-salary-range": 
      addSalaryRange();
      break;
    case "details-job-type": 
      addJobType();
      break;
    case "details-federal-contractor": 
      addFederalContractor();
      break;
    case "details-user-notes": 
      addUserNotes();
      break;
  }
}

function saveButtonClick() {

}

function cancelButtonClick(detailGroupId) {
  detailgroupDiv
}

function addCompanySize() {

}

function addSalaryRange() {
  textInputToCurrency(document.getElementById('salary-range-1-input'));
  textInputToCurrency(document.getElementById('salary-range-2-input'));
}

function addJobType() {

}

function addFederalContractor() {

}

function addUserNotes() {

}