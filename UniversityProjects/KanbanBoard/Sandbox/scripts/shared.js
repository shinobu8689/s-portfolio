/**
 * This file contains the task class that is instantiated each time the user creates a new task, the inventory class
 * that contains all the instances of the tasks, and some functions that are used to retrieve and store the task data
 * from the users local storage.
 *
 * Last modified: 17-10-2022
 */
const TASK_KEY = "currentTaskIndex"
const TASKS_KEY = "tasksData"

/***
 * This class is used to create objects for the individual tasks that will be created from the users input.
 *
 */
class Task {
    constructor(taskName, assignee, tag, type, priority, storyPoint, description){
        this.title = taskName;
        this.assignee = assignee;
        this.tag = tag;
        this.type = type;
        this.priority = priority;
        this.storyPoint = storyPoint;
        this.taskStatus = "not started";
        this.timeSpent = 0;
        this.description = description;
        this.timeCompleted = null;
    }

    set title(newTitle){
        this._title = newTitle;
    }

    set assignee(newName){
        this._name = newName;
    }

    set tag(newTag){
        this._tag = newTag;
    }

    set type(newType){
        this._type = newType;
    }

    set priority(newPriority){
        this._priority = newPriority;
    }

    set storyPoint(newStoryPoint){
        this._storyPoint = newStoryPoint;
    }

    set taskStatus(newStatus){
        this._taskStatus = newStatus;
    }

    set member(newMember){
        this._member = newMember;
    }

    set description(newDescription){
        this._description = newDescription;
    }

    set timeSpent(newTime){
        this._timeSpent = newTime;
    }

    set timeCompleted(newTime){
        this._timeCompleted = newTime;
    }

    get title (){
        return this.title;
    }

    get getName (){
        return this.assignee;
    }

    get tag(){
        return this.tag;
    }

    get type(){
        return this.type;
    }

    get priority(){
        return this.priority;
    }

    get storyPoint(){
        return this.storyPoint;
    }

    get description(){
        return this.description;
    }

    get timeSpent(){
        return this.timeSpent;
    }

    get timeCompleted(){
        return this.timeCompleted;
    }

    fromData(data){
        this._title = data._title;
        this._name = data._name;
        this._tag = tag;
        this._type = data._type;
        this._priority = data._priority;
        this._storyPoint = data._storyPoint;
        this._description = data._description;
        this._timeSpent = data._timeSpent;
    }
}

/***
 * This class stores all the instances of the task class.
 *
 */
class Inventory
{
    constructor(){
        this._tasks = [];
    }
    get tasks(){return this._tasks};

    // Add category method adds a category to the warehouse
    addTask(titleName, nameName, tagName, typeName, priorityName, storyPointName, descriptionName){
        let task = {
            title: titleName,
            name: nameName,
            tag:tagName,
            type:typeName,
            priority : priorityName,
            storyPoint : storyPointName,
            description : descriptionName
                };
        this._tasks.push(task);
        }
    
    //add item method adds items inside the category
    
	popTask(){
        this.tasks.pop();
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

// @FIXME: 47 line duplicated code matches with kanbanStorage.js
let inventory = new Inventory();


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


if (checkLSData(TASKS_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(TASKS_KEY);
    // Restore data into inventory
    inventory.fromData(data);
}
