def check_window(state,chip,i,j):
    state = [s+['o']*(7-len(s)) for s in state]
    # print(state)
    max_count = 0
    count = 0
    if i <= 3:
        count = 0
        for col in range(4):
            if state[i+col][j] == chip:
                count += 1
            elif state[i+col][j] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
    if j >= 3:
        count = 0
        for row in range(4):
            if state[i][j-row] == chip:
                count += 1
            elif state[i][j-row] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count

    if i <= 3 and j >= 3:
        count = 0
        for k in range(4):
            if state[i+k][j-k] == chip:
                count += 1
            elif state[i+k][j-k] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
    
    if i <= 3 and j <= 2:
        count = 0
        for k in range(4):
            if state[i+k][j+k] == chip:
                count += 1
            elif state[i+k][j+k] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
        
    # if max_count == 3 and (j == 0 or state[i][j-1] != 'o') and state[i][j] == 'o':
    #    return (i,j,3)
    # if max_count == 3 and state[i][j-1] == 'o':
    #    return (i,j,3)
    return (i,j,max_count)




def feature2_row(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    count = 0
    j = 0
    startIndex = -1

    is_left_adjacent = False
    is_right_adjacent = False
    is_one_adjacent_always = False
    score = 900000
    space_between_index = -1

    # for j in range(6): #Row
    for i in range(7): #Column
        print(state[i][j] , ' chip: ', chip)
        if state[i][j] == chip:
            count += 1
            if startIndex == -1:
                startIndex = i
        elif count > 0 and count < target and state[i][j] == 'o' and ((j-1 >= 0 and state[i][j-1] != 'o') or (j == 0)) and space_between_index == -1:
            space_between_index = i
        elif count < target and state[i][j] != 'o':
            count = 0
            startIndex = -1
        else:
            count = 0
            startIndex = -1
            space_between_index = -1

        #Add special case
        if count == target:
            print('Found target ', chip, ' count ', count)
            break

    if count == target:
        left_adjacent = startIndex - 1
        right_adjacent = startIndex + target
        if space_between_index != -1:
            print('One always adjacent', space_between_index)
            is_one_adjacent_always = True
        else:
            print('Checking left adjacent')
            if left_adjacent >= 0 and state[left_adjacent][j] == 'o':
                print('check left adjacent')
                if j > 0:
                    print('Need to check below row')
                    if state[left_adjacent][j-1] != 'o':
                        print('immediately adjacent left square')
                        is_left_adjacent = True
                else:
                    print('immediately adjacent left square')
                    is_left_adjacent = True

            if right_adjacent < 7 and state[right_adjacent][j] == 'o':
                print('check right adjacent')
                if j > 0:
                    print('Need to check below row')
                    if state[right_adjacent][j-1] != 'o':
                        print('immediately adjacent right square')
                        is_right_adjacent = True
                else:
                    print('immediately adjacent right square')
                    is_right_adjacent = True
    print('is_left_adjacent: ', is_left_adjacent, ' is_right_adjacent: ', is_right_adjacent, ' is_one_adjacent_always: ', is_one_adjacent_always)

    return is_left_adjacent * score + is_right_adjacent * score + is_one_adjacent_always * score




def feature2_column(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    count = 0
    i = 1
    startIndex = -1
    is_top_adjacent = False
    score = 900000
    # for j in range(6): #Row
    for j in range(6): #Column
        print(state[i][j] , ' chip: ', chip)
        if state[i][j] == chip:
            count += 1
            if startIndex == -1:
                startIndex = j
        elif count < target and state[i][j] != 'o':
            count = 0
            startIndex = -1

        if count == target:
            print('Found target ', chip, ' count ', count)
            break

    if count == target:
        print('Checking top adjacent')
        top_adjacent = startIndex + target
        
        if top_adjacent < 6 and state[i][top_adjacent] == 'o':
            print('immediately adjacent top square')
            is_top_adjacent = True
    print('is_top_adjacent: ', is_top_adjacent)

    return is_top_adjacent * score

def feature2_diagonally(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    # count = 0
    # i = 1
    
    score = 900000
    for i in range(6): #Row
        for j in range(6): #Column
            # if i <= 3 and j >= 3:
            #     count = 0
            #     startIndex = -1
            #     for k in reversed(range(4)):
            #         if state[i+k][j-k] == chip:
            #             count += 1
            #         elif state[i+k][j-k] != 'o':
            #             count = 0
            #             break
                    
            #         if count == target:
            #             print('Found target ', chip, ' count ', count)
            #             print('Checking top adjacent')
            #             top_adjacent = startIndex + target
        
            #             if top_adjacent < 6 and state[i][top_adjacent] == 'o':
            #                 print('immediately adjacent top square')
            #                 is_top_adjacent = True
            
            if i <= 3 and j <= 2:
                count = 0
                is_top_adjacent = False
                is_bottom_adjacent = False
                is_one_adjacent_always = False
                empty_index = None
                for k in range(4):
                    print(state[i+k][j+k] , ' chip: ', chip)
                    if state[i+k][j+k] == chip:
                        count += 1
                    elif count > 0 and not is_one_adjacent_always and state[i+k][j+k] == 'o':
                        is_one_adjacent_always = True
                        empty_index = (i+k, j+k)
                    else: #Should start with chip
                        break    

                    if count == target:
                        print('Found target ', chip, ' count ', count)
                        if is_one_adjacent_always and state[empty_index[0]][empty_index[1] -1 ] != 'o' :
                            print(empty_index)
                            return is_one_adjacent_always * score
                        else:
                            top_diagonal_adjacent_row = j + target
                            top_diagonal_adjacent_column = i + target
                            print('Top: ',state[top_diagonal_adjacent_column][top_diagonal_adjacent_row])
                            if top_diagonal_adjacent_row < 6 and top_diagonal_adjacent_column < 7 and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row] == 'o' and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row-1] != 'o':
                                print('immediately adjacent top square')
                                is_top_adjacent = True

                            bottom_diagonal_adjacent_row = j  - 1
                            bottom_diagonal_adjacent_column = i - 1
                            print('Top: ',state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row])
                            if bottom_diagonal_adjacent_row >= 0 and bottom_diagonal_adjacent_column >=0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row] == 'o':
                                if bottom_diagonal_adjacent_row == 0 or (bottom_diagonal_adjacent_row - 1 > 0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row -1] != 'o'):    
                                    print('immediately adjacent top square')
                                    is_bottom_adjacent = True

                            return is_top_adjacent * score + is_bottom_adjacent * score


                        
                               
    
    # if i <= 3 and j <= 2:p
    #     count = 0
    #     for k in range(4):
    #         if state[i+k][j+k] == chip:
    #             count += 1
    #         elif state[i+k][j+k] != 'o':
    #             count = 0
    #             break
    #     if count == 4:
    #         return (i,j,4)
    # if count > max_count:
    #     max_count = count
        
def show_state(state):
    print()
    state = [s+['o']*(7-len(s)) for s in state]
    for r in range(5,-1,-1):
        str_out = ''
        for c in range(7):
            str_out += state[c][r]
        print(str_out)
    print('1234567')


# def is_win(state,chip):
#     max = -1
#     for i in range(7):
#         for j in range(6):
#             # ret=feature2(state,chip,i,j)


# state = ([],[],[],[],[],[],[])
# state=[['B', 'B', 'B','W'], [], ['W', 'W','B'], ['B', 'W','B'], ['W','W'], ['W'], []]

# state=[['B'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #No feature2 row 1
# state=[['B'], ['W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #Only left
# state=state=[['B'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B'], []] #Only right
# state=[['B'], ['W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B'], []] #Both

# state=[['B'], ['W','B'], ['W', 'W','B'], [], ['W','W'], ['B','B','W','W'], []] #One always
# state=[['B'], ['B','W','B'], ['B','W', 'W','B'], ['B'], ['B','W','W'], ['B','B','B','W','W'], ['B']] #One always
# print('score:', feature2_row(state=state, chip='W'))   


# state=[['B'], ['W','B','W','W', 'W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #Column
# print('score:', feature2_column(state=state, chip='W'))

# state=[['B'], ['W','B'], ['W', 'W','B'], [], ['W','W'], ['B','B','W','W'], []]
state=[['W'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W','W','W'], ['B','B','W','W'], []]
print('score:', feature2_diagonally(state=state, chip='B'))