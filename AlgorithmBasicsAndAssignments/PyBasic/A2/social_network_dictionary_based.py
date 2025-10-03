import datetime
from datetime import date

def make_person(this_id,name,date_of_birth):
    '''
    return a dictionary of a person's identity
    '''
    dict_keys = ["friends","history","id","name","date_of_birth"]
    dict_values = [[],[],this_id,name,date_of_birth]
    combine_dict = dict(zip(dict_keys, dict_values)) #combine them into dict in order 
    return combine_dict


def find_friendX_inY(person_X,person_Y):
    '''
    Finding person_X's id within person_Y's list of friends
    
    Output :
    return the position of person_Y's ID in person_X.list 
    return None if no in the list
    '''
    x_id = person_X['id']
    y_lst = person_Y['friends']
    output = None
    
    for i in range(len(y_lst)):
        if x_id == y_lst[i]:
            output = i
            
    return output

def make_friendship(person_X,person_Y):
    """
    add each other to both friend list
    only if they are not the same person and not inside the other person's friends list
    """
    #to find each others' id index in the list of friends
    x_id_index = find_friendX_inY(person_X,person_Y)
    y_id_index = find_friendX_inY(person_Y,person_X)
    
    #to avoid unreciprocrated friendship and to not include the same person's id
    if x_id_index == None and person_X['id'] != person_Y['id']:
        person_Y['friends'].append (person_X['id'])
    if y_id_index == None and person_X['id'] != person_Y['id']:   
        person_X['friends'].append (person_Y['id'])
    
    return None


def end_friendship(person_X,person_Y):
    """
    remove each other from both friend list
    only if they are inside the their correspondent friends list
    """
    #to find each others' id index in the list of friends
    x_id_index = find_friendX_inY(person_X,person_Y)
    y_id_index = find_friendX_inY(person_Y,person_X)
    
    if x_id_index != None:
        person_Y['friends'].pop (x_id_index)
    if y_id_index != None:   
        person_X['friends'].pop (y_id_index)
    
    return None
    
def birthday_within_X_days_of_Y(person,days,comparison_date):
    '''
    Check if someone's birthday is within 'days' of the 'comparison_date' 
    return True if it is or False if it is not.
    '''
    upper_range = comparison_date + datetime.timedelta(days=days)   #set range to compare
    lower_range = comparison_date - datetime.timedelta(days=days)
    #force dof to the same(?) year
    #since days wont make sense with more than 365/366 days
    dof_format_upper = datetime.date(upper_range.year,person.get("date_of_birth").month,person.get("date_of_birth").day)  
    dof_format_lower = datetime.date(lower_range.year,person.get("date_of_birth").month,person.get("date_of_birth").day)
    return (lower_range <= dof_format_upper <= upper_range) or (lower_range <= dof_format_lower <= upper_range) 


####R2
def add_person(dict_of_people,name,date_of_birth):
    """
    create a person and add to the list in the network
    return the id number of the newly generated person
    """
    #default user id 1
    id_num = 1
    #if people dict is not empty, the next id is the current + 1
    if bool(dict_of_people): 
        id_num = max(dict_of_people.keys()) + 1
    
    dict_of_people.update({id_num: make_person(id_num,name,date_of_birth)})
    
    return id_num

def get_person_by_id (dict_of_people,find_id):
    """
    find the id we looking for inside this dict_of_people or not
    return the person we are looking for if we found them and None if not
    """
    keys_lst = list(dict_of_people.keys())
    output = None
    
    for num in keys_lst:
        if find_id == num:
            output = dict_of_people[find_id]
            
    return output

####R3

def convert_lines_to_friendships(lines):
    """
    convert string into formatted friendships data to store
    return a dictionary of profiles with list of friends depending on the connection from the input
    
    >>people = [
        'Fred,2022-02-01<->Jenny,2004-11-18',
        'Jiang,1942-09-16<->Sasha,1834-02-02',
        'Corey,2015-05-22',
        'Sasha,1834-02-02<->Amir,1981-08-11'
    ]
    >>convert_lines_to_friendships(people)

    output = {
    1: {'friends': [2], 'history': [], 'id': 1, 'name': 'Fred', 'date_of_birth': datetime.date(2022, 2, 1)},
    2: {'friends': [1], 'history': [], 'id': 2, 'name': 'Jenny', 'date_of_birth': datetime.date(2004, 11, 18)}, 
    3: {'friends': [4], 'history': [], 'id': 3, 'name': 'Jiang', 'date_of_birth': datetime.date(1942, 9, 16)}, 
    4: {'friends': [3, 6], 'history': [], 'id': 4, 'name': 'Sasha', 'date_of_birth': datetime.date(1834, 2, 2)}, 
    5: {'friends': [], 'history': [], 'id': 5, 'name': 'Corey', 'date_of_birth': datetime.date(2015, 5, 22)}, 
    6: {'friends': [4], 'history': [], 'id': 6, 'name': 'Amir', 'date_of_birth': datetime.date(1981, 8, 11)}
    }
    """
    included_names = {} #to prevent double profile in the output
    output = {}
    
    for i in range(len(lines)):
        set_of_friends = lines[i].split('<->')
        index = 0
        name_temp = []

        #so it will iterate for the 2 friends or those without friends
        while index < len(set_of_friends):
            
            name_bday = set_of_friends[index].split(',')
            name = name_bday[0]
            bday = date.fromisoformat(name_bday[1])

            #to store the friendships
            name_temp.append(name)

            #if its a new person then it will generate a new profile
            if name not in included_names:
                id_num = add_person(output,name,bday)
                output.update({id_num: make_person(id_num,name,bday)})
                included_names.update({name: id_num})

            #if there is a friendship, then check from the name_temp and call previous function to make friends
            #the included_names has the persons name as key and id_num as values
            if len(name_temp) > 1:
                p1 = included_names[name_temp[0]]
                p2 = included_names[name_temp[1]]
                make_friendship(output[p1],output[p2])
                
            index+=1
        
    return output

####R4
def new_post(content,owner,tagged):
    """
    create a post from owner and share it to tagged friends 
    """
    friend_list = owner['friends']
    share_to = []

    #only share to those who are tagged
    for followers in tagged:
        if followers in friend_list:
            share_to.append(followers)

    return(content, owner['id'],share_to)

####R5
def birthdays_within_a_week_of(person_id,people_dict,comparison):
    """
    return a list of friends of the person(of the person id) who has birthday in the next 7 days
    """
    lst_friends = people_dict[person_id]['friends']
    output = []
    #search in friend list and see who has a birthday soon
    for friends in lst_friends:
        almost_bday = birthday_within_X_days_of_Y(people_dict[friends],7,comparison)
        if almost_bday == True:
            output.append(friends)
    return output

def make_birthday_posts(people_dict,from_person_id,for_people_ids):
    """
    make happy birthday post for those who will have birthday in (for_people_ids)
    """
    output = []
    for upcoming_bday_star in for_people_ids:
        content= f"Happy birthday {people_dict[upcoming_bday_star]['name']} Hope you have a good one!"
        posts = (content,from_person_id,[upcoming_bday_star])
        output.append(posts)
    return output  


if __name__=="__main__":
    people = [
        'Fred,2022-02-01<->Jenny,2004-11-18',
        'Jiang,1942-09-16<->Sasha,1834-02-02',
        'Corey,2015-05-22',
        'Sasha,1834-02-02<->Amir,1981-08-11'
        ]
    convert_lines_to_friendships(people)
    
               
