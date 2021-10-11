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




def feature2(state,chip):#Find 3 connected
    state = [s+['o']*(7-len(s)) for s in state]
    show_state(state)
    target = 3
    count = 0
    j = 1
    startIndex = 0
    # for j in range(6): #Row
    for i in range(7): #Column
        print(state[i][j] , ' chip: ', chip)
        if state[i][j] == chip:
            count += 1
            if startIndex == 0:
                startIndex = i
        elif count < target and state[i][j] != 'o':
            count = 0

        if count == target:
            print('Found target ', chip, ' count ', count)
            break

    #Calculate Score
    is_left_adjacent = False
    is_right_adjacent = False
    if count == target:
        print('Checking left adjacent')
        left_adjacent = startIndex - 1
        right_adjacent = startIndex + target
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
    print('is_left_adjacent: ', is_left_adjacent, ' is_right_adjacent: ', is_right_adjacent)


def show_state(state):
    print()
    state = [s+['o']*(7-len(s)) for s in state]
    for r in range(5,-1,-1):
        str_out = ''
        for c in range(7):
            str_out += state[c][r]
        print(str_out)
    print('1234567')


def is_win(state,chip):
    max = -1
    for i in range(7):
        for j in range(6):
            ret=feature2(state,chip,i,j)


# state = ([],[],[],[],[],[],[])
# state=[['B', 'B', 'B','W'], [], ['W', 'W','B'], ['B', 'W','B'], ['W','W'], ['W'], []]

# state=[['B'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #No feature2 row 1
# state=[['B'], ['W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B','B','W','W'], []] #Only left
# state=state=[['B'], ['W','B'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B'], []] #Only right
state=[['B'], ['W'], ['W', 'W','B'], ['B', 'W','B','B'], ['W','W'], ['B'], []] #Both
# print(is_win(state,'W'))     
feature2(state=state, chip='W')