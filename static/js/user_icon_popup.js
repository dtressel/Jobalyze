// Load DOM objects:
const userIcon = document.getElementById('user-icon');
const userIconPopup = document.getElementById('user-icon-popup');

let userIconDisplayed = false;

// Event Listener:
userIcon.addEventListener('click', displayUserIconPopup);

// On click of user icon display popup if not already showing
function displayUserIconPopup(evt) {
  userIconPopup.classList.toggle('display-none');
  userIconDisplayed = !userIconDisplayed;
  if (userIconDisplayed) {
    userIcon.addEventListener('mouseleave', leaveUserIcon, {once: true});
  }
}

// When mouse leaves user icon while popup is showing add window click event listener
function leaveUserIcon() {
  if (userIconDisplayed) {
    window.addEventListener('click', hideUserIconPopup, {once: true});
  }
}

// When click on anywhere in the window close popup
// except when clicking on empty space in popup
// in that case re-add window click event listener when mouse moves
function hideUserIconPopup(evt) {
  if (evt.target.id != "user-icon-popup") {
    userIconPopup.classList.add('display-none');
    userIconDisplayed = false;
  }
  window.addEventListener('mousemove', leaveUserIcon, {once: true});
}