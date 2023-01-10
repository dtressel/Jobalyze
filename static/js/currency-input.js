function textInputToCurrency(textInput) {
  textInput.addEventListener('input', (evt) => replaceValue(evt.target));
  if (textInput.value) {
    replaceValue(textInput);
  }
}

function replaceValue(input) {
  const inputValue = input.value;
  const filteredValue = [...inputValue].filter((char) => !isNaN(char)).join('');
  // Removes all non-number characters
  const num = +filteredValue;
  // Turns string into number
  const currencyString = num.toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits: 0});
  // Adds US currency symbols
  input.value = currencyString;
  // Replaces old value with new in currency format
}

function usLocaleStrToInt(str) {
  const strFiltered = [...str].filter((char) => !isNaN(char)).join('');
  return +strFiltered;
}

function fromUsLocaleStr(str) {
  return [...str].filter((char) => !isNaN(char)).join('');
}