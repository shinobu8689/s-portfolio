height = 0
space = " "
valid_input = 0

while valid_input == 0:
   height = int(input("How tall do you want the tower: "))
   if height >= 5:
       valid_input = 1

for i in range(height):
    for s in range((height+1)*-1, -i):
        print(" ", end="")
    for j in range(i+1):
        if i == 0:
            print("A ", end="")
        else:
            print("* ", end="")
    print()