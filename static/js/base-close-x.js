// Requirements:
// The close-x element must have a class name of 'close-x'.
// The window that is closed should be the direct parent of the close-x element.

const closeXs = document.getElementsByClassName('close-x');

if (closeXs) {
  for (const closeX of closeXs) {
    closeX.addEventListener('click', closeWindow);
  }
}

function closeWindow(evt) {
  evt.target.parentElement.hidden = true;
}