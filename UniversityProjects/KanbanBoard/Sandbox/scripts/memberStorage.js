/**
 * Holds classes and inventory classes for any functionality that relates to management of members
 *
 * Last modified: 16-10-2022
 */

const MEMBER_KEY = "currentMemberIndex"
const MEMBERS_KEY = "membersData"
// key to access item of the memberStorage

class Member {

    //constructor
    constructor(member_name, member_email){
        this.member_name = member_name;
        this.member_email = member_email;
    }

    // setter
    set member_name(new_name){
        this._member_name = new_name;
    }

    set member_email(new_email){
        this._member_email = new_email;
    }
    
    // getter
    get member_name(){
        return this.member_name;
    }

    get member_email(){
        return this.member_email;
    }

    //method
    fromData(data){
        this._member_name = data._member_name;
        this._member_email = data._member_email;
    }
}

//a class to store Member
class InventoryM
{

    //constructor
    constructor(){
        this._memberList = [];
    }

    get memberList(){
        return this._memberList;
    }

    getTotalMembers(){
        return this._memberList.length
    }
    //add category method adds a category to the warehouse
    addMember(memberName, memberEmail){
        let member = {
            member_name: memberName,
            member_email: memberEmail
        };
        this._memberList.push(member);
        console.log(this.getTotalMembers)
        }
    
    //add item method adds items inside the category
    
    getMember(memberIndex){
        return this._memberList[memberIndex];
    }

    fromData(data){
        this._memberList = [];
        for ( let i = 0; i < data._memberList.length ; i++ ){
            let member = {
                member_name: data._memberList[i].member_name,
                member_email: data._memberList[i].member_email
            };
            this._memberList.push(member);
        }
    }
}

let m_inventory = new InventoryM();


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


if (checkLSData(MEMBERS_KEY))
{
    // If data exists, retrieve it
    let data = retrieveLSData(MEMBERS_KEY);
    // Restore data into inventory
    m_inventory.fromData(data);
}
