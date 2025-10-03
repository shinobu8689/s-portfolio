
    .data

new_line:   .asciiz "\n"
space:      .asciiz " "
.globl print_combination
.globl combination_aux
.globl main

    .text

    j main

print_combination:
    # def print_combination(arr, n, r):
    # save $ra and $fp in stack
    addi $sp, $sp, -8   # make space
    sw $ra, 4($sp)      # save $ra
    sw $fp, 0($sp)      # save $fp
    addi $fp, $sp, 0    # copy $fp to $fp

    addi $sp, $sp, -4   # Allocate 4 bytes (data) of local var

    # 8($fp) is arr addr
    # 12($fp) is n
    # 16($fp) is r
    # -4($fp) is data addr

    # data = [0] * r
    addi $v0, $0, 9         # allocate space
    lw $t0, 16($fp)         # $t0 = r
    addi $t1, $0, 4         # $t1 = 4
    mult $t0, $t1           # $t1 = r * 4
    mflo $t1
    addi $t1, $t1, 4        # $t1 = (r * 4) + 4
    add $a0, $0, $t1
    syscall
    sw $v0, -4($fp)         # -4($fp) = data address

    lw $t0, 16($fp)         # $t0 = r
    sw $t0, ($v0)           # -4($fp).length = r
    # assign array value
    # all value of the array are zero so no need to assign

    # combination_aux(arr, n, r, 0, data, 0), 6var: (6*4) of arug
    addi $sp, $sp, -24
    lw $t0, 8($fp)     # arg 1 = arr addr
    sw $t0, 0($sp)
    lw $t0, 12($fp)    # arg 2 = n
    sw $t0, 4($sp)
    lw $t0, 16($fp)    # arg 3 = r
    sw $t0, 8($sp)
    addi $t0, $0, 0    # arg 4 = 0
    sw $t0, 12($sp)
    lw $t0, -4($fp)    # arg 5 = data addr
    sw $t0, 16($sp)
    addi $t0, $0, 0    # arg 6 = 0
    sw $t0, 20($sp)
    jal combination_aux

    addi $sp, $sp, 24   # remove arug

    addi $sp, $sp, 4    # remove local var

    lw $fp, 0($sp)      # restore $fp
    lw $ra, 4($sp)      # restore $ra
    addi $sp, $sp, 8    # deallocate

    jr $ra

#def combination_aux(arr, n, r, index, data, i):
combination_aux:
    # save $ra and $fp in stack
    addi $sp, $sp, -8   # make space
    sw $ra, 4($sp)      # save $ra
    sw $fp, 0($sp)      # save $fp
    addi $fp, $sp, 0    # copy $fp to $fp

    addi $sp, $sp, -4   # Allocate 4 bytes (j) of local var

    # 8($fp) is arr addr
    # 12($fp) is n
    # 16($fp) is r
    # 20($fp) is index
    # 24($fp) is data addr
    # 28($fp) is i
    # -4($fp) is j

    # if (index == r):
    lw $t0, 20($fp)     # $t0 = index
    lw $t1, 16($fp)     # $t1 = r
    bne $t0, $t1, if2   # if index != r, to if2

    # for j in range(r):
    lw $t0, -4($fp)     # j = 0
    addi $t0, $0, 0
    sw $t0, -4($fp)
loop:
    # while j < r:
    lw $t0, -4($fp)         # $t0 = j
    lw $t1, 16($fp)         # $t1 = r
    slt $t2, $t0, $t1       # $t2 = j < r
    beq $t2, $0, endloop    # if j < r, to endloop

    # print(data[j], end = " ")
    addi $v0, $0, 1
    lw $t0, 24($fp)     # $t0 = data addr
    lw $t1, -4($fp)     # $t1 = j
    addi $t2, $0, 4     # $t2 = 4
    mult $t1, $t2       # $t2 = j * 4
    mflo $t2
    add $t0, $t0, $t2   # $t0 = $t0 + $t2, shift array slot
    lw $a0, 4($t0)      # $a0 = data[j]
    syscall

    addi $v0, $0, 4     # print space between each num
    la $a0, space
    syscall

    lw $t0, -4($fp)     # j += 1
    addi $t0, $t0, 1
    sw $t0, -4($fp)

    j loop

endloop:

    addi $v0, $0, 4     # print()
    la $a0, new_line
    syscall

    j return

if2:
    # if (i >= n) (not (i < n)):
    lw $t0, 28($fp)     # $t0 = i
    lw $t1, 12($fp)     # $t1 = n
    slt $t2, $t0, $t1   # $t2 = i < n
    beq $t2, $0, return # if i < n, to return

    lw $t0, 24($fp)     # $t0 = data addr
    lw $t1, 20($fp)     # $t1 = ,index
    addi $t2, $0, 4     # $t2 = 4
    mult $t1, $t2       # $t2 = index * 4
    mflo $t2
    add $t0, $t0, $t2
    lw $t3, 4($t0)

    #data[index] = arr[i]
    lw $t0, 8($fp)      # $t0 = arr addr
    lw $t1, 28($fp)     # $t1 = i
    addi $t2, $0, 4     # $t2 = 4
    mult $t1, $t2       # $t2 = i * 4
    mflo $t2
    add $t0, $t0, $t2
    lw $t3, 4($t0)      # $t3 = arr[i]


    lw $t0, 24($fp)     # $t0 = data addr
    lw $t1, 20($fp)     # $t1 = index
    addi $t2, $0, 4     # $t2 = 4
    mult $t1, $t2       # $t2 = index * 4
    mflo $t2
    add $t0, $t0, $t2
    sw $t3, 4($t0)      # data[index] = arr[i]


# combination_aux(arr, n, r, index + 1, data, i + 1), 6 var: (6*4) of arug
    addi $sp, $sp, -24
    lw $t0, 8($fp)      # arg 1 = arr addr
    sw $t0, 0($sp)
    lw $t0, 12($fp)     # arg 2 = n
    sw $t0, 4($sp)
    lw $t0, 16($fp)     # arg 3 = r
    sw $t0, 8($sp)
    lw $t0, 20($fp)     # arg 4 = index + 1
    addi $t0, $t0, 1
    sw $t0, 12($sp)
    lw $t0, 24($fp)     # arg 5 = data addr
    sw $t0, 16($sp)
    lw $t0, 28($fp)     # arg 6 = i + 1
    addi $t0, $t0, 1
    sw $t0, 20($sp)
    jal combination_aux

    addi $sp, $sp, 24   # remove arug

    # combination_aux(arr, n, r, index, data, i + 1), 6 var: (6*4) of arug
    addi $sp, $sp, -24
    lw $t0, 8($fp)      # arg 1 = arr addr
    sw $t0, 0($sp)
    lw $t0, 12($fp)     # arg 2 = n
    sw $t0, 4($sp)
    lw $t0, 16($fp)     # arg 3 = r
    sw $t0, 8($sp)
    lw $t0, 20($fp)     # arg 4 = index
    sw $t0, 12($sp)
    lw $t0, 24($fp)     # arg 5 = data addr
    sw $t0, 16($sp)
    lw $t0, 28($fp)     # arg 6 = i + 1
    addi $t0, $t0, 1
    sw $t0, 20($sp)
    jal combination_aux

    addi $sp, $sp, 24   # remove arug


return:

    addi $sp, $sp, 4    # remove local var

    lw $fp, 0($sp)      # restore $fp
    lw $ra, 4($sp)      # restore $ra
    addi $sp, $sp, 8    # deallocate

    jr $ra




main:
    # set $fp and make space for locals
    addi $fp, $sp, 0        # copy $sp into $fp
    addi $sp, $sp, -12      # Allocate 12 bytes (arr & r & n) of local var

    # arr = [1, 2, 3, 4, 5]
    addi $v0, $0, 9         # allocate space
    addi $a0, $0, 24        # (5 * 4) + 4
    syscall
    sw $v0, -12($fp)        # -12($fp) = address
    addi $t0, $0, 5         # $t0 = 5
    sw $t0, ($v0)           # -12($fp).length = 5
    # assign array value
    lw $t0, -12($fp)        # $t0 = arr address
    addi $t1, $0, 1
    sw $t1,  4($t0)         # -12($fp)[0] = 1
    addi $t1, $0, 2
    sw $t1,  8($t0)         # -12($fp)[1] = 2
    addi $t1, $0, 3
    sw $t1, 12($t0)         # -12($fp)[2] = 3
    addi $t1, $0, 4
    sw $t1, 16($t0)         # -12($fp)[3] = 4
    addi $t1, $0, 5
    sw $t1, 20($t0)         # -12($fp)[4] = 5

    addi $t0, $0, 3         # r = 3
    sw $t0, -8($fp)

    # n = len(arr)
    lw $t0, -12($fp)        # $t0 = arr address
    lw $t1, ($t0)
    sw $t1, -4($fp)

    # -12($fp) = arr address
    # -8($fp) = r
    # -4($fp) = n

    # call print_combination(arr, n, r), 3 var: (3*4) of arug
    addi $sp, $sp, -12
    lw $t0, -12($fp)        # arg 1 = arr addr
    sw $t0, 0($sp)
    lw $t0, -4($fp)         # arg 2 = n
    sw $t0, 4($sp)
    lw $t0, -8($fp)         # arg 3 = r
    sw $t0, 8($sp)
    jal print_combination

    addi $sp, $sp, 12       # remove arug

    # exit
    addi $v0, $0, 10
    syscall

