/**
 * This file contains the methods directly related to the time tracking, and storage of the user input time
 * tracking data.
 *
 * Last modified: 17-10-2022
 */

const TIME_KEY = "currentTimeIndex"
const TIME_DATA_KEY = "timeData"

/**
 * This class will be used to record the details each time a user tracks time for one of the in-progress tasks.
 * @param {number} time - The amount of time logged by the user in hours
 * @param {string} teamMember - The name of the team member that logged the time
 */
class TimeLog{
    constructor(time, teamMember) {
        this.time = time;
        this.date = Date.now()      // Uses the date built-in to create a date object for the current date
        this.teammember = teamMember;
    }

    getTime(){return this.time;}
    getDate(){return this.date;}
    getTeamMember(){return this.teammember;}
}

/**
 * This class stores all instances of the timeLog class and contains the revelant methods to get and store the data/
 */
class TimeInventory
{
    constructor(){
        this._timeTracked = [];
    }

    getTimeTracked(){ return this._timeTracked };

    addTimeLog(timeInput, teamMember){
        let timeLogged = new TimeLog(timeInput, teamMember)
        this._timeTracked.push(timeLogged);
    }

    popTime(){
        this._timeTracked.pop();
    }

    getTotalTimeTracked(){
        let totalTime = 0

        for (let x in this.getTimeTracked()) {
            totalTime += this.getTimeTracked()[x].time;
        }
        return totalTime
    }

    fromData(data){
        this._memberList = [];
        for (let i = 0; i < data._timeTracked.length ; i++){
            let timeLog = {
                time: data._timeTracked[i].time,
                date: data._timeTracked[i].date,
                teammember: data._timeTracked[i].teammember,
            };
            this._timeTracked.push(timeLog)
        }
    }

}

let timeInventory = new TimeInventory();


// Functions for calculating the average time over a date range

/**
 * Increments the input date by the specified number of days then returns the new date object
 * @param dateInput Date object for the date to be incremented
 * @param increment The amount of days that the date should be incremented by
 * @returns {Date} The new date object for the incremented date
 */
function incrementDate(dateInput, increment) {
    let dateFormatTotime = new Date(dateInput);
    let increasedDate = new Date(dateFormatTotime.getTime() + (increment * 86400000));
    return increasedDate;
}

/**
 * This function check if the two input dates are on the same date regardless of time
 * @param date1
 * @param date2
 * @returns {boolean} True if they are equiliven, otherwise false
 */
function equalDateCheck(date1, date2){
    return date1.toDateString() === date2.toDateString();
}

/**
 * This function return the amount of days differences between the two input dates using date object methods
 * @param date1
 * @param date2
 * @returns {number} Difference amount of days
 */
function dateDiff(date1, date2){
  
    let timeDiff = (date2 - date1)/24/60/60/1000;
    return Math.floor(timeDiff)
}

/**
 * Checks that the user input dates are valid, if not alerts the user, otherwise calculates the average time recorded
 * per person per day for all team members within the user specified date range.
 */
function averageTime(){

    // Getting user input dates and converting to date objects
    let startDateStr = document.getElementById("team-avg-start").value    // yyyy-mm-dd
    let endDateStr = document.getElementById("team-avg-end").value        // dd/mm/yyyy

    if (startDateStr === "" || endDateStr === "") {
        alert("Please enter the desired dates");
        return 1
    }

    let st_year = startDateStr.substring(0,4);
    let st_month = startDateStr.substring(5,7);
    let st_date = startDateStr.substring(8,10);
    let end_year = endDateStr.substring(0,4);
    let end_month = endDateStr.substring(5,7);
    let end_date = endDateStr.substring(8,10);

    if (parseInt(st_month) < 0 || parseInt(st_month) > 11) {
        alert("Please enter valid dates")
        return 1
    } else if (parseInt(end_month) < 0 || parseInt(end_month) > 11) {
        alert("Please enter valid dates")
        return 1
    } else if (parseInt(st_date) <= 0 || parseInt(st_date) > 31) {
        alert("Please enter valid dates")
        return 1
    } else if (parseInt(end_date) <= 0 || parseInt(end_date) > 31) {
        alert("Please enter valid dates")
        return 1
    }

    let startDate, endDate;

    try {
        startDate = new Date(st_year, st_month, st_date)
        endDate = new Date(end_year, end_month, end_date)
    } catch (e) {
        alert("Please enter valid dates")
        return 1
    }

    if (dateDiff(startDate, endDate) < 0){
        alert("The end date must be after the start date")
        return 1
    }

    let totalTime = 0; // The total time within the specified date range


    for(let x = 0; x < timeInventory.getTimeTracked().length; x++){
        let num = timeInventory.getTimeTracked()[x].date;
        let timeinvdate = new Date(num);
        if (dateDiff(timeInventory.getTimeTracked()[x].date, startDate.getTime()) >= 0 && dateDiff(startDate.getTime(), timeInventory.getTimeTracked()[x].date) <= dateDiff(startDate, endDate)){
            totalTime += timeInventory.getTimeTracked()[x].time;
        } else {
        }
    }

    let avgTime;
    if (dateDiff(startDate,endDate)===0){
        avgTime = totalTime/m_inventory.getTotalMembers();
    } else {
        avgTime = totalTime/m_inventory.getTotalMembers()/(dateDiff(startDate,endDate) + 1);
    }

    let roundedAvgTime = Math.round(avgTime * 100) / 100
    alert("The average time tracked is: " + roundedAvgTime);
}




// FIXME: Local storage functions for time tracking
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

if (checkLSData(TIME_DATA_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(TIME_DATA_KEY);
    // Restore data into inventory
    timeInventory.fromData(data);
}
