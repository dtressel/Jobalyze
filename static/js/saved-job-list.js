const daysAgoRadios = document.querySelectorAll('input[name="days-ago"]');
const includeAppliedCheckbox = document.getElementById('include-applied-checkbox');
const tbodyList = document.getElementsByTagName('tbody');

let daysAgo = document.getElementById('days-ago-filter').dataset.daysAgo;
let includeApplied = document.getElementById('include-applied-filter').dataset.includeApplied;

// Event Listeners for Filters
for (const radio of daysAgoRadios) {
  radio.addEventListener('change', daysAgoRadioChange)
}
includeAppliedCheckbox.addEventListener('change', includeAppliedChange)

// Event Listener for Delete Buttons
tbodyList[0].addEventListener('click', deleteButtonClick);

function daysAgoRadioChange(evt) {
  daysAgo = evt.target.value;
  window.location.replace(`/saved-jobs?days=${daysAgo}&ia=${includeApplied}`);
}

function includeAppliedChange() {
  if (includeApplied === 'yes') {
    includeApplied = 'no'
  } else {
    includeApplied = 'yes'
  }
  window.location.replace(`/saved-jobs?days=${daysAgo}&ia=${includeApplied}`);
}

function deleteButtonClick(evt) {
  if (evt.target.classList[0] === 'delete-button') {
    const savedJobId = evt.target.id;
    const company = document.getElementById(`company-${savedJobId}`).textContent;
    const title = document.getElementById(`title-${savedJobId}`).textContent;
    const text = `Delete the following saved job?\n\n${title}\n${company}`;
    if (confirm(text)) {
      evt.target.parentElement.submit();
    }
  }
}

// On Load:
document.getElementById(`days-ago-${daysAgo}`).checked = true;
if (includeApplied === 'yes') {
  includeAppliedCheckbox.checked = true;
}