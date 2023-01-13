const saveUpdatesButton = document.getElementById('save-updates-button');
const jobAppDeleteButtons = document.getElementsByClassName('job-app-delete-button');
const jobAppListTbody = document.getElementById('job-app-list-tbody');
const jobAppListTable = document.getElementById('job-app-list-table');

let changedSelectsList = [];

saveUpdatesButton.addEventListener('click', saveUpdatesButtonClick);
jobAppListTbody.addEventListener('click', jobAppListTbodyClick);

function jobAppListTbodyClick(evt) {
  if (evt.target.classList[0] === 'job-app-delete-button'){
    jobAppDeleteButtonClick(evt.target.parentElement.parentElement.rowIndex, evt.target.dataset.appId);
  }
  if (evt.target.localName = 'select') {
    evt.target.addEventListener('change', selectChange, {once: true});
  }
}

async function jobAppDeleteButtonClick(rowIndex, jobAppId) {
  const resp = await fetch(`/job-apps/${jobAppId}/delete`, {
    method: 'DELETE'
  })
  if (resp.status === 200) {
    jobAppListTable.deleteRow(rowIndex);
    // ****************** Add Message ***********************
  }
}

function selectChange(evt) {
  if (!changedSelectsList.includes(evt.target)) {
    changedSelectsList.push(evt.target);
    evt.target.parentElement.classList.add('pending-changes');
    evt.target.classList.add('pending-changes');
  }
}

async function saveUpdatesButtonClick() {
  const indexesUpdated = [];
  for (let i = 0; i < changedSelectsList.length; i++) {
    const jobAppId = changedSelectsList[i].dataset.appId;
    const currentStatusValue = changedSelectsList[i].value;
    const resp = await fetch(`/job-apps/${jobAppId}/edit/json`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({current_status: currentStatusValue})
    })
    if (resp.status === 200) {
      console.log('200 status code');
      indexesUpdated.push(i);
      changedSelectsList[i].parentElement.classList.remove('pending-changes');
      changedSelectsList[i].classList.remove('pending-changes');
    }
  }
  if (indexesUpdated.length === changedSelectsList.length) {
    changedSelectsList = [];
    // ******************************** display success message *****************************
  } else {
    for (const index of indexesUpdated) {
      changedSelectsList.splice(index, 1);
    }
  }
}


