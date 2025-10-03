
    .data

new_line: .asciiz "\n"
space:    .asciiz " "
.globl insertion_sort
.globl main
    .text

    j main

insertion_sort:
    # def insertion_sort(the_list: List[T]):
    # save $ra and $fp in stack
    addi $sp, $sp, -8   # make space
    sw $ra, 4($sp)      # save $ra
    sw $fp, 0($sp)      # save $fp
    addi $fp, $sp, 0    # copy $fp to $fp

    addi $sp, $sp, -16       # Allocate 16 bytes (length & i & j & key) of local var

    # -16($fp) is length
    # -12($fp) is i
    # -8($fp) is j
    # -4($fp) is key

    # length = len(the_list)
    lw $t0, -16($fp)    # $t0 = length
    lw $t1, 8($fp)      # $t1 = array addr
    lw $t2, ($t1)       # $t2 = array.size
    addi $t0, $t2, 0    # $t0 = array.size
    sw $t0, -16($fp)    # length = $t0

    # for i in range(1, length):
    lw $t0, -12($fp)        # $t0 = i
    addi $t0, $0, 1         # $t0 = i + 1
    sw $t0, -12($fp)        # i = $t0
loop_i:
    lw $t0, -12($fp)        # $t0 = i
    lw $t1, -16($fp)        # $t1 = length
    slt $t2, $t0, $t1       # $t2 = i < length
    beq $t2, $0, endloop_i  # if i >= length, to endloop_i

    # key = the_list[i]
    lw $t0, -4($fp)     # $t0 = key
    lw $t1, 8($fp)      # $t1 = arr adddr
    lw $t2, -12($fp)    # $t2 = i
    addi $t3, $0, 4     # $t3 = 4
    mult $t2, $t3       # $t3 = i * 4
    mflo $t3
    add $t1, $t1, $t3   # $t1 = $t1 + $t3 shift array slot
    lw $t4, 4($t1)      # $t2 = the_list[i]
    sw $t4, -4($fp)     # key = $t2

    # j = i - 1
    lw $t0, -8($fp)     # $t0 = j
    lw $t1, -12($fp)    # $t1 = i
    addi $t0, $t1, -1   # j = i - 1
    sw $t0, -8($fp)

loop_j:
    # while j >= 0 (not j < 0) and key < the_list[j] :
    lw $t0, -8($fp)         # $t0 = j
    slt $t1, $t0, $0        # j < 0
    bne $t1, $0, endloop_j  # if j < 0, to endloop_j

    lw $t0, -4($fp)         # $t0 = key
    lw $t1, 8($fp)          # $t1 = arr adddr
    lw $t2, -8($fp)         # $t2 = j
    addi $t3, $0, 4         # $t3 = 4
    mult $t2, $t3           # $t3 = j * 4
    mflo $t3
    add $t1, $t1, $t3       # $t1 = $t1 + $t3 shift array slot
    lw $t4, 4($t1)          # $t4 = the_list[j]
    slt $t5, $t0, $t4
    beq $t5, $0, endloop_j  # if j < 0, to endloop_j

    # the_list[j + 1] = the_list[j]
    # get value of the_list[j]
    lw $t0, 8($fp)          # $t0 = arr addr
    lw $t1, -8($fp)         # $t1 = j
    addi $t2, $0, 4         # $t2 = 4
    mult $t1, $t2           # $t2 = j * 4
    mflo $t2
    add $t0, $t0, $t2       # $t0 = $t0 + $t2 shift array slot
    lw $t3, 4($t0)          # $t3 = the_list[j]
    #get addr of the_list[j+1]
    lw $t4, 8($fp)          # $t4 = arr adddr
    lw $t5, -8($fp)         # $t5 = j
    addi $t6, $0, 4         # $t6 = 4
    mult $t5, $t6           # $t6 = j * 4
    mflo $t6
    addi $t6, $t6, 4        # $t6 = j * 4 + 4
    add $t4, $t4, $t6       # $t4 = $t4 + $t6 shift array slot
    sw $t3, 4($t4)          # the_list[j + 1] = the_list[j]

    # j -= 1
    lw $t0, -8($fp)
    addi $t0, $t0, -1
    sw $t0, -8($fp)

    j loop_j

endloop_j:


    #the_list[j + 1] = key
    lw $t0, -4($fp)         # $t0 = key
    lw $t1, 8($fp)          # $t1 = arr addr
    addi $t2, $0, 4         # $t2 = 4
    lw $t3, -8($fp)         # $t3 = j
    mult $t2, $t3           # $t3 = j * 4
    mflo $t3
    addi $t3, $t3, 4        # $t3 = j * 4 + 4
    add $t1, $t1, $t3
    sw $t0, 4($t1)

    # i += 1
    lw $t0, -12($fp)
    addi $t0, $t0, 1
    sw $t0, -12($fp)

    j loop_i

endloop_i:

    addi $sp, $sp, 16   # remove local var
    lw $fp, 0($sp)      # restore $fp
    lw $ra, 4($sp)      # restore $ra
    addi $sp, $sp, 8    # deallocate

    jr $ra





main:
    # set $fp and make space for locals
    addi $fp, $sp, 0        # copy $sp into $fp
    addi $sp, $sp, -8       # Allocate 8 bytes of local var arr & i

    # arr = [6, -2, 7, 4, -10]
    addi $v0, $0, 9         # allocate space
    addi $a0, $0, 16        # (5 * 4) + 4
    syscall
    sw $v0, -8($fp)         # -8($fp) = address
    addi $t0, $0, 5         # $t0 = 5
    sw $t0, ($v0)           # -8($fp).length = 5
    # assign array value
    lw $t0, -8($fp)         # $t0 = arr address
    addi $t1, $0, 6
    sw $t1,  4($t0)         # -8($fp)[0] = 6
    addi $t1, $0, -2
    sw $t1,  8($t0)         # -8($fp)[1] = -2
    addi $t1, $0, 7
    sw $t1, 12($t0)         # -8($fp)[2] = 7
    addi $t1, $0, 4
    sw $t1, 16($t0)         # -8($fp)[3] = 4
    addi $t1, $0, -10
    sw $t1, 20($t0)         # -8($fp)[4] = -10

    # -8($fp) = arr address
    # -4($fp) = i

    # call insertion_sort(arr), 1 var: (1*4) of arug
    addi $sp, $sp, -4
    lw $t0, -8($fp)     # arg 1 = array address
    sw $t0, 0($sp)
    jal insertion_sort

    # remove arug
    addi $sp, $sp, 4

    # i = 0
    lw $t0, -4($fp)
    addi $t0, $0, 0
    sw $t0, -4($fp)

loop:
    # while i < len(arr):
    lw $t0, -4($fp)         # $t0 = i
    lw $t1, -8($fp)         # $t1 = array addr
    lw $t2, ($t1)           # $t2 = array.size
    slt $t3, $t0, $t2       # i < len(arr)
    beq $t3, $0, loopexit   # if not i < len(arr), to loopexit


    # print (arr[i], end=" ")
    lw $t0, -8($fp)         # $t0 = array addr
    lw $t1, -4($fp)         # $t1 = i
    addi $t2, $0, 4         # $t2 = 4
    mult $t2, $t1           # $t2 = i * 4
    mflo $t2
    add $t0, $t0, $t2       # $t0 = $t0 + $t2 shift array slot
    lw $t2, 4($t0)          # $t0 = arr[i]
    addi $v0, $0, 1         # print array int
    addi $a0, $t2, 0
    syscall

    addi $v0, $0, 4         # print space between each num
    la $a0, space
    syscall

    # i += 1
    lw $t0, -4($fp)
    addi $t0, $t0, 1
    sw $t0, -4($fp)

    j loop

loopexit:
    # next line
    addi $v0, $0, 4
    la $a0, new_line
    syscall

    # exit
    addi $v0, $0, 10
    syscall
