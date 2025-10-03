
    .data

height:         .word 0
space:          .asciiz " "
valid_input:    .word 0
height_prompt:  .asciiz "How tall do you want the tower: "
i:              .word 0
s:              .word 0
j:              .word 0
A:              .asciiz "A "
star:           .asciiz "* "
new_line:       .asciiz "\n"


    .text


while1:
    # while valid_input == 0:
    lw $t0, valid_input         # $t0 = valid_input
    bne $t0, $0, endwhile1      # if valid_input == 0, to endwhile1



    # height = int(input("How tall do you want the tower: "))
    # print prompt
    addi $v0, $0, 4
    la $a0, height_prompt
    syscall
    # ask for input
    addi $v0, $0, 5
    syscall    
    sw $v0, height
        


    # if height >= 5 (not height < 5):
    lw $t0, height              # $t0 = height
    addi $t1, $0, 5             # $t1 = 0 + 5
    slt $t2, $t0, $t1           # $t2 = height < 5
    bne $t2, $0, endif1         # if height < 5 == 1, end loop
    
    
    
    # valid_input = 1
    addi $t0, $0, 1
    sw $t0, valid_input

endif1:
    j while1                   

endwhile1:



            
for1:
    # for i in range(height):
    lw $t0, height              # $t0 = height              
    lw $t1, i                   # $t1 = i
    beq $t1, $t0, end_for1      # if i == height, end loop



    # for s in range( ( height+1 ) * -1, -i):
    # range ( height+1 ) * -1
    lw $t0, height              # $t0 = height
    addi $t0, $t0, 1            # $t0 = height + 1
    addi $t1, $0, -1            # $t1 = 0 + (-1)
    mult $t0, $t1               # $t2 = ( height + 1 ) * -1
    mflo $t2
    sw $t2, s                   # s = $t2

for2:
    lw $t0, s                   # $t0 = s
    lw $t1, i                   # $t1 = i, decrement -i
    addi $t2, $0, -1            # $t2 = 0 + (-1)
    mult $t1, $t2               # $t1 = $t1 * $t2
    mflo $t1                
    beq $t0, $t1, end_for2      # if s == -i, end loop



    # print(" ", end="")
    addi $v0, $0, 4
    la $a0, space
    syscall

    lw $t0, s                   # $t0 = s
    addi $t0, $t0, 1            # $t0 = $t0 + 1, s increment
    sw $t0, s                   # s = $t0

    j for2

end_for2:



        
for3:
    # for j in range(i+1):
    lw $t0, i                   # $t0 = i
    lw $t1, j                   # $t1 = j
    addi $t0, $t0, 1            # $t0 = $t0 + 1
    beq $t1, $t0, end_for3      # if j == (i + 1), end loop



    # if i == 0:
    lw $t0, i               # $t0 = i
    bne $t0, $0, else2      # if i ==1, to else2



    # print("A ", end="")
    addi $v0, $0, 4
    la $a0, A
    syscall

    j endif2



else2:
    # print("* ", end="")
    addi $v0, $0, 4
    la $a0, star
    syscall

endif2:

    lw $t0, j               # $t0 = j
    addi $t0, $t0, 1        # $t0 = $t0 + 1
    sw $t0, j               # j = $t0

    j for3

end_for3:

    # manual reset the value of j, python does this automaticly but mips wont
    addi $t0, $0, 0
    sw $t0, j



    # print()
    addi $v0, $0, 4         # next line for the tower
    la $a0, new_line
    syscall


    # i += 1
    lw $t0, i               # $t0 = i
    addi $t0, $t0, 1        # $t0 = $t0 + 1
    sw $t0, i               # i = $t0

    j for1

end_for1:



    # exit
    addi $v0, $0, 10        # $v0 = 0 + 10
    syscall
