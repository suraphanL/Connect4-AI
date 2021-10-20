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
    total_score = 0
    score = 900000
    for j in range(6): #Row
        count = 0
        startIndex = -1
        space_between_index = -1
        is_left_adjacent = False
        is_right_adjacent = False
        is_one_adjacent_always = False
        
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
            if is_left_adjacent and is_right_adjacent:
                return float('inf')
            else:
                return is_left_adjacent * score + is_right_adjacent * score + is_one_adjacent_always * score 
    return 0

def feature2_column(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    score = 900000
    for i in range(6): #Row
        count = 0
        startIndex = -1
        is_top_adjacent = False
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
    return 0

def feature2_diagonally(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    
    score = 900000
    for i in range(7): #Row
        for j in range(6): #Column
            count = 0
            is_top_adjacent = False
            is_bottom_adjacent = False
            is_one_adjacent_always = False
            empty_index = None
            startIndex = -1
            if i <= 3 and j >= 3:
                print(i,j)
                for k in reversed(range(4)):
                    print(state[i+k][j-k] , ' chip: ', chip)
                    print( (i+k), (j-k))
                    if state[i+k][j-k] == chip:
                        count += 1
                        if startIndex == -1:
                            startIndex = k
                    elif count > 0 and not is_one_adjacent_always and state[i+k][j-k] == 'o':
                        is_one_adjacent_always = True
                        empty_index = (i+k, j-k)
                    else:
                        count = 0
                        startIndex = -1    
                        is_one_adjacent_always = False
                        empty_index = None    
                    
                    if count == target:
                        print('Found target ', chip, ' count ', count)

                        if is_one_adjacent_always:
                            if state[empty_index[0]][empty_index[1] -1 ] != 'o':
                                return is_one_adjacent_always * score
                            else:
                                count_token = 0
                                for token in state[empty_index[0]]:
                                    if token != 'o':
                                        count_token+=1
                                    else:
                                        break
                                if count_token == empty_index[1] -1:
                                    print(empty_index)
                                    return is_one_adjacent_always * score
                        else:
                            top_diagonal_adjacent_row = j - startIndex + target
                            top_diagonal_adjacent_column = i + startIndex - target
                            print('Top: ',state[top_diagonal_adjacent_column][top_diagonal_adjacent_row])
                            if top_diagonal_adjacent_row < 6 and top_diagonal_adjacent_column < 7 and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row] == 'o' and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row-1] != 'o':
                                print('immediately adjacent top square')
                                is_top_adjacent = True

                            bottom_diagonal_adjacent_row = j - startIndex - 1
                            bottom_diagonal_adjacent_column = i + startIndex + 1
                            print('Top: ',state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row])
                            if bottom_diagonal_adjacent_row >= 0 and bottom_diagonal_adjacent_column >=0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row] == 'o':
                                if bottom_diagonal_adjacent_row == 0 or (bottom_diagonal_adjacent_row - 1 > 0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row -1] != 'o'):    
                                    print('immediately adjacent top square')
                                    is_bottom_adjacent = True

                            return is_top_adjacent * score + is_bottom_adjacent * score


            
            if i <= 3 and j <= 2:
                for k in range(4):
                    print(state[i+k][j+k] , ' chip: ', chip)
                    if state[i+k][j+k] == chip:
                        count += 1
                        if startIndex == -1:
                            startIndex = k
                    elif count > 0 and not is_one_adjacent_always and state[i+k][j+k] == 'o':
                        is_one_adjacent_always = True
                        empty_index = (i+k, j+k)
                    else: #Should start with chip
                        count = 0
                        startIndex = -1    
                        is_one_adjacent_always = False
                        empty_index = None

                    if count == target:
                        print('Found target ', chip, ' count ', count)
                        if is_one_adjacent_always:
                            if state[empty_index[0]][empty_index[1] -1 ] != 'o':
                                return is_one_adjacent_always * score
                            else:
                                count_token = 0
                                for token in state[empty_index[0]]:
                                    if token != 'o':
                                        count_token+=1
                                    else:
                                        break
                                if count_token == empty_index[1] -1:
                                    print(empty_index)
                                    return is_one_adjacent_always * score
                        else:
                            top_diagonal_adjacent_row = j + startIndex + target
                            top_diagonal_adjacent_column = i + startIndex + target
                            print('Top: ',state[top_diagonal_adjacent_column][top_diagonal_adjacent_row])
                            if top_diagonal_adjacent_row < 6 and top_diagonal_adjacent_column < 7 and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row] == 'o' and state[top_diagonal_adjacent_column][top_diagonal_adjacent_row-1] != 'o':
                                print('immediately adjacent top square')
                                is_top_adjacent = True

                            bottom_diagonal_adjacent_row = j + startIndex  - 1
                            bottom_diagonal_adjacent_column = i + startIndex - 1
                            print('Top: ',state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row])
                            if bottom_diagonal_adjacent_row >= 0 and bottom_diagonal_adjacent_column >=0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row] == 'o':
                                if bottom_diagonal_adjacent_row == 0 or (bottom_diagonal_adjacent_row - 1 > 0 and state[bottom_diagonal_adjacent_column][bottom_diagonal_adjacent_row -1] != 'o'):    
                                    print('immediately adjacent top square')
                                    is_bottom_adjacent = True

                            return is_top_adjacent * score + is_bottom_adjacent * score
    return 0

                        
                               
    
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
        
def feature3_row(state,chip):#Find 2 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 2
    total_score = 0
    
    for j in range(6): #Row
        target_count = 0
        space_before_count = 0
        space_after_count = 0
        startIndex = -1
        
        for i in range(7): #Column
            print(state[i][j] , ' chip: ', chip)
            if state[i][j] == chip:
                target_count += 1
                if startIndex == -1:
                    startIndex = i
            elif state[i][j] != chip and state[i][j] != 'o': #Opponent
                target_count = 0
                space_before_count = 0
                space_after_count = 0
                startIndex = -1
            elif state[i][j] == 'o':
                if j == 0 or state[i][j-1] != 'o':
                    space_before_count +=1

                
            if target_count == target:
                print('i,j',i,j)
                print('Found target ', chip, ' count ', target_count)
                for after in range(i+1,7):
                    print('After: ', after)
                    print(state[after][j])
                    if state[after][j] == 'o':
                        if j == 0 or state[after][j-1] != 'o':
                            space_after_count +=1
                    else:
                        break       
                number_of_available_squares = space_before_count + space_after_count 
                print('Result: ', number_of_available_squares)
                total_score += feature3_score(number_of_available_squares)
                break
    print('total score:', total_score)
    return total_score

def show_state(state):
    print()
    state = [s+['o']*(7-len(s)) for s in state]
    for r in range(5,-1,-1):
        str_out = ''
        for c in range(7):
            str_out += state[c][r]
        print(str_out)
    print('1234567')

def feature3_score(number_of_available_squares):
    if number_of_available_squares >=5:
                    return 40000
    elif number_of_available_squares == 4:
        return 30000
    elif number_of_available_squares == 3:
        return 20000
    elif number_of_available_squares == 2:
        return 10000               
    else:
        return 0
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
# state=[['W'], ['W'], ['W'], [], ['W', 'W'], ['W', 'W'], ['W', 'W']] #One always
# print('score:', feature2_row(state=state, chip='W'))   


# state=[['B'], ['W','B','W','W', 'W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #Column
# print('score:', feature2_column(state=state, chip='W'))

# state=[['B'], ['W','B'], ['W', 'W','B'], ['B', 'W', 'B', 'B'], ['W','W'], ['B','B','W','W'], []]
# state=[['W'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W','W','W'], ['B','B','W','W'], []]
# state=[['W','W','W','B'], ['W','W','B'], ['W','B'], [], ['W','W','W','W'], ['B','B','W','W'], []] #dia first, Case start empty
# state=[['W','W','W'], ['W','W','B'], ['W','B'], ['B'], ['W','W','W','W'], ['B','B','W','W'], []] #dia first, Case start 
# state=[['W','W',], ['W','W','W','B'], ['W', 'W','W', 'W','B'], ['W','W', 'W','W', 'W','B'], ['W','W'], ['B','B','W','W'], []] #dia second, Case start empty
# state=[['B'], ['W'], ['B', 'W'], ['W', 'W'], ['B','B','W','W'], ['W'], []] #Special case feature 2, 1
# state=[['B','B','W','W'], ['W'], ['B', 'W'], ['W'], [], ['W'], []] #Special case feature 2, 2
# state=[['B','B','W'], ['W','W','W'], ['B', 'W'], ['W'], [], ['W'], []] #Special case feature 2, 2 start empty
# print('score:', feature2_diagonally(state=state, chip='W'))

# state=[[], [], ['B'], ['B'], [], ['W'], ['W']] #Fig 9 Left
# state=[[], ['W', 'B'], ['B', 'B'], ['W'], ['B'], ['W'], ['B', 'W']] #Fig 9 Middle
# state=[[], ['W', 'B'], ['B', 'B'], ['W', 'W'], ['B'], ['W'], ['B', 'W']] #Fig 9 Right
state=[[], [], ['B'], ['B'], ['W'], ['W', 'B'], ['W', 'B']] #Fig 9 Left with modification for test 2 2 connected
print('score:', feature3_row(state=state, chip='B'))
