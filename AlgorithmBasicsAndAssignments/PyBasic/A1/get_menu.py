options = []
default_menu = ["Budda Bowl (vg),25,20,10,3","Eye Fillet Steak,55,25,7,1","Spaghetti Bolognese,30,22,40,5","Pad Thai (seafood),22,17,30,1","."]
default_menu_mode = False
i = 1

#default_menu_mode: determine user's input menu or use default_menu
#initial user input
users_input = input()
if users_input == ".":
    default_menu_mode = True
    users_input = default_menu[0]
 
#input section
while users_input != ".":
    users_input = users_input.split(",")
    #taking and store the values into the dictionary
    meal_info = {"name" : str(users_input[0]), "sell_for" : float(users_input[1]), "cost_to_make" : float(users_input[2]), "cook_time": float(users_input[3]), "cook_time_stdev" : float(users_input[4])}
    options.append(meal_info)
    #if true, it will take from the default_menu or else it will ask for input from the user
    if default_menu_mode:
        users_input = default_menu[i]
    else:
        users_input = input()
    i += 1

#print options
i = 1
for meal in options:
    #taking and store the values into the dictionary then printing it according to the sample output
    print(f'{i}. Name:{meal.get("name")} Sells:${meal.get("sell_for")} Costs:${meal.get("cost_to_make")} Takes:{meal.get("cook_time")} mins')
    i += 1
