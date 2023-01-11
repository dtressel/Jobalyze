const savedJobAddForm = document.getElementById('saved-job-add-form');
const saveButton = document.getElementById('save-button');
const editableDivs = document.getElementsByClassName('contenteditable-field');

saveButton.addEventListener('click', saveButtonClick);

function saveButtonClick() {
  for (const div of editableDivs) {
    const value = div.innerHTML;
    div.nextElementSibling.value = value;
  }
  savedJobAddForm.submit();
}

function markSelectedOptionsForSelectInputs() {
  const selectInputs = document.getElementsByTagName('select');
  for (const input of selectInputs) {
    const value = input.dataset.value;
    const optionList = input.childNodes;
    for (const option of optionList) {
      if (option.value === value) {
        option.selected = true;
      }
    }
  }
}

// On Page Load:
textInputToCurrency(document.getElementById('salary_min'));
textInputToCurrency(document.getElementById('salary_max'));
markSelectedOptionsForSelectInputs();