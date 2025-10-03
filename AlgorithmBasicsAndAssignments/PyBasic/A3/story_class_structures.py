'''
Group plz input team name

Alvina Florence
Mingru Qin
Yansen Gunawan Tjeng
Yin Lam lo

Contains class: Story, Scene, Character

python3 story_class_structures.py
python3 test_character_class.py
python3 test_choose_your_own_adventure.py   
python3 test_make_check_function.py
python3 test_story_bestchar.py
python3 test_story_class.py
'''
import random, re

class Character:
    '''
    Character represents an individual character as previously defined in the supporting information
    by Yin Lam Lo
    ver. 16/5/2022

    attribute:
        name    (str)
        acumen  (int)
        body    (int)
        charm   (int)
        skill   (str)

    method:
        __init__(self,string_input)
        check_status(self,status_string)
        check_skill(self,skill_string)
        get_acumen(self)
        get_body(self)
        get_charm(self)
        get_name(self)
        get_proficient(self)
        make_check(self,skill_or_attribute_name,difficulty,override_random)
        __str__(self)
    '''

    def __init__(self,string_input):
        '''
        the constructor
        param: string_input (list)
        '''
        self.name = string_input[0]
        self.check_status(string_input[1])
        self.check_skill(string_input[2])

    def check_status(self,status_string):
        '''
        check status string and check correctness from string_input[1]
        and assign value to obj itself

        param: status_string (str)
        return: None
        '''
        status_type = ["acumen","body","charm"]
        status_value = []
        status_list = status_string.split(" ") # get the 3 values
        for i in status_list:
            status_value.append(int(i[1:])) # remove the Alphabet and add to correspondence slot in status_value

        # validation
        try:
            assert sum(status_value) == 7
        except:
            raise ValueError(status_string + " is invalid, sum of attributes does not equal 7")

        for i in range(len(status_value)):
            try:
                assert status_value[i] >= 1 and status_value[i] <= 4 
            except:
                raise ValueError("invalid value for " + status_type[i] + "; " + str(status_value[i]) + " is not in the range 1 to 4")

        # store to obj attribute when passed
        self.acumen = status_value[0]
        self.body = status_value[1]
        self.charm = status_value[2]

    def check_skill(self,skill_string):
        '''
        check skill string and check correctness from string_input[2]
        and assign value to obj itself

        param: skill_string (str)
        return: None
        '''
        # skill info
        approved_skill_list = ["Di","In","Me","La","Ac","Cr"]
        skill_list_full = ["diplomacy","investigation","medicine","language","acrobatics","craft"]

        # validation
        try:
            assert skill_string.count('*') == 1
        except :
            raise ValueError(skill_string + " is invalid; exactly one proficiency asterisk expected")

        skill_list = skill_string.split(" ")

        try:
            for i in skill_list:
                assert i[:2] in approved_skill_list
                if "*" in i: # set proficient skill if pass
                    self.skill = skill_list_full[skill_list.index(i)]
                    break
        except:
            raise ValueError(skill_string + " is invalid; unexpected skill name given")

    # getters
    def get_acumen(self):
        return self.acumen

    def get_body(self):
        return self.body
    
    def get_charm(self):
        return self.charm

    def get_name(self):
        return self.name

    def get_proficient(self):
        return self.skill

    def make_check(self,skill_or_attribute_name,difficulty,override_random):
        '''
        check attribute condition determine result

        param: skill_or_attribute_name (str), difficulty (str), override_random (int)
        return: difficulty symbol
        '''
        value = random.randint(-1,1)
        if override_random != None:
            value = override_random
        char_value = None
        if skill_or_attribute_name == "diplomacy" or skill_or_attribute_name == "language" or skill_or_attribute_name == "charm":
            char_value = self.get_charm()
        elif skill_or_attribute_name == "investigation" or skill_or_attribute_name == "medicine" or skill_or_attribute_name == "acumen":
            char_value = self.get_acumen()
        elif skill_or_attribute_name == "acrobatics" or skill_or_attribute_name == "craft" or skill_or_attribute_name == "body":
            char_value = self.get_body()
        #print("char_value:",char_value , "diff:", difficulty)
        
        char_value += value

        #if the skill is specialty then add 2 to the char_value
        if self.skill == skill_or_attribute_name:
            char_value += 2

        difficulty = int(difficulty)
        #print("char_value:",char_value , "(" + str(value) + ")", "diff:", difficulty)
        
        if char_value >= difficulty + 3:
            return "++"
        elif char_value >= difficulty:
            return "+"
        elif char_value <= difficulty - 4:
            return "--"
        elif char_value < difficulty:
            return "-"

    def __str__(self):
        '''
        param: 
        return: formatted string
        '''
        return "{} [A{} B{} C{}] is proficient in {}".format(self.name, self.acumen, self.body, self.charm, self.skill)



class Scene:
    '''
    object scene for better program design
    by Yin Lam Lo
    ver. 16/5/2022

    attribute:
        scene_id        (int)
        scene_content   (int)
        option_spec     (2d list) [[option_id (str),skill_str (str),skill_difficulty(str),next_scene (str) ......],[next_option]....]
        option_text     (list) ["text for option 1","text for option 2",.....]
        
    method:
        __init__(self,scene_id,scene_content,option_spec,option_text)
        get_scene_id(self)
        get_scene_content(self)
        get_option_spec(self)
        get_option_text(self)
    '''
    def __init__(self,scene_id,scene_content,option_spec,option_text):
        '''
        the constructor
        param: scene_id (str), scene_content (str), option_spec (list), option_text (list)
        '''
        self.scene_id = scene_id
        self.scene_content = scene_content
        self.option_spec = option_spec
        self.option_text = option_text

    # getter
    def get_scene_id(self):
        return self.scene_id

    def get_scene_content(self):
        return self.scene_content

    def get_option_spec(self):
        return self.option_spec

    def get_option_text(self):
        return self.option_text


class Story:
    '''
    Represents the story containing all the data of relevant scenes, options and characters appropriate.
    It keeps track of the current scene and allows the choosing of options to progress to the next scene
    by Yin Lam Lo
    ver. 17/5/2022

    attribute:
        scene_string_data
        characters_in_story
    method:
    __init__(self,scene_string_data,characters_in_story)
    char_string_to_list(self)
    scene_string_to_list(self)
    get_scene_id(self)
    show_current_scene(self)
    search_scene(self,search_id)
    new_decision(self,out,decision)
    find_next_scene(self,index,selected_option,decision)
    select_option(self,option_number,override)
    symbol_to_grade(self,symbol)
    sort_outcome(self,lst)
    __str__(self)
    '''

    def __init__(self,scene_string_data,characters_in_story):
        '''
        the constructor
        param: scene_string_data (list), characters_in_story (list)
        '''
        self.characters_in_story = characters_in_story
        self.scene_string_data = scene_string_data
        self.current_scene = "S"
        self.char_list = []
        self.scene_list = []
        self.char_string_to_list()
        self.scene_string_to_list()

    def char_string_to_list(self):
        '''
        turn self.characters_in_story store into self.char_list
        '''
        chars_process = self.characters_in_story 
        times_to_loop = chars_process.count("----") + 1
        for i in range(times_to_loop):
            self.char_list.append(Character(chars_process[0:3]))
            chars_process = chars_process[4:]
    
    def scene_string_to_list(self):
        '''
        turn self.scene_string_data store into self.scene_list
        '''
        scene_process = self.scene_string_data
        scene_amount = scene_process.count("====")
        for scene_count in range(scene_amount): # store scene obj into scene_list
            # seat area for a scene
            upper = scene_process.index("----")
            lower = scene_process.index("----",upper+1)
            one_scene = scene_process[upper:lower+1] # extract one scene
            
            scene_process = scene_process[lower+1:] # remove the one currently processing from the remaining scene
            scene_id = one_scene[1]
            option_spliter = one_scene.index("====")
            scene_content = one_scene[2:option_spliter]
            one_option = one_scene[option_spliter+1:-1] # option only from one_scene
            option_spec = []
            option_content = []
            for i in range(len(one_option)): # seperate option_spec for operation, and option_content for display
                inner_option = []
                inner_option_content = []
                one_option[i] = one_option[i].split()
                for j in one_option[i]:
                    if "." in j or "[" in j or "]" in j or "+" in j or "-" in j:
                        inner_option.append(j.replace("[","").replace("]","").replace(".",""))
                    else:
                        inner_option_content.append(j)
                inner_option_content = " ".join(inner_option_content) 
                # append result
                option_content.append(inner_option_content)
                option_spec.append(inner_option)
            for i in range(len(option_spec)): # sort next scene by difficulty
                if option_spec[i][1].isalpha(): # for 2 types for format, one with skill, one without
                    option_spec[i] = option_spec[i][0:3] + self.sort_outcome(option_spec[i][3:])
                else:
                    option_spec[i] = option_spec[i][0:1] + self.sort_outcome(option_spec[i][1:])
            # one scene done
            self.scene_list.append(Scene(scene_id,scene_content,option_spec,option_content))

    def get_scene_id(self):
        return self.current_scene

    def show_current_scene(self):
        '''
        determine what to show depending on current screen
        constructing the string
        '''
        if self.current_scene == "the game is over":
            raise StopIteration("the game is over")
        base_string = ""
        base_string += "Scene " + self.get_scene_id() + "\n"
        scene = self.search_scene(self.get_scene_id())
        for i in scene.get_scene_content():
            base_string += i + "\n"   
        base_string += "====\n"
        for i,k in enumerate(scene.get_option_text()):
            base_string += ("{}. {}".format(i+1,k)) + "\n"
        base_string += "----"
        
        return base_string

    def search_scene(self,search_id):
        '''
        param: search_id (int)
        return: scene obj with the search_id
        '''
        for scene in self.scene_list:
            if scene.get_scene_id() == search_id:
                return scene

    def new_decision(self,out,decision):
        if decision == "++":
            decision = "+"
        elif decision == "--":
            decision = "-"
        elif decision == "-":
            decision = "--"
        return decision
    
    def find_next_scene(self,index,selected_option,decision):
        out = None
        if index == 3:
            for i in selected_option[index:]: #find next scene in result
                if self.symbol_to_grade(re.sub('[^+-]',"",i)) == self.symbol_to_grade(decision):
                    out = re.sub('[+-]',"",i)

        if index == 1:
            lowest = "++"
            for i in selected_option[1:]: # pick the lowest possible
                if self.symbol_to_grade(re.sub('[^+-]',"",i)) < self.symbol_to_grade(lowest):
                    out = re.sub('[+-]',"",i)

        if out == None:
            decision = self.new_decision(out,decision)
            out = self.find_next_scene(index,selected_option,decision)
        return out
    
    
    def select_option(self,option_number,override):
        '''
        proceed to next scene
        param: option_number (int), override (int)
        '''
        if "E" in self.current_scene: # there is no next scene if arrived at ending
            self.current_scene = "the game is over"
            return

        option_spec = self.search_scene(self.get_scene_id()).get_option_spec()

        selected_option = None
        for i in option_spec: # get the selected option
            if i[0] == str(option_number):
                selected_option = i
                break
        
        if selected_option[1].isalpha(): # if the option required skill
            if override != None:
                decision = self.char_list[0].make_check(selected_option[1],selected_option[2],override) # generate consequences

            index_with_skill = 3
            out = self.find_next_scene(index_with_skill,selected_option,decision)
            
        else: # if option no skill required
            index_without_skill = 1
            out = self.find_next_scene(index_without_skill,selected_option,None)
        
        #set next scene
        self.current_scene = out

    def symbol_to_grade(self,symbol):
        '''
        turn symbol to int for easier comparison
        param: symbol (str)
        return: int
        '''
        if symbol == "++":
            return 4
        elif symbol == "+":
            return 3
        elif symbol == "-":
            return 2
        elif symbol == "--":
            return 1

    def sort_outcome(self,lst):
        '''
        sort() won't work in this case, custom made sorting
        param: lst (list)
        return: sorted list according to consequences level
        '''
        grade = [None] * 4
        for i in lst:
            if "++" in i :
                grade[0] = i
            elif "+" in i:
                grade[1] = i
            elif "--" in i:
                grade[3] = i
            elif "-" in i:
                grade[2] = i
        out = []
        for i in grade:
            if i != None:
                out.append(i)
        return out

    def __str__(self):
        '''
        param: 
        return: formatted string
        '''
        base_string = ""
        base_string += "CHARACTERS\n"
        for i in self.char_list:
            base_string += str(i) + "\n"
        base_string += "SCENES\n"
        
        for scene in self.scene_list:
            base_string += scene.get_scene_id() + " >"
            for option_pack in scene.get_option_spec():
                if option_pack[1].isalpha():
                    base_string += " [{}. {}{} {}]".format(option_pack[0],option_pack[1],option_pack[2]," ".join(option_pack[3:]))
                else:
                    base_string += " [{}. {}]".format(option_pack[0]," ".join(option_pack[1:]))
            if self.scene_list.index(scene)+1 != len(self.scene_list):
                base_string += "\n"
        return base_string

#below for debug uses

def read_file(filename):
    file = open(filename, "r")
    content = []
    for i in file.readlines():
        content.append(i.replace("\n",""))
    return content

if __name__=="__main__":
    char_text = read_file("sample_chara.txt")
    story_text = read_file("sample_story.txt")
    '''
    char_text = ["Hero","A2 B3 C2","Di In Me La Ac* Cr","----","doctorb","A3 B3 C1","Di In Me* La Ac Cr"]
    story_text = [
        "----",
        "S",
        "the friends are sitting in the little chicken café together after happily having submitted their assignment 3. This is the most convenient spot for them and was where they worked on the assignment together. Feeling their caffeine levels dropping below optimal, someone heads to the counter and offers to buy everyone a coffee. Many seconds pass while waiting in line (at least seven!) before they reach the front only to discover they left their wallet at home. They decide to...",
        "====",
        "1. [diplomacy 5] use their diplomacy skills to request ask for a freebie -1 +2",
        "2. [acumen 4] draw on all their internal acumen to *will* a coffee into existence ++3 +4 -1",
        "3. [acrobatics 3] use their acrobatics skills to dash home and return with their wallet before the other patrons are the wiser +5 -E~1",
        "4. give up and return to the table -E~1",
        "----","","----",
        "3",
        "Focusing very closely on their desire to be heavily caffeinated",
        "visualising the coffee before them and drawing on all the mental faculties and strength of will they can muster they ",
        'speak their desire to the universe "Oh great provisioners of stimulant beans and their associated beverages, I call upon thee. Share with me your bounty!" They feel a growing solid form of cup within there hand. Minutes pass as they continue to start at their cupped hands and reiterating their desire. The distinct aroma of fresh-brewed coffee wafts its way into', "their nostrils, they feel the warmth between their hands and low and behold in front of their eyes, their will is actioned. They returns to the table with their new coffee and a grin on their face. The friends give a questioning look", '"Something wrong with their machine?". Consequently...',
        '====',
        "1. [language 2] They draws upon their language skills to determine whether the empty hands represents an element of a signlanguage they are familiar with +6 -7 ++8",
        "2. [acrobatics 3] They use their acrobatics skills to get to the counter and order for themselves before they close -E~1 +9",
        '----']
    '''
    St = Story(story_text,char_text)
    '''
    print("==========RESULT 1==========")
    print(St.char_list[0])
    print(St.char_list[0].make_check("acrobatics",2,-1))
    #expect = +
    #got = -
    print("==========RESULT 2==========")
    print(St.char_list[0])
    print(St.char_list[0].make_check("acrobatics",2,2))
    #expect = ++
    #got = +
    print("==========RESULT 3==========")
    print(St.char_list[0])
    print(St.char_list[0].make_check("acrobatics",2,-4))
    #expect = -
    #got = --
    '''
    St.select_option(3,-1)
    St.select_option(2,-2)
    print(St.show_current_scene())

    
#python3 heh/story_class_structures.py

#python3 heh/test_character_class.py
#python3 heh/test_choose_your_own_adventure.py   
#python3 heh/test_make_check_function.py
#python3 heh/test_story_bestchar.py
#python3 heh/test_story_class.py
