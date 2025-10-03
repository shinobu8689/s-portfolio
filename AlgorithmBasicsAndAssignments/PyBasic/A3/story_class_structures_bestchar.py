'''
Group plz input team name

Alvina Florence
Mingru Qin
Yansen Gunawan Tjeng
Yin Lam lo

python3 story_class_structures.py
python3 test_character_class.py
python3 test_choose_your_own_adventure.py   
python3 test_make_check_function.py
python3 test_story_bestchar.py
python3 test_story_class.py
'''
from story_class_structures import Story, Scene, Character
import re
#import the story and character class from base file 

class StoryBest(Story):
    '''
    StoryBest represents the story containing all the data of relevant scenes, options and characters appropriate with some revised function where it is able to identify which characters is the best option without actually running the check.

    attribute:
    scene_string_data     (list)
    characters_in_story   (list)
    current_scene         (str)

    method:
    __init__(self,scene_string_data,characters_in_story)
    swap_char(self,new_guy)
    select_character_for_check(self,skill_or_attribute_name)
    select_option(self,option_number,override)   
    '''
    def __init__(self,scene_string_data,characters_in_story):
        '''
        the constructor
        param: scene_string_data (list), characters_in_story (list)
        '''
        Story.__init__(self,scene_string_data,characters_in_story)
        self.current_character = self.char_list[0]

    def swap_char(self,new_guy):
        '''
        to swap the current character with the other character
        param : new_guy
        '''
        self.current_character = new_guy

    def select_character_for_check(self,skill_or_attribute_name):
        '''
        to identify which is best placed to make a given check without actually running the check
        param : skill_or_attribute_name (str)
        '''
        the_guy = None
        highest_value = 0
        for i in self.char_list:
            if skill_or_attribute_name == "diplomacy" or skill_or_attribute_name == "language" or skill_or_attribute_name == "charm":
                char_value = i.get_charm()
            elif skill_or_attribute_name == "investigation" or skill_or_attribute_name == "medicine" or skill_or_attribute_name == "acumen":
                char_value = i.get_acumen()
            elif skill_or_attribute_name == "acrobatics" or skill_or_attribute_name == "craft" or skill_or_attribute_name == "body":
                char_value = i.get_body()
            if i.skill == skill_or_attribute_name:
                char_value += 2
            if char_value > highest_value:
                highest_value = char_value
                the_guy = i
        return the_guy
    
    def select_option(self,option_number,override):
        '''
        proceed to next scene
        param: option_number (int), override (int)
        '''
        if "E" in self.current_scene: # there is no next scene if arrive at ending
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
                decision = self.select_character_for_check(selected_option[1]).make_check(selected_option[1],selected_option[2],override) # generate consequences
            index_with_skill = 3
            out = self.find_next_scene(index_with_skill,selected_option,decision)

        else: # if option no skill required
            index_without_skill = 1
            out = self.find_next_scene(index_without_skill,selected_option,None)

        #set next scene
        self.current_scene = out

#below for debug uses

def read_file(filename):
    '''
    to read file from another text file
    param: filename
    '''
    file = open(filename, "r")
    content = []
    for i in file.readlines():
        content.append(i.replace("\n",""))
    return content

if __name__ == "__main__":
    char_text = read_file("sample_chars.txt")
    story_text = read_file("sample_story.txt")

    St = StoryBest(story_text,char_text)

    #print(St.current_character)
    St.select_option(2,-3)
    #St.select_option(5,1)
    #print(St.get_scene_id())
    print(St.show_current_scene())
    #print(St.select_option(2,1))
    #print(St.show_current_scene())
    #print(St.show_current_scene())
    

    

#python3 heh/story_class_structures_bestchar.py
#python3 heh/test_story_bestchar.py
    
