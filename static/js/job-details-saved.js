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

function addButtonClick(element) {
  element.classList.add('display-none');
  element.parentElement.lastElementChild.classList.remove('display-none');
  switch(element.parentElement.id) {
    case "details-company-size": 
      addCompanySize(element);
      break;
    case "details-salary-range": 
      addSalaryRange(element.parentElement.lastElementChild.firstElementChild);
      break;
    case "details-job-type": 
      addJobType(element);
      break;
    case "details-federal-contractor": 
      addFederalContractor(element);
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

function addSalaryRange(element) {
  textInputToCurrency(element);
}

function addJobType() {

}

function addFederalContractor() {

}

function addUserNotes() {

}