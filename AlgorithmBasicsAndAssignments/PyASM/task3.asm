
    .data
smashed_prompt1:.asciiz "Hulk smashed "
smashed_prompt2:.asciiz " people"
smash:          .asciiz "Hulk SMASH! >:(\n"
sad:            .asciiz "Hulk Sad :(\n"
new_line:       .asciiz "\n"
.globl smash_or_sad
.globl main


    .text

    j main

# def smash_or_sad(the_list: List[int], hulk_power: int) -> int:
smash_or_sad:
    # save $ra and $fp in stack
    addi $sp, $sp, -8   # make space
    sw $ra, 4($sp)      # save $ra
    sw $fp, 0($sp)      # save $fp
    addi $fp, $sp, 0    # copy $fp to $fp

    # smash_count = 0
    addi $sp, $sp, -8       # Allocate 8 bytes (smash_count & i) of local var

    # -8($fp) is smash_count
    # -4($fp) is i

loop:
    # while i < len(the_list):
    lw $t0, -4($fp)     # $t0 = i
    lw $t1, 8($fp)      # $t1 = array addr
    lw $t2, ($t1)       # $t2 = array.size
    slt $t3, $t0, $t2       # i < len(the_list)
    beq $t3, $0, loopexit   # if not i < len(the_list), to loopexit

    # if the_list[i] <= hulk_power (not hulk_power > the_list[i]):
    lw $t0, 12($fp)     # $t0 = param hulk_power
    lw $t1, -4($fp)     # $t1 = i
    lw $t2, 8($fp)      # $t2 = array addr
    addi $t3, $0, 4     # $t3 = 4
    mult $t3, $t1       # $t4 = i * 4
    mflo $t4
    add $t2, $t2, $t4   # $t2 = $t2 + $t4 shift array slot
    lw $t2, 4($t2)      # $t2 = the_list[i]
    slt $t5, $t0, $t2   # $t5 = hulk_power > the_list[i]
    bne $t5, $0, else   # if hulk_power > the_list[i] == 1, to else

    # print("Hulk SMASH! >:(")
    addi $v0, $0, 4
    la $a0, smash
    syscall

    # smash_count += 1
    lw $t0, -8($fp)     # $t0 = smash_count
    addi $t0, $t0, 1    # $t0 = smash_count + 1
    sw $t0, -8($fp)     # smash_count = $t0

    j endif

else:
    # print("Hulk Sad :(")
    addi $v0, $0, 4
    la $a0, sad
    syscall

endif:

    # update i
    lw $t0, -4($fp)     # $t0 = i
    addi $t0, $t0, 1    # $t0 = i + 1
    sw $t0, -4($fp)     # i = $t0

    j loop

loopexit:

    # return smash_count
    lw $v0, -8($fp) # $v0 = smash_count

    addi $sp, $sp, 8    # remove local var
    lw $fp, 0($sp)      # restore $fp
    lw $ra, 4($sp)      # restore $ra
    addi $sp, $sp, 8    # deallocate

    jr $ra



main:
    # set $fp and make space for locals
    addi $fp, $sp, 0        # copy $sp into $fp
    addi $sp, $sp, -8       # Allocate 8 bytes (my_list & hulk_power) of local var

    # my_list = [10, 14, 16]
    addi $v0, $0, 9         # allocate space
    addi $a0, $0, 16        # (3 * 4) + 4
    syscall
    sw $v0, -8($fp)         # -8($fp) = address
    addi $t0, $0, 3         # $t0 = 3
    sw $t0, ($v0)           # -8($fp).length = 3
    # assign array value
    lw $t0, -8($fp)         # $t0 = address
    addi $t1, $0, 10
    sw $t1,  4($t0)         # -8($fp)[0] = 10
    addi $t1, $0, 14
    sw $t1,  8($t0)         # -8($fp)[1] = 14
    addi $t1, $0, 16
    sw $t1, 12($t0)         # -8($fp)[2] = 16

    # hulk_power = 15
    addi $t0, $0, 15
    sw $t0, -4($fp)         # -4($fp) = 15

    # call smash_or_sad(the_list, hulk_power), 2var: (2*4) of arug
    addi $sp, $sp, -8
    lw $t0, -8($fp)     # arg 1 = array address
    sw $t0, 0($sp)
    lw $t0, -4($fp)     # arg 2 = hulk_power
    sw $t0, 4($sp)
    jal smash_or_sad

    # remove arug
    addi $sp, $sp, 8

    addi $t0, $v0, 0    # $t0 = function return

    # print(f"Hulk smashed
    addi $v0, $0, 4
    la $a0, smashed_prompt1
    syscall

    # print the return value from smash_or_sad
    addi $v0, $0, 1
    addi $a0, $t0, 0
    syscall

    #  people")
    addi $v0, $0, 4
    la $a0, smashed_prompt2
    syscall


    # exit
    addi $v0, $0, 10
    syscall
