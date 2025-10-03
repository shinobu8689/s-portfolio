import random
str = input().split(",")

#will generate a random number by using the average and the standard deviation from input
cooking_time = random.gauss(float(str[0]),float(str[1]))
tip_probability = random.random()

#if the tip probability is less than 10%, it will be positive tip, but if greater than 90%, then it will be negative tip
if tip_probability >= 0.9:
    final_tip = -5
elif tip_probability <= 0.1:
    final_tip = 5
else:
    final_tip = 0

print(f'Actual cooking time was {cooking_time} and the tip paid was {final_tip}%')
