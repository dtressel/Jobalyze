const popup = document.getElementById('popup');
const popupContinueButton = document.getElementById('popup-continue-button');
const popupCancelButton = document.getElementById('popup-cancel-button');
const popupFinishButton = document.getElementById('popup-finish-button');
const popupScreens = document.getElementsByClassName('popup-jh');

popupContinueButton.addEventListener('click', continueWizard);
popupCancelButton.addEventListener('click', cancelWizard);

let popupWindowNum = 1;
let newJobHuntObj = {};

function newJobHuntClick() {
  popup.classList.remove('display-none');
}

function continueWizard() {
  switch(popupWindowNum) {
    case 1: 
      popup1();
      break;
    case 2: 
      popup2();
      break;
    case 3: 
      popup3();
      break;
    case 4: 
      popup4();
      break;
    case 5: 
      popup5();
      break;
    case 6: 
      popup6();
      break;
    case 7: 
      popup7();
      break;
    case 8: 
      popup8();
      break;
    case 9: 
      finishJhAdd();
      break;
  }
}

function popup1() {
  hideAllScreens();
  popupContinueButton.textContent = 'Continue';
  popupScreens[1].classList.remove('display-none');
  popupWindowNum++;
}

function popup2() {
  hideAllScreens();
  // get data from screen 1:
  newJobHuntObj.job_title_desired = document.getElementById('job-title-desired').value;
  newJobHuntObj.o_net_code = document.getElementById('o-net-code').value;
  popupScreens[2].classList.remove('display-none');
  popupWindowNum++;
}

function popup3() {
  hideAllScreens();
  // get data from screen 2:
  inUs = +document.querySelector('input[name="us-job"]:checked').value;
  if (!inUs) {
    console.log('evaulated as false');
    newJobHuntObj.non_us = true;
    popupScreens[6].classList.remove('display-none');
    popupWindowNum += 4;
  } else {
    console.log('evaulated as true');
    popupScreens[3].classList.remove('display-none');
    popupWindowNum++;
  }
}

function popup4() {
  hideAllScreens();
  // get data from screen 3:
  remote = +document.querySelector('input[name="remote"]:checked').value;
  if (remote) {
    newJobHuntObj.remote = true;
  }
  popupScreens[4].classList.remove('display-none');
  popupWindowNum++;
}

function popup5() {
  hideAllScreens();
  // get data from screen 4:
  where = document.querySelector('input[name="where"]:checked').value;
  if (where === 'anywhere') {
    newJobHuntObj.location = 'US'
    popupScreens[6].classList.remove('display-none');
    popupWindowNum += 2;
  } else {
    popupScreens[5].classList.remove('display-none');
    popupWindowNum++;
  }
}

function popup6() {
  hideAllScreens();
  // get data from screen 5:
  newJobHuntObj.radius = document.getElementById('radius').value;
  newJobHuntObj.location = document.getElementById('location').value;
  popupScreens[6].classList.remove('display-none');
  popupWindowNum++;
}

function popup7() {
  hideAllScreens();
  // get data from screen 6:
  newJobHuntObj.app_goal_number = document.getElementById('app-goal-number').value;
  newJobHuntObj.app_goal_time_frame = document.getElementById('app-goal-time-frame').value;
  popupScreens[7].classList.remove('display-none');
  popupWindowNum++;
}

function popup8() {
  hideAllScreens();
  // get data from screen 7:
  newJobHuntObj.hired_by_goal_date = document.getElementById('hired-by-date').value;
  popupContinueButton.textContent = 'Finish';
  popupScreens[8].classList.remove('display-none');
  popupWindowNum++;
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
  popup.classList.add('display-none');
  newJobHuntObj = {};
  popupWindowNum = 1;
  hideAllScreens();
  popupScreens[0].classList.remove('display-none');
  popupContinueButton.textContent = 'Start';
  popupCancelButton.textContent = 'Cancel';
  popupContinueButton.classList.remove('display-none');
}

function hideAllScreens() {
  for (const screen of popupScreens) {
    screen.classList.add('display-none');
  }
}

function fillHiddenForm() {
  document.querySelector('#new-job-hunt-form > input[name="name"]').value = newJobHuntObj.name;
  document.querySelector('#new-job-hunt-form > input[name="job_title_desired"]').value = newJobHuntObj.job_title_desired;
  document.querySelector('#new-job-hunt-form > input[name="o_net_code"]').value = newJobHuntObj.o_net_code;
  document.querySelector('#new-job-hunt-form > input[name="location"]').value = newJobHuntObj.location;
  document.querySelector('#new-job-hunt-form > input[name="radius"]').value = newJobHuntObj.radius;
  document.querySelector('#new-job-hunt-form > input[name="non_us"]').value = newJobHuntObj.non_us;
  document.querySelector('#new-job-hunt-form > input[name="remote"]').value = newJobHuntObj.remote;
  document.querySelector('#new-job-hunt-form > input[name="app_goal_time_frame"]').value = newJobHuntObj.app_goal_time_frame;
  document.querySelector('#new-job-hunt-form > input[name="app_goal_number"]').value = newJobHuntObj.app_goal_number;
  document.querySelector('#new-job-hunt-form > input[name="hired_by_goal_date"]').value = newJobHuntObj.hired_by_goal_date;
  document.querySelector('#new-job-hunt-form > input[name="description"]').value = newJobHuntObj.description;
}

// Old submission function when submitting from front end

// async function sendJhToBackend() {
//     // called by popup9()
//     const resp = await fetch('/job-hunts/add', {
//       method: 'POST',
//       headers: {'Content-Type': 'application/json'},
//       body: JSON.stringify(newJobHuntObj)
//     })
  
//     return resp
// }