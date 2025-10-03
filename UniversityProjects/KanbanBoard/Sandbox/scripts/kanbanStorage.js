/**
 * this function is responsible to manage and store the tasks within the running sprint
 *
 * Last modified: 16-10-2022
 */
const TODO_KEY ="currentTodoTaskIndex"
const TODOS_KEY = "todoData"

const INPROGRESS_KEY = "currentInprogressTaskIndex"
const INPROGRESSES_KEY = "inprogressData"

const COMPLETED_KEY = "currentCompletedTaskIndex"
const COMPLETES_KEY = "completedData"// i know bad namings (;-;)

const STATUS_KEY = "statusData"


let inventoryTodo = new Inventory();

let inventoryInprogress = new Inventory();

let inventoryCompleted = new Inventory();

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


if (checkLSData(TODOS_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(TODOS_KEY);
    // Restore data into inventory
    inventoryTodo.fromData(data);
}

if (checkLSData(INPROGRESSES_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(INPROGRESSES_KEY);
    // Restore data into inventory
    inventoryInprogress.fromData(data);
}

if (checkLSData(COMPLETES_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(COMPLETES_KEY);
    // Restore data into inventory
    inventoryCompleted.fromData(data);
}