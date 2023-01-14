const editableDivFields = document.getElementsByClassName('contenteditable-field');

for (field of editableDivFields) {
  field.addEventListener('click', editableDivFieldClick);
}

function editableDivFieldClick(evt) {
  
}