"""
This file serves as an example Python code for Task 1 Assignment 1
"""
__author__ = "Saksham Nagpal"
__date__ = "18.05.2022"

tier_one_price = 9
tier_two_price = 11
tier_three_price = 14
discount_flag = 0

print("Welcome to the Thor Electrical Company!")
age = int(input("Enter your age: "))
if age <= 18 or age >= 65:
    discount_flag = 1
else:
    discount_flag = 0

consumption = int(input("Enter your total consumption in kWh: "))
total_cost = 0

if consumption > 1000 and discount_flag == 0:
    total_cost = total_cost + ((consumption-1000)*tier_three_price)
    consumption = 1000
elif consumption > 1000:
    total_cost = total_cost + ((consumption-1000) * (tier_three_price - 2))
    consumption = 1000

if consumption > 600:
    total_cost = total_cost + ((consumption-600)*tier_two_price)
    consumption = 600
else:
    total_cost = total_cost + ((consumption-600)*(tier_two_price-2))
    consumption = 600

total_cost = total_cost + (consumption*tier_one_price)
gst = total_cost // 10

total_bill = total_cost + gst
print(f"Mr Loki Laufeyson, your electricity bill is ${total_bill // 100}.{total_bill % 100}")