// Requirements:
// Input must have type = "text"
// Input must have a "data-input-type" equal to "integer"

const integerInputs = document.querySelectorAll('input[data-input-type="integer"]');

for (const input of integerInputs) {
  textInputToInteger(input);
}

function textInputToInteger(textInput) {
  if (textInput.value && textInput.value !== 'None') {
    replaceValue(textInput);
  } else {
    textInput.value = '';
  }
  textInput.addEventListener('input', (evt) => replaceValue(evt.target));
}

function replaceValue(input) {
  const inputValue = input.value;
  // Removes all non-number characters
  const filteredValue = [...inputValue].filter((char) => !isNaN(char)).join('');
  // Replaces old value with new filtered value
  input.value = filteredValue;
}