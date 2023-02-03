// Requirements:
// On each <select> element, include a 'data-value' ('data_value' in WTForms) attribute equal to the value of the selected option.

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

// On Page load:
markSelectedOptionsForSelectInputs();