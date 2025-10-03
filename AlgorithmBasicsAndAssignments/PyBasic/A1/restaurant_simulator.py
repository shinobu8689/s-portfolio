import random


def get_meals_list_from_user():
    options = []
    default_menu = ["Budda Bowl (vg),25,20,10,3","Eye Fillet Steak,55,25,7,1","Spaghetti Bolognese,30,22,40,5","Pad Thai (seafood),22,17,30,1","."]
    default_menu_mode = False #flag for using default_menu or asking user for input
    i = 1 #for tracking the default_menu's slot

    #input section
    #determine is default_menu_mode
    users_input = input()
    if users_input == ".":
        #activate default_menu_mode
        default_menu_mode = True
        users_input = default_menu[0]

    #load default_menu/user's menu to dict and into the list 
    while users_input != ".":
        users_input = users_input.split(",")
        #taking and store the values into the dictionary
        meal_info = {"name" : str(users_input[0]), "sell_for" : float(users_input[1]), "cost_to_make" : float(users_input[2]), "cook_time": float(users_input[3]), "cook_time_stdev" : float(users_input[4])}
        options.append(meal_info)
        #if it is default_menu_mode then take from the default_menu, if not ask the user for the next input
        if default_menu_mode:
            users_input = default_menu[i]
        else:
            users_input = input()
        i += 1
    return options


def display_menu(options):
    i = 1
    for meal in options: #print a formatted string
        print(f'{i}. Name:{meal.get("name")} Sells:${meal.get("sell_for")} Costs:${meal.get("cost_to_make")} Takes:{meal.get("cook_time")} mins')
        i += 1


def validate_user_choice(options, users_input):
    #return True when the input are within the range of the menu and numbers only
    if users_input.isnumeric() and int(users_input) > 0 and int(users_input) <= len(options) :
        return True
    else:
        return False


#determine the state of the meal according to the condition
def classify_cook_time(average_cook_time, stdev_cook_time, actual_cook_time):
    t = actual_cook_time
    mu = average_cook_time
    sigma = stdev_cook_time

    if t < mu - 2 * sigma:
        return "very undercooked"
    elif t >= mu - 2 * sigma and t <= mu - sigma:
        return "slightly undercooked"
    elif t > mu - sigma and t < mu + sigma:
        return "well cooked"
    elif t >= mu + sigma and t <= mu + 2 * sigma:
        return "slightly overcooked"
    else: #t > mu + 2 * sigma
        return "very overcooked"


#determine the cooking tip according to the classification
def get_cooking_tip(classification, base_tip):
    if classification == "very undercooked":
        tip = -100
    elif classification == "slightly undercooked":
        tip = 0
    elif classification == "well cooked":
        tip = base_tip
    elif classification == "slightly overcooked":
        tip = 0
    elif classification == "very overcooked":
        tip = -100
    return tip


#calculate the random_tip (0 - 1)
def random_tip_compute(tip_chance, base_tip_value, random_comparison):
    tip_probability = random_comparison
    if tip_probability <= tip_chance: #get tip when below the tip_chance range (satisfied)
        final_tip = base_tip_value
    elif tip_probability >= (1 - tip_chance):  #customer pay less when above the 1 - tip_chance range (unsatisfied)
        final_tip = -base_tip_value
    else: #normal
        final_tip = base_tip_value * 0
    return final_tip

#====================above funtions are from previous tasks====================

def order(options):
    print("Please enter your order. The options are given below")
    display_menu(options)

    #get users selection
    print("Please enter a number to make your choice")
    users_selection = input()
    #ask for re-input if its not valid
    while not validate_user_choice(options, users_selection):
        print("Invalid input, Please enter a number to make your choice.")
        users_selection = input()
    selected_meal = options[int(users_selection) - 1] #store the selected meal object
    print(f'now cooking {selected_meal.get("name")}')

    #get meal status
    attempt = 0
    total_profit = 0
    while attempt < 3:
        #generate cook times value and determine the status of the meal
        avg_cook_time = selected_meal.get("cook_time")
        cook_time_stdev = selected_meal.get("cook_time_stdev")
        actual_cook_time = round(random.gauss(avg_cook_time,cook_time_stdev),2)
        meal_state = classify_cook_time(avg_cook_time, cook_time_stdev, actual_cook_time)
        print(f'{selected_meal.get("name")} was {meal_state} ({actual_cook_time} vs {avg_cook_time} mins)')
    
        #tip calculation
        cooking_tip = get_cooking_tip(meal_state, 10)
        random_value = round(random.random(), 2)
        random_tip = random_tip_compute(0.1, 5, random_value)
        print(f'cooking tip was {cooking_tip} random tip was {random_tip} the random value being ({random_value})' )

        #calculate the profit
        final_price = round(selected_meal.get("sell_for") * (1 + cooking_tip/100) * (1 + random_tip/100),2)
        print(f'final selling price was ${final_price}')
        profit = round(final_price - selected_meal.get("cost_to_make"),2)
        #formatting value to display (make $-100 looks like -> -$100)
        plus_minus = ""
        profit_display = profit
        if profit < 0 :
            profit_display = profit * -1
            plus_minus = "-"
        print(f'for a profit of {plus_minus}${profit_display}')

        #add to total_profit each time the meals are cooked 
        total_profit += profit

        #if the meal is not overcooked/undercooked, it should not cook again (out of the loop)
        if not cooking_tip < 0 :
            break
        #otherwise another attempt to cook again
        attempt += 1

    if attempt >= 3:
        print("giving up after 3 failed attempts")

    #total profit/loss for this meal
    #formatting value to display (make $-100 looks like -> -$100)
    plus_minus = ""
    total_profit_display = total_profit
    if total_profit < 0 :
            total_profit_display = total_profit * -1
            plus_minus = "-"
    print(f'overall, the profit for this meal was {plus_minus}${total_profit_display}')

    return total_profit

def order_for_x_people(X):
    options = get_meals_list_from_user()
    customer_remaining = X
    total_customer_profit = 0

    #serving each customer
    while customer_remaining != 0: 
        total_customer_profit += order(options)
        customer_remaining -= 1
        
        #calculating total_customer_profit
        #formatting value to display (make $-100 looks like -> -$100)
        plus_minus = ""
        total_customer_profit_display = total_customer_profit
        if total_customer_profit < 0:
            total_customer_profit_display = total_customer_profit * -1
            plus_minus = "-"
        print(f'running profit {plus_minus}${total_customer_profit_display}')

    print(f'After serving meals to {X} people, we made a profit of {plus_minus}${total_customer_profit_display}')
    return total_customer_profit

if __name__ == "__main__":
    order_for_x_people(3)

