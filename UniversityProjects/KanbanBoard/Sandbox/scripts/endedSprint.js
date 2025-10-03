/**
 * this file is responsible for sprints that has been done
 * 
 * Last modified: 17/10/2022
 */

const CURRENT_SPRINT = "currentsprint"
const PAST_SPRINTS_KEY = "sprints"

/**
 * This class is to record the data for each new sprint that the user creates
 */
class Sprint{
    constructor(sprintTitle,startDate, endDate, todoTasks, inprogressTasks,completedTask ){
        this.sprintName = sprintTitle
        this.startDate = startDate
        this.endDate = endDate
        this.todo = todoTasks
        this.inprogress = inprogressTasks
        this.completed = completedTask
    }


}

/**
 * A class that will store all sprints that has been created
 */
class Sprints{
    constructor(){
        this._sprints = []
    }

    /**
     * This method will be called when the user has decided to start the sprint,
     * it initialises the tasks as an empty array and will store the new sprint instance.

     * @param sprint - An instance of the sprint class that is to be added to the sprint storage
     */
    addSprint(sprint){
        this._sprints.push(sprint)
    }
}


//makes sure that there is only 1 instance of this sprints
// Object.freeze(sprints)

/**
 * Display the sprints that has been done, displays the sprint name, the start
 * and end date, as well as the tasks and their states
 * @param {data} this is the sprints 
 */
function displayPastSprints(data){
    let outputRef3 = document.getElementById("pastSprints");
        let output3 = "";
        
        for (let i = 0; i < data.length; i++) {

            let completedTasks ="";

            for (let j = 0;j< data[i].completed.length;j++){
                completedTasks+=data[i].completed[j].title._title + ', '
            }

            let todoTasks = ""

            for (let j = 0;j< data[i].todo.length;j++){
                todoTasks+=data[i].todo[j].title._title + ', '
            }

            let inprogressTasks = ""

            for (let j = 0;j< data[i].inprogress.length;j++){
                inprogressTasks+=data[i].inprogress[j].title._title + ', '
            }


            
                output3 += `<div class="demo-card mdl-card mdl-shadow--2dp">
                <div class="mdl-card__title">
                <h2 class="mdl-card__title-text" style="font-weight: bold; font-family: arial">${data[i].sprintName}</h2>
                </div>
                <div class="mdl-card__supporting-text">
                <p style="font-weight: bold">Start date: ${data[i].startDate} <br>End date: ${data[i].endDate} <br>Completed tasks: ${completedTasks}
                <br>In progress tasks: ${inprogressTasks}<br> To do tasks: ${todoTasks}
                 </p>
                </div>
                <div class="mdl-card__menu">
                </div>
            </div>
            <br>`
            
        }
        outputRef3.innerHTML = output3;
}

/**
 * This chunk of code ensures that all the code is run first before showing it to the page
 */
document.addEventListener("DOMContentLoaded", 
    function(){
      let path = window.location.pathname;
      let page = path.split("/").pop();
      if(page =="pastSprints.html" ){
          pastSprints = retrieveLSData(PAST_SPRINTS_KEY)
          if(pastSprints._sprints!=null){
            displayPastSprints(pastSprints._sprints); 
          }
      }
    })










