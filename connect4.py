import threading
import time
import math
from connect4_heuristic import *
from functools import lru_cache
debug = False

def push(col,chip,state):
    if len(state[col]) >= 6:
        return False
    state[col].append(chip)

def check_window(state,chip,i,j):
    state = [s+['o']*(7-len(s)) for s in state]
    # print(state)
    max_count = 0
    count = 0
    if i <= 3: #​Column ฝั่งซ้าย
        count = 0
        for col in range(4):
            if state[i+col][j] == chip: #หา Row เดียวกัน แนวนอน
                count += 1
            elif state[i+col][j] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
    if j >= 3:#Row บน เกิน 4
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

def utility(state,chip):
    # ret=is_win(state,chip)
    new_state = tuple([ tuple( s+['o']*(7-len(s)) ) for s in state])
    state_temp = tuple([ tuple(s) for s in state])
    ret = score_position(new_state,state_temp, chip)
    if debug: #show_state(state)
    if debug: print(ret)
    if chip == 'B':
        return ret
    return -ret
    

def is_win(state,chip):
    max = -1
    for i in range(7):
        for j in range(6):
            ret=check_window(state,chip,i,j)
            if ret[2] > max:
                max = ret[2]
                ans = ret
    return ans

def #show_state(state):
    print()
    state = [s+['o']*(7-len(s)) for s in state]
    for r in range(5,-1,-1):
        str_out = ''
        for c in range(7):
            str_out += state[c][r]
        print(str_out)
    print('1234567')
    # print(state)

max_depth = 12

def min_value_function(state,a,b,level):
    # just pushed black
    if is_win(state,'B')[2] == 4:
        return math.inf
    if level >= max_depth:
        if debug: print('Cutoff',state)
        ret_u = utility(state,'B')
        if debug: print('Utility',ret_u)
        return ret_u
    v=math.inf
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'W',new_state)
        v = min(v,max_value_function(new_state,a,b,level+1))
        if v <= a:
            return v
        if b == math.inf:
            b = v
        else:
            b = min(b,v)
    return v

def max_value_function(state,a,b,level):
    # just pushed white
    if is_win(state,'W')[2] == 4:
        return -math.inf
    v=-math.inf
    # if black can win
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        if is_win(new_state,'B')[2] == 4:
            return math.inf
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        v = max(v,min_value_function(new_state,a,b,level+1))
        if v >= b:
            return v
        if a == -math.inf:
            a = v
        else:
            a = max(a,v)
    return v

def alpha_beta_decision(state):
    global max_depth
    s_res = sum([len(c) for c in list(state)])
    if s_res == 1:#ถ้าเราเป็น Turn ที่สอง
        ind = 0
        for c in list(state):
            if len(c) == 1: #หา Column ที่มี chip อยู่
                if ind == 0:#ถ้าเป็น Colum แรก return 1
                    return 1
                else:
                    return ind-1
            ind += 1
    elif s_res == 0:#ถ้าเราเป็น Turn แรก
        return 3

    max_depth = 4
    # if s_res < 5:
    #     max_depth = 4
    # elif s_res < 12:
    #     max_depth = 6
    # elif s_res < 24:
    #     max_depth = 8
    # else:
    #     max_depth = 10

    print('max_depth', max_depth)     
    max_value = -math.inf
    a,b=-math.inf,math.inf
    min_score=[]
    count_win = 0
    count_lose = 0
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        ret=min_value_function(new_state,a,b,0)
        min_score.append(ret)
        if debug: print('MiniMax Value',ret)
        if debug: show_state(new_state)
        if ret >= max_value:
            max_value=ret
            action = i
        if ret == math.inf:
            count_win += 1
        elif ret == -math.inf:
            count_lose += 1
    if count_win >= 1:
        print('From my calculation, I will win')
    elif count_lose == 7:
        print('From my calculation, you will win')
    print(min_score,action)
    return action

def count_down_thread():
    print('\n5..',end='')
    for i in range(4,-1,-1):
      time.sleep(1)
      if terminate_flag:
        break
      print(str(i)+'..',end='')
    print()

is_white_turn = True
state = ([],[],[],[],[],[],[])
#state=[['B', 'B', 'B','W'], [], ['W', 'W','B'], ['B', 'W','B'], ['W','W'], ['W'], []]
#show_state(state)
while sum([len(c) for c in list(state)]) != 42:
    if is_white_turn:
        c = int(input('Please enter your column:'))
        while len(state[c-1]) == 6:
            print('You cannot put in column',c)
            c = int(input('Please enter your column:'))
        push(c-1,'W',state)
        if is_win(state,'W')[2] == 4:
            print('You win!!!')
            #show_state(state)
            break
        is_white_turn = False
    else:
        ct=threading.Thread(target=count_down_thread)
        terminate_flag=False
        ct.start()
        c = alpha_beta_decision(state)
        print('select: ', c)
        terminate_flag=True
        push(c,'B',state)
        #show_state(state)
        if is_win(state,'B')[2] == 4:
            print('I win!!!')
            break
        is_white_turn = True

print(score_position.cache_info())        