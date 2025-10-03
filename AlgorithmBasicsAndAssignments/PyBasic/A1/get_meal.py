options = []
users_input = input()

#will keep inputting the menu until "." is inputted
while users_input != ".":
    users_input = users_input.split(",")
    #taking and store the values into the dictionary
    meal_info = {"name" : str(users_input[0]), "sell_for" : float(users_input[1]), "cost_to_make" : float(users_input[2]), "cook_time": float(users_input[3]), "cook_time_stdev" : float(users_input[4])}
    options.append(meal_info)
    users_input = input()

print(options)
