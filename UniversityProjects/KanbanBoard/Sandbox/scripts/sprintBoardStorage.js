/**
 * This file contains storage for tasks in the sprint board of the product backlog
 *
 * Last modified: 17-10-2022
 */

const SPRINT_KEY ="currentSprintTaskIndex"
const SPRINTS_KEY = "sprintData"


class InventoryS{
    //constructor
    constructor(){
        this._tasks = [];
    }
    //accessor
    get tasks(){return this._tasks};
    
    addTask(task){
        this._tasks.push(task);
    }
    
    getTask(taskIndex){
        return this._tasks[taskIndex];
    }
    fromData(data){
        this._tasks = [];
        for ( let i = 0; i <data._tasks.length ; i++){
            let task = {
                title:data._tasks[i].title,
                name: data._tasks[i].name,
                tag:data._tasks[i].tag,
                type:data._tasks[i].type,
                priority:data._tasks[i].priority,
                storyPoint:data._tasks[i].storyPoint,
                description:data._tasks[i].description
            };
            
            this._tasks.push(task);
        }
    }
} 

let inventoryS = new Inventory();


/**
 * checkLSData function
 * Used to check if any data in LS exists at a specific key
 * @param {string} key LS Key to be used
 * @returns true or false representing if data exists at key in LS
 */
 function checkLSData(key)
 {
     if (localStorage.getItem(key) != null)
     {
         return true;
     }
     return false;
 }
 /**
  * retrieveLSData function
  * Used to retrieve data from LS at a specific key. 
  * @param {string} key LS Key to be used
  * @returns data from LS in JS format
  */
 function retrieveLSData(key)
 {
     let data = localStorage.getItem(key);
     try
     {
         data = JSON.parse(data);
     }
     catch(err){}
     finally
     {
         return data;
     }
 }
 /**
  * updateLSData function
  * Used to store JS data in LS at a specific key
  * @param {string} key LS key to be used
  * @param {any} data data to be stored
  */
 function updateLSData(key, data)
 {
     let json = JSON.stringify(data); 
     localStorage.setItem(key, json);
 }


if (checkLSData(SPRINTS_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(SPRINTS_KEY);
    // Restore data into inventory
    inventoryS.fromData(data);
}