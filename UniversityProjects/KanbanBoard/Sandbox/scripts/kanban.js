/**
 * This file contains the functionality for the kanban board page, allowing it to display, move, and filter the tasks
 *
 * Last modified: 17-10-2022
 */
        
/**
 * This function displays the tasks that are still in the to-do section of the kanban board page using dynamically
 * written HTML
 *
 * @param data - The task data that is to be displayed
 */
function displayTodo(data) {
        let outputRef1 = document.getElementById("todo");
        let output1 = "";
        let flag = false;

        console.log(filter.value)
        
        for (let i = 0; i < data._tasks.length; i++) {

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
                    <button onclick="openDetailsPopup(${i}, 'todo')" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" style="font-weight: bold; font-size: small; margin-right: 35%">
                    Details
                    </button>

                    <button onclick="openAddAssigneePopup(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title = "Change Assignee">
                    <i class="material-icons">person</i>
                </button>
                <button onclick="moveTaskToInprogressFromTodo(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title= "Move to 'In Progress'">
                    <i class="material-icons"> chevron_right </i>
                </button>
                </div>
            </div>
            <br>`
            }
        }
        outputRef1.innerHTML = output1;
    }


/**
 * This function moves task from in progress to to-do in the kanban board page.
 *
 * @param index - The index of the specific task instance that is to be moved
 */
function moveTaskToInprogressFromTodo(index){
         
        let taskTitle = inventoryTodo.getTask(index).title._title;
        let taskAssignee = inventoryTodo.getTask(index).title._name
        let taskTag = inventoryTodo.getTask(index).title._tag
        let taskType = inventoryTodo.getTask(index).title._type
        let taskPriority = inventoryTodo.getTask(index).title._priority
        let storyPoint = inventoryTodo.getTask(index).title._storyPoint
        let description = inventoryTodo.getTask(index).title._description
        let timeSpent = inventoryTodo.getTask(index).title._timeSpent

        if (taskAssignee == null) {
            alert("Please set the assignee.");
            return
        }

        let task = inventoryTodo._tasks.splice(index,1)

        let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
        newTask._timeSpent = timeSpent
        updateLSData(TODOS_KEY, inventoryTodo)

        inventoryInprogress.addTask(newTask)
        updateLSData(INPROGRESSES_KEY,inventoryInprogress)

        location.reload()
    }


/**
 * This function displays the tasks that are still in the in-progress section of the kanban board page using dynamically
 * written HTML.
 *
 * @param data - The task data that is to be displayed
 */
    function displayInprogress(data) {
        let outputRef2 = document.getElementById("inprogress");
        let output2 = "";

        let flag = false;

        console.log(filter.value)
        
        for (let i = 0; i < data._tasks.length; i++) {

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
                <button onclick="openDetailsPopup(${i}, 'inprogress')" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" style="font-weight: bold; font-size: small; margin-right: 20%">
                Details
                </button>
                <button onclick="openTimeSpentPopup(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title= "Add Time Spent">
                    <i class="material-icons">schedule square</i>
                </button>
                
                <button onclick="moveTaskToTodo(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title= "Move to 'In Progress'">
                    <i class="material-icons"> chevron_left </i>
                </button>
                <button onclick="moveTaskToCompleted(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title= "Move to 'Completed'">
                    <i class="material-icons"> chevron_right </i>
                </button>
                </div>         
            </div>
            <br>`
            }
            
        }
        

        outputRef2.innerHTML = output2;

    }

/**
 * This function moves task to completed in the kanban board page.
 *
 * @param index - The index of the specific task instance that is to be moved
 */
function moveTaskToCompleted(index){
        let taskTitle = inventoryInprogress.getTask(index).title._title;
        let taskAssignee = inventoryInprogress.getTask(index).title._name
        let taskTag = inventoryInprogress.getTask(index).title._tag
        let taskType = inventoryInprogress.getTask(index).title._type
        let taskPriority = inventoryInprogress.getTask(index).title._priority
        let storyPoint = inventoryInprogress.getTask(index).title._storyPoint
        let description = inventoryInprogress.getTask(index).title._description
        let timeSpent = inventoryInprogress.getTask(index).title._timeSpent

        let task = inventoryInprogress._tasks.splice(index,1)

        let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
        newTask._timeSpent = timeSpent
        newTask._timeCompleted = Date.now();
        updateLSData(INPROGRESSES_KEY,inventoryInprogress)

        inventoryCompleted.addTask(newTask)
        updateLSData(COMPLETES_KEY,inventoryCompleted)

        location.reload()
    }

    /**
     * this function moves task to to do
     * @param {*} index 
     */
    function moveTaskToTodo(index){
        let taskTitle = inventoryInprogress.getTask(index).title._title;
        let taskAssignee = inventoryInprogress.getTask(index).title._name
        let taskTag = inventoryInprogress.getTask(index).title._tag
        let taskType = inventoryInprogress.getTask(index).title._type
        let taskPriority = inventoryInprogress.getTask(index).title._priority
        let storyPoint = inventoryInprogress.getTask(index).title._storyPoint
        let description = inventoryInprogress.getTask(index).title._description
        let timeSpent = inventoryInprogress.getTask(index).title._timeSpent

        let task = inventoryInprogress._tasks.splice(index,1)

        let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description)
        newTask._timeSpent = timeSpent
        updateLSData(INPROGRESSES_KEY,inventoryInprogress)

        inventoryTodo.addTask(newTask)
        updateLSData(TODOS_KEY,inventoryTodo)

        location.reload()
    }


    /**
     * this function displays the completed tasks
     * @param {*} data 
     */
    function displayCompleted(data) {
        let outputRef3 = document.getElementById("completed");
        let output3 = "";
        let flag = false;

        
        for (let i = 0; i < data._tasks.length; i++) {

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
                output3 += `<div class="demo-card mdl-card mdl-shadow--2dp">
                <div class="mdl-card__title">
                <p class="mdl-card__title-text" style="font-weight: bold; font-family: arial; font-size: small">${data.getTask(i).title._title}</p>
                </div>
                <div class="mdl-card__supporting-text">
                <p style="font-weight: bold; font-size: small">ASSIGNEE: ${data.getTask(i).title._name} <br>HOURS SPENT: ${data.getTask(i).title._timeSpent} <br>STORY POINTS: ${data.getTask(i).title._storyPoint}</p>
                </div>      
                
                <div class="mdl-card__actions mdl-card--border">
                <button onclick="openDetailsPopup(${i}, 'completed')" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" style="font-weight: bold; font-size: small; margin-right: 50%">
                Details
                </button>
                <button onclick="moveTaskToInprogressFromCompleted(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" title= "Move to 'In Progress'">
                    <i class="material-icons"> chevron_left </i>
                </button>
                </div>         
            </div>
            <br>`
            }
        }
        outputRef3.innerHTML = output3;
    }

    // to grab the sprint title page header
    function onLoadSprintPage(){
        if (retrieveLSData(CURRENT_SPRINT_DETAILS) == null) {
            target = document.getElementById('sprint-title-header');
            target.innerHTML = 'No active sprint currently.';
        }
        else {
            title =  retrieveLSData(CURRENT_SPRINT_DETAILS).sprintName;

            target = document.getElementById('sprint-title-header');
            target.innerHTML = title;
        }
    }


    /**
     * this function moves task from completed to in progress
     * @param {*} index 
     */
    function moveTaskToInprogressFromCompleted(index){
        let taskTitle = inventoryCompleted.getTask(index).title._title;
        let taskAssignee = inventoryCompleted.getTask(index).title._name;
        let taskTag = inventoryCompleted.getTask(index).title._tag;
        let taskType = inventoryCompleted.getTask(index).title._type;
        let taskPriority = inventoryCompleted.getTask(index).title._priority;
        let storyPoint = inventoryCompleted.getTask(index).title._storyPoint;
        let description = inventoryCompleted.getTask(index).title._description;
        let timeSpent = inventoryCompleted.getTask(index).title._timeSpent;

        let task = inventoryCompleted._tasks.splice(index,1);

        let newTask = new Task(taskTitle, taskAssignee, taskTag, taskType, taskPriority, storyPoint, description);
        newTask._timeSpent = timeSpent;
        updateLSData(COMPLETES_KEY,inventoryCompleted);

        inventoryInprogress.addTask(newTask);
        updateLSData(INPROGRESSES_KEY,inventoryInprogress);

        location.reload();
    }

    /**
     * this function ensures that the code runs before activating the html page
     */
    document.addEventListener("DOMContentLoaded", 
    function(){
      let path = window.location.pathname;
      let page = path.split("/").pop();
      if(page =="kanbanBoard.html" ){
            
          if(inventoryTodo != null){
            displayTodo(inventoryTodo);
          }
          if(inventoryInprogress!=null){
            displayInprogress(inventoryInprogress);
          }
          if(inventoryCompleted!=null){
            displayCompleted(inventoryCompleted); 
          }
      }
    })

    /**
     * this functions will return the user to the kanban page
     */
    function returnToKanban() {
        taskStatus = retrieveLSData(STATUS_KEY)
        if (taskStatus == `productBacklog` || taskStatus == `sprintBacklog`){
            window.location = "productBacklog.html"
        }
        else {
            window.location = "kanbanBoard.html"
        }
    }

    /**
     * this functions ends the current sprint and add the sprint tasks according to their state
     * to the sprint list, and removing them from the local storage, as well changing the page to
     * the past sprints page
     */

    function endSprint(){
        if(window.confirm("Are you sure you want to end the sprint")){
            addToPastSprints( inventoryTodo.tasks, inventoryInprogress.tasks, inventoryCompleted.tasks)
            
            localStorage.removeItem(TODOS_KEY);
            localStorage.removeItem(INPROGRESSES_KEY);
            localStorage.removeItem(COMPLETES_KEY);
            localStorage.removeItem(CURRENT_SPRINT_DETAILS)
            window.reload;
            
            window.location="pastSprints.html"
        }
    }

    function addToPastSprints(todoTasks, inprogressTasks, completedTasks){
        let sprintDetails = retrieveLSData(CURRENT_SPRINT_DETAILS);
        let sprintTitle = sprintDetails.sprintName;
        let sprintStartDate = sprintDetails.startDate;
        let sprintEndDate = sprintDetails.endDate;
        let newSprint = new Sprint(sprintTitle, sprintStartDate, sprintEndDate, todoTasks, inprogressTasks, completedTasks )
        
        //this prevents the code to make a new array of sprints every time a new sprint is made
        if(retrieveLSData(PAST_SPRINTS_KEY) == undefined){
            let sprints = new Sprints();
            sprints.addSprint(newSprint)
            updateLSData(PAST_SPRINTS_KEY,sprints)
        }
        else{
            sprints = retrieveLSData(PAST_SPRINTS_KEY)
            sprints._sprints.push(newSprint)
            updateLSData(PAST_SPRINTS_KEY,sprints)
        }
        

        
    }