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
  // Replaces old input value with new input value in currency format
}