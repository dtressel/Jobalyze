// HTML Requirements:
// contenteditable form group must have class name of 'contenteditable-field-group'
// contenteditable div must be have class name of 'contenteditable-field'

const contenteditableFormGroup = document.getElementsByClassName('contenteditable-field-group');

for (field of contenteditableFormGroup) {
  for (child of field.children) {
    if (child.contentEditable !== 'true') {
      child.style.pointerEvents = 'none';
    }
  }
  field.addEventListener('click', contenteditableFormGroupClick);
}

function contenteditableFormGroupClick(evt) {
  if (evt.target.contentEditable !== 'true') {
    evt.target.getElementsByClassName('contenteditable-field')[0].focus();
  }
}