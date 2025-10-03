'''
Group plz input team name

Alvina Florence
Mingru Qin
Yansen Gunawan Tjeng
Yin Lam lo


'''
from story_class_structures_bestchar import StoryBest, Scene, Character
def read_file(filename):
    '''
    to read file from another text file
    param: filename (str)
    '''
    file = open(filename, "r")
    content = []
    for i in file.readlines():
        content.append(i.replace("\n",""))
    return content

if __name__ == "__main__":
    # this is the application so the file name could change
    char_text = read_file("test_cR5.txt")
    story_text = read_file("test_s.txt")
    St = StoryBest(story_text,char_text)

    while True:
        print(St.show_current_scene())
        if "E" in St.get_scene_id(): # it should end when it is the end scene
            break
        input_choice = input("Your Choice:")
        required = St.search_scene(St.get_scene_id()).get_option_spec()[int(input_choice) - 1][1]
        if required.isalpha():
            the_guy = St.select_character_for_check(required)
            St.swap_char(the_guy)

        St.select_option(input_choice,None)

