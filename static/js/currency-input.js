function textInputToCurrency(textInput) {
  textInput.addEventListener('input', replaceValue);
}

function replaceValue(evt) {
  const inputValue = evt.target.value;
  const filteredValue = [...inputValue].filter((char) => !isNaN(char)).join('');
  // Removes all non-number characters
  const num = +filteredValue;
  // Turns string into number
  const currencyString = num.toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits: 0});
  // Adds US currency symbols
  evt.target.value = currencyString;
  // Replaces old value with new in currency format
}

function usLocaleStrToInt(str) {
  const strFiltered = [...str].filter((char) => !isNaN(char)).join('');
  return +strFiltered;
}

function fromUsLocaleStr(str) {
  return [...str].filter((char) => !isNaN(char)).join('');
}