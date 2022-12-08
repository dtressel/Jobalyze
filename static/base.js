const userIcon = document.getElementById('user-icon');
const userIconPopup = document.getElementById('user-icon-popup');
userIcon.addEventListener('click', displayUserIconPopup);
let userIconDisplayed = false;

function displayUserIconPopup(evt) {
  userIconPopup.classList.toggle('display-none');
  userIconDisplayed = !userIconDisplayed;
  if (userIconDisplayed) {
    userIcon.addEventListener('mouseleave', leaveUserIcon, {once: true});
  }
}

function leaveUserIcon() {
  if (userIconDisplayed) {
    window.addEventListener('click', hideUserIconPopup, {once: true});
  }
}

function hideUserIconPopup(evt) {
  if (evt.target.id != "user-icon-popup") {
    userIconPopup.classList.add('display-none');
    userIconDisplayed = false;
  }
  window.addEventListener('mousemove', leaveUserIcon, {once: true});
}