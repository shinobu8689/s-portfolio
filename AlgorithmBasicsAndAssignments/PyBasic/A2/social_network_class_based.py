import datetime
from datetime import date

class Person:

    #initialise the object Person
    def __init__(self,this_id,name,date_of_birth):
        self.this_id = this_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.friends = []
        self.history = []

    def birthday_within_X_days_of_Y(self,days,comparison_date):
        """
        return boolean: is this person birthday within X days or not
        """
        #set range to compare
        upper_range = comparison_date + datetime.timedelta(days=days)
        lower_range = comparison_date - datetime.timedelta(days=days)
        #force dof to be the same(?) year
        #since days wont make sense with more than 365/366 days
        dof_format_upper = datetime.date(upper_range.year,self.date_of_birth.month,self.date_of_birth.day)
        dof_format_lower = datetime.date(lower_range.year,self.date_of_birth.month,self.date_of_birth.day)
        return (lower_range <= dof_format_upper <= upper_range) or (lower_range <= dof_format_lower <= upper_range)


    def find_my_friend(self, other_person):
        """
        return the position of other_person's ID in self.friends 
        return None if no in the list
        """
        x_id = other_person.this_id
        y_lst = self.friends
        output = None
        for i in range(len(y_lst)):
            if x_id == y_lst[i]:
                output = i
        return output


    def make_friendship(self,other_person):
        """
        add each other to both friend list
        only if they are not the same person and not inside the other person's friends list
        """
        #to find each others' id index in the list of friends
        x_id_index = other_person.find_my_friend(self)
        y_id_index = self.find_my_friend(other_person)
        #to avoid unreciprocrated friendship and to not include the same person's id
        if x_id_index == None and self.this_id != other_person.this_id:
            other_person.friends.append(self.this_id)
        if y_id_index == None and self.this_id != other_person.this_id:   
            self.friends.append(other_person.this_id)


    def end_friendship(self,other_person):
        """
        remove each other to both friend list
        only if they are inside the their correspondent friends list
        """
        #to find each others' id index in the list of friends
        x_id_index = other_person.find_my_friend(self)
        y_id_index = self.find_my_friend(other_person)
        if x_id_index != None:
            other_person.friends.pop(x_id_index)
        if y_id_index != None:   
            self.friends.pop(y_id_index)


    def make_post(self,content,tagged):
        """
        create post for as self w/ content and shared to friends according to their friends id (tagged)
        """
        friend_list = self.friends
        share_to = []
        #only share to those who are inside self.friend
        for follower in tagged:
            share_to.append(follower)        
        self.history.append((content, self.this_id, share_to))

        return (content, self.this_id, share_to)

    #formatted toString
    def __str__(self):
        self.friends = str(self.friends).replace("[","")
        self.friends = str(self.friends).replace("]","")
        return '{self.this_id} ({self.name}, {self.date_of_birth}) --> {self.friends}'.format(self=self)



class SocialNetwork:

    #initialise the Social Network
    def __init__(self,people_friendship_data,post_history):
        self.people = {}
        self.posts = []
        self.convert_lines_to_friendships(people_friendship_data)    


    def add_person(self,name,date_of_birth):
        """
        create a person and add to the list in the network
        """
        #default user id 1
        id_num = 1
        #if people dict is not empty, the next id is the current + 1
        if bool(self.people): 
            id_num = max(self.people) + 1
        self.people.update({id_num: Person(id_num,name,date_of_birth)})
        return id_num

    
    def get_person_by_id(self,find_id):
        """
        find the id we looking for inside this person friend list or not
        """
        keys_lst = list(self.people)
        find_id = int(find_id) 
        output = None
        for num in keys_lst:
            if find_id == num:
                output = self.people[find_id]  
        return output
    

    def convert_lines_to_friendships(self, lines):
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
        
        for i in range(len(lines)):
            set_of_friends = lines[i].split('<->')
            index = 0
            name_temp = []
            #iterate for the 2 friends or those without friends
            while index < len(set_of_friends):   
                name_bday = set_of_friends[index].split(',')
                name = name_bday[0]
                bday = date.fromisoformat(name_bday[1])
                #to store the friendships
                name_temp.append(name)
                #if its a new person then it will generate a new profile
                if name not in included_names:
                    id_num = self.add_person(name,bday)
                    included_names.update({name: id_num})
                #if there is a friendship, then check from the name_temp and call previous function to make friends
                #the included_names has the persons name as key and id_num as values
                if len(name_temp) > 1:
                    p1 = included_names[name_temp[0]]
                    p2 = included_names[name_temp[1]]
                    self.people.get(p1).make_friendship(self.people.get(p2))
                index += 1


    def make_birthday_posts(self,from_person_id,comparison_date):
        """
        post happy birthday to those who will has birthday in the next 7 days
        """
        lst_friends = self.get_person_by_id(from_person_id).friends
        for_people_ids = []
        #search in friend list and see who has a birthday soon
        for friends in lst_friends:
            almost_bday = self.get_person_by_id(friends).birthday_within_X_days_of_Y(7, comparison_date)
            if almost_bday == True:
                for_people_ids.append(friends)


        #create post for those who birthday according to the list created earlier
        for upcoming_bday_star in for_people_ids:
            content= f"Happy birthday {self.get_person_by_id(upcoming_bday_star).name}! Hope you have a good one!"
            
            #check duplicate, post if not
            duplicate = False
            for previous_post in self.get_person_by_id(from_person_id).history:
                if previous_post[0] == content and previous_post[2][0] == upcoming_bday_star:
                    duplicate = True
            if not duplicate:
                self.posts.append(self.get_person_by_id(from_person_id).make_post(content, [upcoming_bday_star]))
    

    #formatted toString
    def __str__(self):
        result = ""
        for person in self.people.items():
            result += str(person[1]) + "\n"
        return result



#for R7 program
if __name__=="__main__":
    people = [
        'Fred,2022-02-01<->Jenny,2004-11-18',
        'Jiang,1942-09-16<->Sasha,1834-02-02',
        'Corey,2015-05-22',
        'Sasha,1834-02-02<->Amir,1981-08-11'
        ]
        
    social_network = SocialNetwork(people,[])
    print(social_network.convert_lines_to_friendships(people))
    
    current_year = date.today().year
    current_running_date = datetime.date(current_year,1,1)

    #go through a year
    while current_running_date < datetime.date(current_year + 1,1,1):
        for i in social_network.people:
            social_network.make_birthday_posts(i,current_running_date)
            current_running_date += datetime.timedelta(days=1)
    #print all the birthday post
    for i in social_network.posts:
        print(i)

