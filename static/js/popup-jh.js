const popupJh = document.getElementById('popup-jh');
const popupJhContinueButton = document.getElementById('popup-jh-continue-button');
const popupJhCancelButton = document.getElementById('popup-jh-cancel-button');
const popupJhFinishButton = document.getElementById('popup-jh-finish-button');
const popupJhScreens = document.getElementsByClassName('popup-jh-screen');

popupJhContinueButton.addEventListener('click', continueWizard);
popupJhCancelButton.addEventListener('click', cancelWizard);

let popupJhWindowNum = 0;
let newJobHuntObj = {};

function iAppliedToJhPopup() {
  popupJh.classList.remove('display-none');
  popupJhScreens[0].classList.remove('display-none');
}

function newJobHuntClick() {
  popupJhWindowNum = 1;
  popupJh.classList.remove('display-none');
  hideAllScreens();
  popupJhContinueButton.textContent = 'Start';
  popupJhScreens[1].classList.remove('display-none');
}

function continueWizard() {
  switch(popupJhWindowNum) {
    case 0:
      newJobHuntClick();
      break;
    case 1: 
      popupJh1();
      break;
    case 2: 
      popupJh2();
      break;
    case 3: 
      popupJh3();
      break;
    case 4: 
      popupJh4();
      break;
    case 5: 
      popupJh5();
      break;
    case 6: 
      popupJh6();
      break;
    case 7: 
      popupJh7();
      break;
    case 8: 
      popupJh8();
      break;
    case 9: 
      finishJhAdd();
      break;
  }
}

function popupJh1() {
  hideAllScreens();
  popupJhContinueButton.textContent = 'Continue';
  popupJhScreens[2].classList.remove('display-none');
  popupJhWindowNum++;
}

function popupJh2() {
  hideAllScreens();
  // get data from screen 1:
  newJobHuntObj.job_title_desired = document.getElementById('job-title-desired').value;
  newJobHuntObj.o_net_code = document.getElementById('o-net-code').value;
  popupJhScreens[3].classList.remove('display-none');
  popupJhWindowNum++;
}

function popupJh3() {
  hideAllScreens();
  // get data from screen 2:
  inUs = +document.querySelector('input[name="us-job"]:checked').value;
  if (!inUs) {
    console.log('evaulated as false');
    newJobHuntObj.non_us = true;
    popupJhScreens[7].classList.remove('display-none');
    popupJhWindowNum += 4;
  } else {
    console.log('evaulated as true');
    popupJhScreens[4].classList.remove('display-none');
    popupJhWindowNum++;
  }
}

function popupJh4() {
  hideAllScreens();
  // get data from screen 3:
  const remote = +document.querySelector('input[name="remote"]:checked').value;
  if (remote == 1) {
    console.log('in remote')
    newJobHuntObj.remote = true;
  }
  popupJhScreens[5].classList.remove('display-none');
  popupJhWindowNum++;
  console.log('input:', document.querySelector('#new-job-hunt-form > input[name="remote"]'));
  console.log(newJobHuntObj.remote);
}

function popupJh5() {
  hideAllScreens();
  // get data from screen 4:
  where = document.querySelector('input[name="where"]:checked').value;
  if (where === 'anywhere') {
    newJobHuntObj.location = 'US'
    popupJhScreens[7].classList.remove('display-none');
    popupJhWindowNum += 2;
  } else {
    popupJhScreens[6].classList.remove('display-none');
    popupJhWindowNum++;
  }
}

function popupJh6() {
  hideAllScreens();
  // get data from screen 5:
  newJobHuntObj.radius = document.getElementById('radius').value;
  newJobHuntObj.location = document.getElementById('location').value;
  popupJhScreens[7].classList.remove('display-none');
  popupJhWindowNum++;
}

function popupJh7() {
  hideAllScreens();
  // get data from screen 6:
  newJobHuntObj.app_goal_number = document.getElementById('app-goal-number').value;
  newJobHuntObj.app_goal_time_frame = document.getElementById('app-goal-time-frame').value;
  popupJhScreens[8].classList.remove('display-none');
  popupJhWindowNum++;
}

function popupJh8() {
  hideAllScreens();
  // get data from screen 7:
  newJobHuntObj.hired_by_goal_date = document.getElementById('hired-by-date').value;
  popupJhContinueButton.textContent = 'Finish';
  popupJhScreens[9].classList.remove('display-none');
  popupJhWindowNum++;
}

function finishJhAdd() {
  // get data from screen 8:
  newJobHuntObj.name = document.getElementById('jh-name').value;
  newJobHuntObj.description = document.getElementById('jh-description').value;
  // Automatically fill and submit hidden form to send to backend
  fillHiddenForm();
  document.getElementById('new-job-hunt-form').submit();
}

function cancelWizard() {
  popupJh.classList.add('display-none');
  newJobHuntObj = {};
  popupJhWindowNum = 1;
  hideAllScreens();
  popupJhContinueButton.textContent = 'Start';
  popupJhCancelButton.textContent = 'Cancel';
  popupJhContinueButton.classList.remove('display-none');
}

function hideAllScreens() {
  for (const screen of popupJhScreens) {
    screen.classList.add('display-none');
  }
}

function fillHiddenForm() {
  document.querySelector('#new-job-hunt-form > input[name="name"]').value = newJobHuntObj.name;
  document.querySelector('#new-job-hunt-form > input[name="job_title_desired"]').value = newJobHuntObj.job_title_desired;
  document.querySelector('#new-job-hunt-form > input[name="o_net_code"]').value = newJobHuntObj.o_net_code;
  document.querySelector('#new-job-hunt-form > input[name="location"]').value = newJobHuntObj.location;
  document.querySelector('#new-job-hunt-form > input[name="radius"]').value = newJobHuntObj.radius;
  document.querySelector('#new-job-hunt-form > input[name="non_us"]').checked = newJobHuntObj.non_us;
  document.querySelector('#new-job-hunt-form > input[name="remote"]').checked = newJobHuntObj.remote;
  document.querySelector('#new-job-hunt-form > input[name="app_goal_time_frame"]').value = newJobHuntObj.app_goal_time_frame;
  document.querySelector('#new-job-hunt-form > input[name="app_goal_number"]').value = newJobHuntObj.app_goal_number;
  document.querySelector('#new-job-hunt-form > input[name="hired_by_goal_date"]').value = newJobHuntObj.hired_by_goal_date;
  document.querySelector('#new-job-hunt-form > input[name="description"]').value = newJobHuntObj.description;
}

// Old submission function when submitting from front end

// async function sendJhToBackend() {
//     // called by popupJh9()
//     const resp = await fetch('/job-hunts/add', {
//       method: 'POST',
//       headers: {'Content-Type': 'application/json'},
//       body: JSON.stringify(newJobHuntObj)
//     })
  
//     return resp
// }