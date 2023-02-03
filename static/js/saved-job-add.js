const saveButton = document.getElementById('save-button');
const editableDivs = document.getElementsByClassName('contenteditable-field');

saveButton.addEventListener('click', saveButtonClick);

function saveButtonClick() {
  if (document.getElementById('job_type').value === '-') {
    document.getElementById('job_type').value = null;
  }
  if (document.getElementById('experience_level').value === '-') {
    document.getElementById('experience_level').value = null;
  }
  if (document.getElementById('company_size').value === '-') {
    document.getElementById('company_size').value = null;
  }
  if (document.getElementById('federal_contractor').value === '-') {
    document.getElementById('federal_contractor').value = null;
  }
  if (document.getElementById('salary_min').value != '') {
    document.getElementById('salary_min').value = fromUsLocaleStr(document.getElementById('salary_min').value);
  }
  if (document.getElementById('salary_max').value != '') {
    document.getElementById('salary_max').value = fromUsLocaleStr(document.getElementById('salary_max').value);
  }
  for (const div of editableDivs) {
    const value = cleanHTML(div.innerHTML);
    div.nextElementSibling.value = value;
  }
  document.getElementById('saved-job-add-form').submit();
}

// On Load:
textInputToCurrency(document.getElementById('salary_min'));
textInputToCurrency(document.getElementById('salary_max'));