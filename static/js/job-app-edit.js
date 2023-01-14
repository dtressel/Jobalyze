const addFactorInput = document.getElementById('add-factor-input');
const addFactorButton = document.getElementById('add-factor-button');
const factorCheckboxUl = document.getElementById('factor-checkbox-ul');

addFactorButton.addEventListener('click', addFactorButtonClick);

function addFactorButtonClick() {
  const factorName = addFactorInput.value;
  if (factorName === '') {
    return;
  }
  const factorObj = {name: factorName, id: factorName, new: true};
  addFactorToForm(factorObj);
  addFactorInput.value = '';
}

function addFactorToForm(factor) {
  const checkbox = document.createElement('input');
  checkbox.setAttribute('type', 'checkbox');
  checkbox.setAttribute('value', factor.id);
  checkbox.setAttribute('name', 'factor');
  checkbox.classList.add('new-factor');
  checkbox.checked = true;
  const checkboxLabel = document.createElement('label');
  checkboxLabel.textContent = factor.name;
  const containerLi = document.createElement('li');
  containerLi.append(checkbox);
  containerLi.append(checkboxLabel);
  factorCheckboxUl.append(containerLi);
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

// On Page load:
markSelectedOptionsForSelectInputs();