const daysAgoRadios = document.querySelectorAll('input[name="days-ago"]');
const includeAppliedCheckbox = document.getElementById('include-applied-checkbox');

let daysAgo = document.getElementById('days-ago-filter').dataset.daysAgo;
let includeApplied = document.getElementById('include-applied-filter').dataset.includeApplied;

for (const radio of daysAgoRadios) {
  radio.addEventListener('change', daysAgoRadioChange)
}
includeAppliedCheckbox.addEventListener('change', includeAppliedChange)

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

// On Load:
document.getElementById(`days-ago-${daysAgo}`).checked = true;
console.log(includeApplied);
if (includeApplied === 'yes') {
  includeAppliedCheckbox.checked = true;
}