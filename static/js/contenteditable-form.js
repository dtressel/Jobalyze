// Requirements:
// Form must have a class of "contenteditable-form"
// Form must have a submit button with a class of "contenteditable-form-submit"
// Submit button must have type="button"
// Form must contain a contenteditable div with class of "contenteditable-field"
// The next element after the contenteditable div must be a hidden input (type="text")
  // to where the value of the contenteditable div will be transferred.
// There must be only one form with contenteditable divs or else only the first will work.
// cleanHTML.js script must also be added to html file before this file.

// Note 1: There may be multiple contenteditable div fields in the form.
// Note 2: This is module is most valuable if this is the only JS necessary on form submit.

const contenteditableForms = document.getElementsByClassName('contenteditable-form');
const contenteditableFormSubmits = document.getElementsByClassName('contenteditable-form-submit');
const editableDivs = document.getElementsByClassName('contenteditable-field');

contenteditableFormSubmits[0].addEventListener('click', submitButtonClick);

function submitButtonClick() {
  for (const div of editableDivs) {
    const value = cleanHTML(div.innerHTML);
    div.nextElementSibling.value = value;
  }
  contenteditableForms[0].submit();
}