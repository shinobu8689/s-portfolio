/**
 * Functions for the team member functionality for interacting to with the page and backlog
 *
 * Last modified: 12-10-2022
 */


// for button move to add new member page
function openMemberPopUp(){
    window.location = "newMemberPopup.html"
}

// for button move to edit member page
function openMemberEditPopup(i){
    updateLSData(MEMBER_KEY, i);
    window.location = "editMemberPopup.html"  
}

// create member from the popup prompt page
function createMember(){
    let memberName =  document.getElementById("member_name").value;
    let memberEmail = document.getElementById("member_email").value;
    let timeTracked = [];

    if (memberName == "" | memberEmail == ""){ // field must not be empty
        alert("Some fields are empty");
    } else {
        let member = new Member(memberName, memberEmail)    // create the member, update the local storage, and return to the member page
        m_inventory.addMember(member);
        updateLSData(MEMBERS_KEY, m_inventory);
        window.location = "memberPage.html"
    } 
}

// for button return to memberpage
function cancel(){
    window.location = "memberPage.html"
}

// for comfirming when deleting a member
function deleteMemberConfirm(index){
    let text = "Are you sure to delete "+ m_inventory.getMember(index).member_name._member_name +" from the member list?";
    if (confirm(text)){
        removeMember(index)
    }
}

// actually delete the member and update LS
function removeMember(index) {
    m_inventory._memberList.splice(index,1);
    updateLSData(MEMBERS_KEY, m_inventory);
    window.location = "memberPage.html"
}
  
// for button editing member
function editMember() {
    let text = "Are you sure to edit?";     // confirm pop-up, proceed when yes
    if (confirm(text)){
        index = retrieveLSData(MEMBER_KEY);
        m_inventory._memberList.splice(index,1);
        createMember();
    } 
}


// generate the dropdown list depends on the member list to choose from
function getMember(){
    var select = document.getElementById("task_assignee");
    var options = [];
    
    for (let i = 0; i < m_inventory.memberList.length; i++){
        options.push(m_inventory.getMember(i).member_name._member_name);
    }

    for(var i = 0; i < options.length; i++) {
        var opt = options[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    }
}

// get the attribute to fill the editing page to edit
function presetAttribute(){
    data = m_inventory;
    index = retrieveLSData(MEMBER_KEY);

    document.getElementById("member_name").setAttribute('value',data.getMember(index).member_name._member_name);
    document.getElementById("member_email").setAttribute('value',data.getMember(index).member_name._member_email);
}

// display the member in listed card form
function display(data)
{
    let outputRef1 = document.getElementById("member_list");
    let output1 = "";
    
    for (let i = 0; i < data.memberList.length; i++) {
            output1 += `<div class="demo-card mdl-card mdl-shadow--2dp">
            <div class="mdl-card__title">
            <h2 class="mdl-card__title-text" style="font-weight: bold; font-family: arial">${data.getMember(i).member_name._member_name}</h2>
            </div>
            <div class="mdl-card__supporting-text">
            <p style="font-weight: bold">EMAIL: ${data.getMember(i).member_name._member_email}</p>
            </div>
            
            <div class="mdl-card__menu">
            <button onclick="openMemberEditPopup(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                <i class="material-icons">edit square</i>
            </button>
            <button onclick="deleteMemberConfirm(${i})" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                <i class="material-icons">delete square</i>
            </button>
            </div>
            
        </div>
        <br>`
    }

    outputRef1.innerHTML = output1;

}

// to set the assignee to when sprint started
function setMember(){
    index = retrieveLSData(TASK_KEY);

    let task = inventoryTodo.getTask(index)
    task.title._name = document.getElementById("task_assignee").value
    
    updateLSData(TODOS_KEY,inventoryTodo)
    window.location = "kanbanBoard.html"
}


display(m_inventory);