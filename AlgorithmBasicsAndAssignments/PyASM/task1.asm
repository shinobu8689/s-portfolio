    .data

tier_one_price:     .word 9
tier_two_price:     .word 11
tier_three_price:   .word 14
discount_flag:      .word 0
age:                .word 0
consumption:        .word 0
total_cost:         .word 0
gst:                .word 0
total_bill:         .word 0

# initialise prompt
welcome:            .asciiz "Welcome to the Thor Electrical Company!\n"
age_prompt:         .asciiz "Enter your age: "
consumption_prompt: .asciiz "Enter your total consumption in kWh: "
bill_prompt:        .asciiz "Mr Loki Laufeyson, your electricity bill is $"
point:              .asciiz "."
new_line:           .asciiz "\n"

    .text

    # print("Welcome to the Thor Electrical Company!")
    addi $v0, $0, 4
    la $a0, welcome
    syscall



    # age = int(input("Enter your age: "))
    addi $v0, $0, 4
    la $a0, age_prompt
    syscall
    # ask for input to age
    addi $v0, $0, 5
    syscall
    sw $v0, age



    # if age <= 18 or age >= 65:
    # check for age <= 18 (not 18 < age)
    lw $t0, age                 # $t0 = age
    addi $t1, $0, 18            # $t1 = 18
    slt $t2, $t1, $t0           # $t2 = 18 < age
    bne $t2, $0, else_age       # if 18 < age == 1, to else_age

    # if age <= 18 is false, then continue to check age >= 65 (not age < 65)
    lw $t0, age                 # $t0 = age
    addi $t1, $0, 65            # $t1 = 18
    slt $t2, $t0, $t1           # $t2 = age < 65
    bne $t2, $0, else_age       # if age < 65 == 1, to else_age



    # if age <= 18 and age >= 65 are both true
    # discount_flag = 1
    addi $t0, $0, 1
    sw $t0, discount_flag
    j endif_age



else_age:
    # discount_flag = 0
    addi $t0, $0, 0
    sw $t0, discount_flag

endif_age:



    # consumption = int(input("Enter your total consumption in kWh: "))
    addi $v0, $0, 4
    la $a0, consumption_prompt
    syscall
    # ask for consumption input
    addi $v0, $0, 5
    syscall
    sw $v0, consumption



    # if consumption > 1000 and discount_flag == 0:
    # check consumption > 1000 first (1000 < consumption)
    lw $t0, consumption             # $t0 = consumption
    addi $t1, $0, 1000              # $t1 = 1000
    slt $t2, $t1, $t0               # $t2 = 1000 < consumption
    beq $t2, $0, elif_consumption   # if 1000 < consumption == 1, to elif_consumption

    # if 1000 < consumption == 0, check discount_flag == 0
    lw $t0, discount_flag           # t0 = discount_flag
    bne $t0, $0, elif_consumption   # if discount_flag == 1, to elif_consumption



    # total_cost = total_cost + ((consumption-1000)*tier_three_price)
    lw $t0, total_cost          # $t0 = total_cost
    lw $t1, consumption         # $t1 = consumption
    addi $t2, $0, 1000          # $t2 = 1000
    lw $t3, tier_three_price    # $t3 = tier_three_price
    sub $t4, $t1, $t2           # $t4 = consumption - 1000
    mult $t4, $t3               # $t4 = (consumption - 1000) * tier_three_price
    mflo $t4
    add $t5, $t0, $t4           # $t5 = total_cost + (consumption - 1000) * tier_three_price
    sw $t5, total_cost          # total_cost = $t5



    # consumption = 1000
    addi $t0, $0, 1000
    sw $t0, consumption



elif_consumption:
    # elif consumption > 1000:
    lw $t0, consumption         # $t0 = consumption
    addi $t1, $0, 1000          # $t1 = 1000
    slt $t2, $t1, $t0           # $t2 = 1000 < consumption
    beq $t2, $0, endif_consumption1000  # if 1000 < consumption == 0, to endif_consumption1000



    #total_cost = total_cost + ((consumption-1000) * (tier_three_price - 2))
    lw $t0, total_cost          # $t0 = total_cost
    lw $t1, consumption         # $t1 = consumption
    addi $t2, $0, 1000          # $t2 = 1000
    lw $t3, tier_three_price    # $t3 = tier_three_price
    addi $t4, $0, 2             # $t4 = 2
    sub $t5, $t1, $t2           # $t5 = consumption - 1000
    sub $t6, $t3, $t4           # $t6 = tier_three_price - 2
    mult $t5, $t6               # $t5 = (consumption - 1000) * (tier_three_price - 2)
    mflo $t5
    add $t6, $t0, $t5           # $t6 = total_cost + (consumption - 1000) * (tier_three_price - 2)
    sw $t6, total_cost          # total_cost = $t6



    # consumption = 1000
    addi $t0, $0, 1000
    sw $t0, consumption

endif_consumption1000:



    #if consumption > 600 (consumption < 600):
    lw $t0, consumption                    # $t0 = consumption
    addi $t1, $0, 600                      # $t1 = 600
    slt $t2, $t1, $t0                      # $t2 = consumption < 600
    beq $t2, $0, endif_consumption         # if consumption < 600 == 0, to endif_consumption



    # total_cost = total_cost + ((consumption - 600) * tier_two_price)
    lw $t0, total_cost          # $t0 = total_cost
    lw $t1, consumption         # $t1 = consumption
    addi $t2, $0, 600           # $t2 = 600
    lw $t3, tier_two_price      # $t3 = tier_two_price
    sub $t4, $t1, $t2           # $t4 = consumption - 600
    mult $t4, $t3               # $t4 = (consumption - 600) * tier_two_price
    mflo $t4
    add $t5, $t0, $t4           # $t5 = total_cost + ((consumption - 600) * tier_two_price)
    sw $t5, total_cost          # total_cost = $t5



    # consumption = 600
    addi $t0, $0, 600
    sw $t0, consumption

endif_consumption:



    # total_cost = total_cost + (consumption*tier_one_price)
    lw $t0, total_cost          # $t0 = total_cost
    lw $t1, consumption         # $t1 = consumption
    lw $t2, tier_one_price      # $t2 = tier_one_price
    mult $t1, $t2               # $t3 = consumption * tier_one_price
    mflo $t3
    add $t3, $t0, $t3           # $t3 = total_cost + (consumption * tier_one_price)
    sw $t3, total_cost          # total_cost = $t3



    # gst = total_cost // 10
    lw $t0, total_cost          # $t0 = total_cost
    addi $t1, $0, 10            # $t1 = 10
    div $t0, $t1                # $t2 = total_cost // 10
    mflo $t2
    sw $t2, gst                 # gst = $t2



    # total_bill = total_cost + gst
    lw $t0, total_cost          # $t0 = total_cost
    lw $t1, gst                 # $t1 = gst
    add $t2, $t0, $t1           # $t2 = total_cost + gst
    sw $t2, total_bill          # total_bill = $t2



    # print(f"Mr Loki Laufeyson, your electricity bill is ${total_bill // 100}.{total_bill % 100}")
    # print("Mr Loki Laufeyson, your electricity bill is $")
    addi $v0, $0, 4
    la $a0, bill_prompt
    syscall

    # print(total_bill // 100)
    lw $t0, total_bill          # $t0 = total_bill
    addi $t1, $0, 100           # $t1 = 0 + 100
    div $t0, $t1                # $t2 = total_bill // 100
    mflo $t2
    addi $v0, $0, 1
    addi $a0, $t2, 0            # $a0 = total_bill // 100
    syscall

    # print(".")
    addi $v0, $0, 4             # $v0 = 0 + 4
    la $a0, point               # $a0 = point
    syscall

    # print(total_bill % 100)
    lw $t0, total_bill          # $t0 = total_bill
    addi $t1, $0, 100           # $t1 = 0 + 100
    div $t0, $t1                # $t2 = total_bill % 100
    mfhi $t2
    addi $v0, $0, 1
    addi $a0, $t2, 0            # $a0 = total_bill % 100
    syscall

    # print new line
    addi $v0, $0, 4
    la $a0, new_line
    syscall



    # exit
    addi $v0, $0, 10
    syscall
