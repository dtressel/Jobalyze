
function markSelectedOptionsForSelectInputs() {
  const selectInputs = document.getElementsByTagName('select');
  for (input of selectInputs) {
    const value = input.dataset.value;
    const optionList = input.childNodes;
    for (option of optionList) {
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