import datetime
from datetime import date

class Person:

    #initialise the object Person
    def __init__(self,this_id,name,date_of_birth):#bulid the constructor 
        self.this_id = this_id#initialize the attributes
        self.name = name
        self.date_of_birth = date_of_birth
        self.friends = [] #empty lists
        self.history = []
        self.followers = []

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


    def find_my_friend(self, other_person, is_friend):
        """
        return the position of other_person's ID in self.friends 
        return None if not in the list
        """
        x_id = other_person.this_id
        if is_friend == True:
            y_lst = self.friends
        else:
            y_lst = self.followers

        output = None
        for i in range(len(y_lst)):
            if x_id == y_lst[i]:
                output = i
        return output
    

    def make_relationship(self,other_person, is_friend):
        """
        add each other to both friend list
        only if they are not the same person and not inside the other person's friends list
        """
        #to find each others' id index in the list of friends
        x_id_index = other_person.find_my_friend(self,is_friend)
        y_id_index = self.find_my_friend(other_person,is_friend)
        #to avoid unreciprocrated friendship and to not include the same person's id
        mine = []
        others = []
        if is_friend == True:
            others = other_person.friends
            mine = self.friends
        elif is_friend == False:
            #others = other_person.followers
            mine = self.followers
        
        if x_id_index == None and self.this_id != other_person.this_id:
            others.append(self.this_id)
        if y_id_index == None and self.this_id != other_person.this_id:   
            mine.append(other_person.this_id)


    def end_relationship(self,other_person, is_friend):
        """
        remove each other to both friend list
        only if they are inside the their correspondent friends list
        """
        #to find each others' id index in the list of friends
        x_id_index = other_person.find_my_friend(self,is_friend)
        y_id_index = self.find_my_friend(other_person,is_friend)

        if is_friend == True:
            others = other_person.friends
            mine = self.friends
        else:
            others = other_person.followers
            mine = self.followers

        if x_id_index != None:
            others.pop(x_id_index)
        if y_id_index != None:   
            mine.pop(y_id_index)


    def make_threaded_post(self,content,tagged,is_private):
        """
        determine whether friends or followers can comment on different situation
        """
        can_comment = []
        #friends can comment if private
        if is_private == True:
            for tag in tagged:
                print(self.friends)
                if tag in self.friends:
                    can_comment.append(tag)

        #if public, followers can comment too
        elif is_private == False:
            for tag in tagged:
                if tag in self.friends or tag in self.followers:
                    can_comment.append(tag)
    
        return (content, self.this_id, can_comment,is_private,[])


    #formatted toString
    def __str__(self):
        """convert the output into a string"""
        return '{self.this_id} ({self.name}, {self.date_of_birth}) --> Fr{self.friends} ==> Fo{self.followers}'.format(self=self)


class SocialNetworkWithFollowers:
   #initialise the Social Network
    def __init__(self,people_friendship_data,post_history):#bulid the constructor
        self.posts = []
        self.people = {}#people attribute as an empty dictionary
        self.convert_lines_to_friendships(people_friendship_data)  

    def add_person(self,name,date_of_birth):
        """
        create a person and add to the list in the network
        """
        #default user id 1
        id_num = 1
        #if people dict is not empty, the next id is the current + 1
        if bool(self.people): 
            id_num = max(self.people.keys()) + 1
        self.people.update({id_num: Person(id_num,name,date_of_birth)})
        return id_num

    def convert_lines_to_friendships(self,lines):
        """
        convert string into formatted friendships or followers data to store
        """
        included_names = {} #to prevent double profile in the output
        status = ''
        
        for i in range(len(lines)):
            if '<->' in lines[i]:
                set_of_friends = lines[i].split('<->')
                status = 'friends'
            elif '-->' in lines[i]:
                set_of_friends = lines[i].split('-->')
                status = 'following'
            elif '<--' in lines[i]:
                set_of_friends = lines[i].split('<--')
                status = 'followed by'

            #if they dont have friends or followers
            else:
                set_of_friends = [lines[i]]
            
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
                if len(name_temp) > 1 and status == 'friends':
                    p1 = included_names[name_temp[0]]
                    p2 = included_names[name_temp[1]]
                    print(self.people)
                    self.people[p1].make_relationship(self.people[p2],True)

                elif len(name_temp) > 1 and status == 'following':
                    p1 = included_names[name_temp[0]]
                    p2 = included_names[name_temp[1]]
                    #print(lines[p1])
                    self.people[p1].make_relationship(self.people[p2],False)

                elif len(name_temp) > 1 and status == 'followed by':
                    p1 = included_names[name_temp[0]]
                    p2 = included_names[name_temp[1]]
                    self.people[p2].make_relationship(self.people[p1],False)
            
                index += 1

    #formatted toString
    def __str__(self):
        """convert the return into strings"""
        result = ""
        for person in self.people.items():
            result += str(person[1]) + "\n"
        return result

def get_person_by_id (dict_of_people,find_id):
    
    keys_lst = list(dict_of_people.keys())
    output = None
    
    for num in keys_lst:
        if find_id == num:
            output = dict_of_people[find_id]
            
    return output

def add_child(threaded_post, content, new_post_owner,tagged, is_private):
        """
        add a new threaded_post into the children of the threaded_post given as argument
        """
        source, old_id, can_comment,privacy,child_post = threaded_post
        post = Person.make_threaded_post(new_post_owner,content,tagged,is_private)
        child_post.append(post)
        social_network.people[old_id].history.append(threaded_post)
    

    
if __name__=="__main__":
    
    line = ['Fred,2022-02-01<--Jenny,2004-11-18',
        'Jiang,1942-09-16-->Sasha,1834-02-02',
        'Corey,2015-05-22',
        'Sasha,1834-02-02<->Amir,1981-08-11']

    network = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<--D,2000-01-04',
            'E,2000-01-05-->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01-->C,2000-01-03',
            'B,2000-01-02<--D,2000-01-04',
            'B,2000-01-02<--F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
            'D,2000-01-04<->E,2000-01-05',
            'G,2000-01-07-->D,2000-01-04'
        ]
    
    social_network = SocialNetworkWithFollowers(line,[])

    person = Person(1,'con',current_running_date)
    #social_network.convert_lines_to_friendships(line)
    '''
    print(social_network)
    print(social_network.people[1].make_threaded_post("hello @Jenny!",[2],True))
    print(social_network.people[2].make_threaded_post("hello @Fred!",[1],True))
    print(social_network.people[4].make_threaded_post("hello @Amir!",[6],True))
    '''
    source = social_network.people[4].make_threaded_post("hello @Amir!",[6],False)
    #print(source)
    #add_child(threaded_post, content, new_post_owner, tagged, is_private)
    add_child(source,'shh I am busy!!!',social_network.people[6],[],True)
    #print(social_network.people[4].history)
    [('hello @Amir!', 4, [6], True, [('shh I am busy!!!', 6, [], True, [])])]
    social_network.convert_lines_to_friendships(line)
    #.get_person_by_id(4).make_threaded_post("source",[],False))
    #print(network.people.get_person_by_id(4).make_threaded_post("source1",[],False))
    print(social_network)

    
if __name__=="__main__":
    
    line = ['Fred,2022-02-01<--Jenny,2004-11-18',
        'Jiang,1942-09-16-->Sasha,1834-02-02',
        'Corey,2015-05-22',
        'Sasha,1834-02-02<->Amir,1981-08-11']

    network = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<--D,2000-01-04',
            'E,2000-01-05-->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01-->C,2000-01-03',
            'B,2000-01-02<--D,2000-01-04',
            'B,2000-01-02<--F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
            'D,2000-01-04<->E,2000-01-05',
            'G,2000-01-07-->D,2000-01-04'
        ]
    
    social_network = SocialNetworkWithFollowers(line,[])
    current_year = date.today().year
    current_running_date = datetime.date(current_year,1,1)

    person = Person(1,'con',current_running_date)
    #social_network.convert_lines_to_friendships(line)
    '''
    print(social_network)
    print(social_network.people[1].make_threaded_post("hello @Jenny!",[2],True))
    print(social_network.people[2].make_threaded_post("hello @Fred!",[1],True))
    print(social_network.people[4].make_threaded_post("hello @Amir!",[6],True))
    '''
    source = social_network.people[4].make_threaded_post("hello @Amir!",[6],False)
    #print(source)
    #add_child(threaded_post, content, new_post_owner, tagged, is_private)
    add_child(source,'shh I am busy!!!',social_network.people[6],[],True)
    #print(social_network.people[4].history)
    [('hello @Amir!', 4, [6], True, [('shh I am busy!!!', 6, [], True, [])])]
    social_network.convert_lines_to_friendships(line)
    #.get_person_by_id(4).make_threaded_post("source",[],False))
    #print(network.people.get_person_by_id(4).make_threaded_post("source1",[],False))
    print(social_network)


#python3 Alvina/test_social_network_class_with_followers.py
#python3 Alvina/social_network_class_with_followers.py
    


