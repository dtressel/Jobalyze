const addFactorInput = document.getElementById('add-factor-input');
const addFactorButton = document.getElementById('add-factor-button');
const factorCheckboxUl = document.getElementById('factor-checkbox-ul');

const editForm = document.getElementById('edit-form');
const saveButton = document.getElementById('save-button');
const editableDivs = document.getElementsByClassName('contenteditable-field');

addFactorButton.addEventListener('click', addFactorButtonClick);
saveButton.addEventListener('click', saveButtonClick);

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

function saveButtonClick() {
  for (const div of editableDivs) {
    const value = cleanHTML(div.innerHTML);
    div.nextElementSibling.value = value;
  }
  editForm.submit();
}