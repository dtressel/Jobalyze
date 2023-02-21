function textInputToCurrency(textInput) {
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
  // Turns string into number
  const num = +filteredValue;
  // Adds US currency symbols
  const currencyString = num.toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits: 0});
  // Replaces old value with new in currency format
  input.value = currencyString;
}

function usLocaleStrToInt(str) {
  const strFiltered = [...str].filter((char) => !isNaN(char)).join('');
  return +strFiltered;
}

function fromUsLocaleStr(str) {
  return [...str].filter((char) => !isNaN(char)).join('');
}