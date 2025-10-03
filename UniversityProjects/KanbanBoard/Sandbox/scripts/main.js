/**\
 * Tasks to store the relevant data
 * this file is responsible for the functionalities in the product backlog page
 *
 * Last modified: 17-10-2022

// Tasks to store the relevant data

/**
 * Key for details of current sprint, end, start date, name
 */
const CURRENT_SPRINT_DETAILS = "currentsprintdetails"

/**
 * opens the task popup page
 */
function openPopUp(){
     window.location = "taskPopup.html"
}

/**
 * opens the edit popup page
 */
function openEditPopup(i){
    updateLSData(TASK_KEY, i);
    window.location = "editTaskPopup.html"
}

/**
 * opens the details task popup page
 */
function openDetailsPopup(i, status){
    updateLSData(TASK_KEY, i);
    updateLSData(STATUS_KEY , status)
    window.location = "taskDetailsPopup.html"
}

/**
 * opens the time spent popup page
 */
function openTimeSpentPopup(i){
    updateLSData(TASK_KEY, i);
    window.location = "timeSpentPopup.html"
}

/**
 * opens the task popup page
 */
function openStartSprint(){
    if(retrieveLSData(TODOS_KEY) == undefined){
        window.location = "startSprintPopup.html"
    } else {
        // If TODOS_KEY exists then a sprint has already started and has not been ended yet
        alert("there is an on going sprint, cant start another sprint")
    }
}

/**
 * Runs remove task after confirmation
 */
function deleteTaskConfirm(index){
    let text = "Are you sure to delete this task "+ parseInt(index+1) +"?";
    if (confirm(text)){
        removeTask(index);
    }
}

function openAddAssigneePopup(i){
    updateLSData(TASK_KEY, i);
    window.location = "addAssigneePopup.html"
}

/**
 * this function will create a task given the vallues that the user gives
 */
function createTask(){

    let taskTitle =  document.getElementById("task_name").value;
    //let taskAssignee = document.getElementById("task_assignee").value;
    let taskTag = document.getElementById("task_tag").value;
    let taskType = document.getElementById("task_type").value;
    let taskPriority = document.getElementById("task_priority").value;
    let storyPoint = document.getElementById("story_points").value;
    let description = document.getElementById("task_description").value;

    if (taskTitle == "" | taskTag == "" | taskType == "" | taskPriority == "" | description == ""){
        alert("Some fields are empty");
    } else {
        let task = new Task(taskTitle, null, taskTag, taskType, taskPriority, storyPoint, description)  //TODO: Change assignee from null? (Note: Cannot be user input yet)
        inventory.addTask(task);
        updateLSData(TASKS_KEY, inventory);
        window.location = "productBacklog.html"
    } 
}

/**
 * this functions starts the sprint and keeps the sprint details like sprint name, 
 * start date, end date to the list of sprints, 
 */
function startSprint(){
    {
        //let inventoryS = retrieveLSData(SPRINTS_KEY)
        let l = inventoryS._tasks.length
        for(let index = 0; index < l;index++){
            //let inventoryS = retrieveLSData(SPRINTS_KEY)
            

            let taskTitle =  inventoryS.getTask(index).title._title;
            let taskAssignee = inventoryS.getTask(index).title._name
            let taskTag = inventoryS.getTask(index).title._tag
            let taskType = inventoryS.getTask(index).title._type
            let taskPriority = inventoryS.getTask(index).title._priority
            let storyPoint = inventoryS.getTask(index).title._storyPoint
            let description = inventoryS.getTask(index).title._description

            let task = inventoryS._tasks.splice(index,1)

            let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
            updateLSData(SPRINTS_KEY, inventoryS)
            inventoryTodo.addTask(newTask)
            updateLSData(TODOS_KEY,inventoryTodo)
        }
        updateLSData(INPROGRESSES_KEY,inventoryInprogress)
        updateLSData(COMPLETES_KEY,inventoryCompleted)
        let sprintTitle = document.getElementById("sprint-title").value
        let sprintStartDate = document.getElementById("sprint-start").value
        let sprintEndDate = document.getElementById("sprint-end").value
        
        let sprintDetails = {sprintName:sprintTitle,startDate:sprintStartDate, endDate:sprintEndDate}
        updateLSData(CURRENT_SPRINT_DETAILS, sprintDetails)
        
        window.location = "kanbanBoard.html"
    }
   
}

/**
 * opens product backlog page
 */
function returnBacklog(){
    window.location = "productBacklog.html"
}

/**
 * removes task from inventory given an index
 */
function removeTask(index) {
  inventory._tasks.splice(index,1);
  updateLSData(TASKS_KEY, inventory);
  window.location = "productBacklog.html"
}

function editTask() {
    let text = "Are you sure edit?";
    if (confirm(text)){
        index = retrieveLSData(TASK_KEY);
        inventory._tasks.splice(index,1);
        createTask();
    }
}

/**
 * loads elements on details page
 */
function loadDetails() {
    data = inventory;

    // Loads a different inventory depending on which column task was in
    taskStatus = retrieveLSData(STATUS_KEY);
    
    if (taskStatus == "todo") {
        data = inventoryTodo;
    }

    if (taskStatus== "inprogress") {
        data = inventoryInprogress
    }

    if (taskStatus == "completed") {
        data = inventoryCompleted
    }

    if (taskStatus == "productBacklog") {
        data = inventory
    }

    if (taskStatus == "sprintBacklog") {
        data = inventoryS
    }

    index = retrieveLSData(TASK_KEY);

    // Displaying on web page
    document.getElementById("task_name").innerHTML += `<p style="font-size: 25; text-align: center">${data.getTask(index).title._title}</p>`;
    document.getElementById("task_assignee").innerHTML += `<p style="font-size: 18; margin-top: 5">${data.getTask(index).title._name}</p>`;
    document.getElementById("task_tag").innerHTML += `<p style="font-size: 18; margin-top: 5">${data.getTask(index).title._tag}</p>`;
    document.getElementById("task_type").innerHTML += `<p style="font-size: 18; margin-top: 5">${data.getTask(index).title._type}</p>`;
    document.getElementById("task_priority").innerHTML += `<p style="font-size: 18; margin-top: 5">${data.getTask(index).title._priority}</p>`;
    document.getElementById("story_points").innerHTML += `<p style="font-size: 18; margin-top: 5">${data.getTask(index).title._storyPoint}</p>`;
    document.getElementById("task_description").innerHTML += `<p style="font-size: 15; margin-top: 5">${data.getTask(index).title._description}</p>`;

}


/**
 * Sets presets attributes when opening the edit page for task
 */
function presetAttribute(){
    data = inventory;

    index = retrieveLSData(TASK_KEY);

    document.getElementById("task_name").setAttribute('value',data.getTask(index).title._title);
    //document.getElementById("task_assignee").setAttribute('value',data.getTask(index).title._name);
    //document.getElementById("task_assignee").value = data.getTask(index).title._name;
    document.getElementById("task_tag").setAttribute('value',data.getTask(index).title._tag);
    document.getElementById("task_type").setAttribute('value',data.getTask(index).title._type);
    document.getElementById("task_priority").setAttribute('value',data.getTask(index).title._priority);
    document.getElementById("story_points").setAttribute('value',data.getTask(index).title._storyPoint);
}

/**
 * this function is responsible to display the tasks to the product backlog
 * @param {*} data 
 */

function display(data) {
        let outputRef1 = document.getElementById("productBacklog");
        
        let output1 = "";
       

        let flag = false;

        
        for (let i = 0; i < data.tasks.length; i++) {

            if (filter.value == "none") {
                flag = true;
            }
            else if (filter.value == data.getTask(i).title._tag) {
                flag = true;
            }
            else {
                flag = false;
            }

            if (flag == true) {
                output1 += `<div class="demo-card mdl-card mdl-shadow--2dp">
                <div class="mdl-card__title">
                <p class="mdl-card__title-text" style="font-weight: bold; font-family: arial; font-size: small">${data.getTask(i).title._title}</p>
                </div>
                <div class="mdl-card__supporting-text">
                <p style="font-weight: bold; font-size: small">ASSIGNEE: ${data.getTask(i).title._name} <br>HOURS SPENT: ${data.getTask(i).title._timeSpent} <br>STORY POINTS: ${data.getTask(i).title._storyPoint}</p>
                </div>      
                
        
                <div class="mdl-card__actions mdl-card--border">
                    <button onclick="openDetailsPopup(${i}, 'productBacklog')" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" style="font-weight: bold; font-size: small; margin-right: 20%">
                    Details
                    </button>

                    <button onclick="deleteTaskConfirm(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title = "Delete task">
                    <i class="material-icons">delete square</i>
                </button>

                    <button onclick="openEditPopup(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title = "Edit task">
                    <i class="material-icons">edit square</i>
                </button>

                    <button onclick="moveTaskToSprint(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title = "Move to Sprint Backlog">
                    <i class="material-icons" > chevron_right </i>
                </button>
                </div>
            </div>
            <br>`
                
                
            }
            
        }

        outputRef1.innerHTML = output1;

}
    
/**
 * this function is responsible to display the tasks to the sprint backlog
 * @param {*} data 
 */


function displaySprint(data) {
        let outputRef1 = document.getElementById("sprintBacklog");
        let output2 = "";
        let flag = false;

        for (let i = 0; i < data.tasks.length; i++) {
    
            if (filter.value == "none") {
                flag = true;
            }
            else if (filter.value == data.getTask(i).title._tag) {
                flag = true;
            }
            else {
                flag = false;
            }
    
            if (flag == true) {
                output2 += `<div class="demo-card mdl-card mdl-shadow--2dp">
                <div class="mdl-card__title">
                <p class="mdl-card__title-text" style="font-weight: bold; font-family: arial; font-size: small">${data.getTask(i).title._title}</p>
                </div>
                <div class="mdl-card__supporting-text">
                <p style="font-weight: bold; font-size: small">ASSIGNEE: ${data.getTask(i).title._name} <br>HOURS SPENT: ${data.getTask(i).title._timeSpent} <br>STORY POINTS: ${data.getTask(i).title._storyPoint}</p>
                </div>      
        
                <div class="mdl-card__actions mdl-card--border">
                    <button onclick="openDetailsPopup(${i}, 'sprintBacklog')" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" style="font-weight: bold; font-size: small; margin-right: 50%">
                    Details
                    </button>

                <button onclick="moveTaskToBacklog(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title = "Move to Product Backlog">
                <i class="material-icons"> chevron_left </i>
            </button>
                </div>
            </div>
            <br>`

            
            }
        }
        outputRef1.innerHTML = output2;
    }

/**
 * Add the tracked time to the task, and calls the relevant time tracking methods to save the data for progress review
 * purposes then returns to the kanban board page
 */
function addTimeSpent(){
    index = retrieveLSData(TASK_KEY);

    let task = inventoryInprogress.getTask(index)
    let timeInput = parseInt(document.getElementById("task_time_spent").value);
    let timeLogged = parseInt(inventoryInprogress.getTask(index).title._timeSpent) + timeInput
    let teamMember = document.getElementById("task_assignee").value;
    task.title._timeSpent = timeLogged;
    
    updateLSData(INPROGRESSES_KEY,inventoryInprogress)

    timeInventory.addTimeLog(timeInput, teamMember);
    updateLSData(TIME_DATA_KEY, timeInventory);

    window.location = "kanbanBoard.html"
  }

  /**
   * this function moves the task to the sprint backlog
   * @param {*} index 
   */
  function moveTaskToSprint(index){
    let taskTitle =  inventory.getTask(index).title._title
    let taskAssignee = inventory.getTask(index).title._name
    let taskTag = inventory.getTask(index).title._tag
    let taskType = inventory.getTask(index).title._type
    let taskPriority = inventory.getTask(index).title._priority
    let storyPoint = inventory.getTask(index).title._storyPoint
    let description = inventory.getTask(index).title._description

    inventory._tasks.splice(index,1)


    let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
    console.log(newTask)

    updateLSData(TASKS_KEY,inventory)
    inventoryS.addTask(newTask)
    updateLSData(SPRINTS_KEY, inventoryS)
   
    location.reload()
  }

  /**
   * this function moves the task to the backlog
   * @param {*} index 
   */
  function moveTaskToBacklog(index){
    let taskTitle =  inventoryS.getTask(index).title._title
    let taskAssignee = inventoryS.getTask(index).title._name
    let taskTag = inventoryS.getTask(index).title._tag
    let taskType = inventoryS.getTask(index).title._type
    let taskPriority = inventoryS.getTask(index).title._priority
    let storyPoint = inventoryS.getTask(index).title._storyPoint
    let description = inventoryS.getTask(index).title._description

    inventoryS._tasks.splice(index,1)


    let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
    console.log(newTask)

    updateLSData(SPRINTS_KEY, inventoryS)
    inventory.addTask(newTask)
    updateLSData(TASKS_KEY,inventory)

    location.reload()
   
  }
  
  /**
   * this function ensures that all the code runs before activating the html page
   */
  document.addEventListener("DOMContentLoaded", 
  function(){
    let path = window.location.pathname;
    let page = path.split("/").pop();
    if(page =="productBacklog.html" ){
        display(inventory); 
        displaySprint(inventoryS); 
    }
    }
  )

  function displayAll(){
    display(inventory)
    displaySprint(inventoryS)
  }


