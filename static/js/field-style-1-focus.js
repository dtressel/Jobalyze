// HTML Requirements:
// contenteditable form group must have class name of 'contenteditable-field-group'
// contenteditable div must be have class name of 'contenteditable-field'

const contenteditableFormGroup = document.querySelectorAll('.field-style-1.contenteditable-field-group');
const regularFieldFormGroup = document.querySelectorAll('.field-style-1:not(.contenteditable-field-group)');

for (const field of regularFieldFormGroup) {
  field.addEventListener('click', (evt) => regularFieldFormGroupClick(evt, field));
}

for (const field of contenteditableFormGroup) {
  for (const child of field.children) {
    if (child.contentEditable !== 'true') {
      child.style.pointerEvents = 'none';
    }
  }
  field.addEventListener('click', contenteditableFormGroupClick);
}

function regularFieldFormGroupClick(evt, field) {
  if (evt.target === field) {
    const input = field.querySelectorAll('input, select, textarea')[0];
    input.focus();
    if (input.type === "checkbox") {
      input.checked = !input.checked;
    }
  }
  // First if statement assures that this only forces focus when clicking on empty space in form group div
  // Necessary for dual input form group where without it clickinig on 2nd input would force focus back to 1st input
}

function contenteditableFormGroupClick(evt) {
  if (evt.target.contentEditable !== 'true') {
    evt.target.getElementsByClassName('contenteditable-field')[0].focus();
  }
}