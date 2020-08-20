import copy
from collections import *
import time
from pprint import pprint
import math

class cell:

    def __init__(self,x,y,c):

        self.x = x
        self.y = y
        self.color = c

class Grid_Halma:

    def __init__(self):

        self.state = []

# if the cell is empty or not
def valid_single(state,r,c):
    if not(r >=0 and r<=15):
        return False

    if not(c >=0 and c<=15):
        return False

    if state[r][c] == ".":
        return True
    else:
        return False

def coordinates_in_range(r,c):
    if not(r >=0 and r<=15):
        return False

    if not(c >=0 and c<=15):
        return False

    return True
# To check if there is any player left in our own camp
def check_if_camp_empty(state,player_color):
    still_present_inside = []
    present_outside = []
    player_cells = get_player_coordinates(state,player_color)
    # print player_cells
    if player_color == "W":
        pc = player_camp
    else:
        pc = opponent_camp

    for cell in player_cells:
        if cell in pc:
            still_present_inside.append(cell)
        else:
            present_outside.append(cell)


    return still_present_inside,present_outside

def in_camp(r,c,player_camp):
    if (r,c) in player_camp:
        return True
    else:
        return False

def in_opponent_camp(r,c,opponent_camp):
    # print opponent_camp
    if (r,c) in opponent_camp:
        return True
    else:
        return False


def get_player_coordinates(state,player_color):
    # print player_color
    player = []
    for row in range(0,16):
        for col in range(0,16):

            if state[row][col] == player_color:
                player.append((row,col))

    return player

def is_farther_away(r1,c1,r2,c2,player_color):

    if player_color == "B":
        # if (r1**2 + c1**2) < (r2**2 + c2**2):
        if (r2 >= r1) and (c2 >= c1):
            return True
        else:
            return False
    else:
        if (r2 <= r1) and (c2 <= c1):
            return True
        else:
            return False

def if_player_present(state,r,c):
    if state[r][c] != ".":
        return True
    else:
        return False

def find_valid_jump(state,r,c):

    adjacent_cells = [(r-1,c-1),(r-1,c),(r-1,c+1) , (r+1,c-1),(r+1,c),(r+1,c+1), (r,c-1) , (r,c+1)]
    one_jump_cells = [(r-2,c-2) , (r-2,c),(r-2,c+2) , (r+2,c-2),(r+2,c),(r+2,c+2), (r,c-2) , (r,c+2)]

    valid_moves = []
    for cell,one_jump in zip(adjacent_cells,one_jump_cells):
        r,c  = cell[0],cell[1]
        r_jump,c_jump = one_jump[0],one_jump[1]
        # print r,c,r_jump,c_jump
        if coordinates_in_range(r,c) and if_player_present(state,r,c) and coordinates_in_range(r_jump,c_jump) and not if_player_present(state,r_jump,c_jump):
            valid_moves.append(one_jump)



    return valid_moves


def dfs(state,r,c,visited_jumps,player_color,path,all_paths):
    level_1_jumps = find_valid_jump(state,r,c)
    # print level_1_jumps

    for cell in level_1_jumps:
        # print cell
        if cell not in visited_jumps:
            # print cell
            visited_jumps.add(cell)

            new_state = copy.deepcopy(state)
            new_state[r][c] = "."
            new_state[cell[0]][cell[1]] = player_color

            dfs(new_state,cell[0],cell[1],visited_jumps,player_color,path+[cell],all_paths)

    if path :
        all_paths.append(path)



def play_jump_move(state,r,c,player_color):
    
    visited_jumps = set()
    visited_jumps.add((r,c))

    valid_jump_moves = []
    valid_jump_moves_outside_camp = []

    if state[r][c] == ".":
        return valid_jump_moves_outside_camp, valid_jump_moves



    if player_color == "W":
        pc = player_camp
        oc = opponent_camp
    else:
        pc = opponent_camp
        oc = player_camp

    
    all_paths = []
    dfs(state,r,c,visited_jumps,player_color,[],all_paths)

    # for cell in visited_jumps:
    for cells in all_paths:
        cell = cells[-1]


        if not in_camp(cell[0],cell[1],pc):
            # valid_jump_moves_outside_camp.append((cell[0],cell[1]))
            valid_jump_moves_outside_camp.append(cells)
            # map_jump[cell] = cells

        elif is_farther_away(r,c,cell[0],cell[1],player_color):
            # valid_jump_moves.append((cell[0],cell[1]))
            valid_jump_moves.append(cells)
            # map_jump[cell] = cells

    if in_opponent_camp(r,c,oc):
        valid_jump_moves_inside_opponent = []
        # print valid_jump_moves_outside_camp
        for cells in valid_jump_moves_outside_camp:
            cell = cells[-1]

            if in_opponent_camp(cell[0],cell[1],oc):
                # valid_jump_moves_inside_opponent.append((cell[0],cell[1]))
                valid_jump_moves_inside_opponent.append(cells)
                # map_jump[cell] = cells


        return valid_jump_moves_inside_opponent,valid_jump_moves

    return valid_jump_moves_outside_camp, valid_jump_moves


def play_single_move_when_in_camp(state,r,c,player_color):
    valid_single_moves = []
    valid_single_moves_outside_camp = []

    if state[r][c] == ".":
        return valid_single_moves_outside_camp,valid_single_moves


    if player_color == "W":
        pc = player_camp
        oc = opponent_camp
    else:
        pc = opponent_camp
        oc = player_camp

    # if not in_opponent_camp(r,c,oc):

    if r-1 >= 0:
        if valid_single(state,r-1,c-1) :

            # the single move is outside the camp
            if not in_camp(r-1,c-1,pc):
                valid_single_moves_outside_camp.append([(r-1,c-1)])
            # if single move possible brought it back in thr camp then see if it get farther away
            elif is_farther_away(r,c,r-1,c-1,player_color):
                valid_single_moves.append([(r-1,c-1)])


        if valid_single(state,r-1,c):

            if not in_camp(r-1,c,pc):
                valid_single_moves_outside_camp.append([(r-1,c)])
            elif is_farther_away(r,c,r-1,c,player_color):
                valid_single_moves.append([(r-1,c)])

        if valid_single(state,r-1,c+1):
            if not in_camp(r-1,c+1,pc):
                valid_single_moves_outside_camp.append([(r-1,c+1)])
            elif is_farther_away(r,c,r-1,c+1,player_color):
                valid_single_moves.append([(r-1,c+1)])

    if r+1 <= 15: 
        if valid_single(state,r+1,c-1):
            if not in_camp(r+1,c-1,pc):
                valid_single_moves_outside_camp.append([(r+1,c-1)])
            elif is_farther_away(r,c,r+1,c-1,player_color):
                valid_single_moves.append([(r+1,c-1)])

        if valid_single(state,r+1,c):
            if not in_camp(r+1,c,pc):
                valid_single_moves_outside_camp.append([(r+1,c)])
            elif is_farther_away(r,c,r+1,c,player_color):
                valid_single_moves.append([(r+1,c)])
            
        if valid_single(state,r+1,c+1):
            if not in_camp(r+1,c+1,pc):
                valid_single_moves_outside_camp.append([(r+1,c+1)])
            elif is_farther_away(r,c,r+1,c+1,player_color):
                valid_single_moves.append([(r+1,c+1)])

    # for cell itself
    if valid_single(state,r,c-1) :
        if not in_camp(r,c-1,pc):
            valid_single_moves_outside_camp.append([(r,c-1)])
        elif is_farther_away(r,c,r,c-1,player_color):
            valid_single_moves.append([(r,c-1)])

    if valid_single(state,r,c+1) :
        if not in_camp(r,c+1,pc):
            valid_single_moves_outside_camp.append([(r,c+1)])
        elif is_farther_away(r,c,r,c+1,player_color):
                valid_single_moves.append([(r,c+1)])
    

    if in_opponent_camp(r,c,oc):
        valid_jump_moves_inside_opponent = []
        # print valid_single_moves_outside_camp
        for cells in valid_single_moves_outside_camp:
            cell = cells[-1]
            if in_opponent_camp(cell[0],cell[1],oc):
                valid_jump_moves_inside_opponent.append([(cell[0],cell[1])])

        return valid_jump_moves_inside_opponent,valid_single_moves


    return valid_single_moves_outside_camp,valid_single_moves

def reached_terminal(state):

    black_p = 0
    white_p = 0
    for cell in player_camp:
        if state[cell[0]][cell[1]] == "W":
            white_p +=1
        elif state[cell[0]][cell[1]] == "B":
            black_p += 1

    ply = (black_p > 0) and (white_p+black_p == 19)


    black_o = 0
    white_o = 0
    for cell in opponent_camp:
        if state[cell[0]][cell[1]] == "W":
            white_o +=1
        elif state[cell[0]][cell[1]] == "B":
            black_o += 1

    opp = (white_o > 0) and (white_o+black_o == 19)

    # if ply or opp:
        # print True

    return ply or opp


def pern_dicstance(x1,y1,a,b,c):
    d = (a * x1 + b * y1 + c) /  (math.sqrt(a * a + b * b)) 
    return d
    sm = 0
    for e in emp:
        sm += math.sqrt((e[0]-r)**2 + (e[1]-c)**2)

    return sm

def dist_empty(emp,r,c):
    sm = 0
    for e in emp:
        sm += math.sqrt((e[0]-r)**2 + (e[1]-c)**2)

    return sm

def evalFN(state):

    sm = 0
    sm_b = 0
    sm_w = 0


    a = 1
    b = 1
    c = -15

    b_in_d = 0
    w_in_d = 0

    b_per = 0
    w_per = 0

    b_emp = 0
    w_emp = 0

    sm_b_o = 0
    sm_w_o = 0

    emp_in_player = [cell  for cell in player_camp if (state[cell[0]][cell[1]] == ".")]
    emp_in_opp = [cell  for cell in opponent_camp if (state[cell[0]][cell[1]] == ".")]

    for row in range(0,16):
        for col in range(0,16):

            # dist = pern_dicstance(row,col,a,b,c)
         
            if state[row][col] == "B":
                # sm_b += math.sqrt( (15-row)**2 + (15-col)**2 ) #+ math.sqrt( (7-row)**2 + (7-col)**2 )
                sm_b_o += math.sqrt( (row)**2 + (col)**2 ) 


                if (row,col) not in player_camp:
                    # b_per += dist
                    b_emp += dist_empty(emp_in_player,row,col)

                else:
                    b_in_d+=1

            # elif state[row][col] == "W" and (row,col) not in opponent_camp:
            elif state[row][col] == "W" :
                # sm_w += math.sqrt(row**2 + col**2 ) #+ math.sqrt( (7-row)**2 + (7-col)**2 )
                sm_w_o += math.sqrt((15-row)**2 + (15-col)**2 ) 

                if (row,col) not in opponent_camp:
                    # w_per += dist
                    w_emp += dist_empty(emp_in_opp,row,col)

                else:
                    w_in_d+=1


    if player[0] == "W":
        # return (sm_b - sm_w ) + (w_in_d - b_in_d) + (w_per - b_per)/17.0
        return (w_in_d - b_in_d) +  (b_emp-w_emp)/19.0 + (sm_w_o - sm_b_o)/19.0

        # return sm_b - sm_w + (w_in_d*w_per - b_per*b_in_d)
    else:
        # return (sm_w -sm_b) + (b_in_d - w_in_d) + (w_per - b_per)/17.0
        return (b_in_d - w_in_d) +  (w_emp - b_emp)/19.0 + (sm_b_o - sm_w_o)/19.0
        # return sm_w -sm_b + (b_in_d*b_per - w_in_d*w_per)
    # return sm


def MAX_VALUE(state,player_color,depth,cuttoff,alpha,beta):

    # global total_move
    all_val = []
    # print depth

    if depth == cuttoff or reached_terminal(state):
        # return 0
        return evalFN(state),[]


    val = float("-inf")
    # val = -1*math.inf

    in_camp,out_camp = check_if_camp_empty(state,player_color)
    # print (in_camp,out_camp)

    # if some players present in the camp
    if in_camp:

        
        valid_in = defaultdict(list)
        valid_out = defaultdict(list)

        # t0 = time.time()
        for cell in in_camp:
            
            jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
            single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
            # print single_out,single_in ,jump_out,jump_in

            
            if jump_out:
                valid_out[cell] += jump_out
            if single_out:
                valid_out[cell]+= single_out

            
            if (not single_out and not jump_out) and jump_in:
                valid_in[cell] += jump_in
            
            if (not single_out and not jump_out) and single_in:
                valid_in[cell] += single_in

        # Call DFS recursively on childeren if exist 
        # If there are possible moves to take titles from camp to outside 
        if valid_out:
            # print valid_out
            for cell in valid_out:
                # total_move += len(valid_out[cell])
                for moves in valid_out[cell]:
                    
                    move = moves[-1]

                    # total_move += 1
                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor
                    # print_grid(succ.state)

                    if player_color == "W":
                        mv = MIN_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)
                    else:
                        mv = MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)

                    val = max(val,mv)
                    # else:
                    #     val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))
                    all_val.append((mv,[cell,moves]))


                    if val >= beta:
                        # print "prune"
                        return val,max(all_val)

                    alpha = max(alpha,val)

            

        elif valid_in:
            # print valid_in
            for cell in valid_in:
                for moves in valid_in[cell]:
                    move = moves[-1]
                    # total_move += 1

                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor
                    # print_grid(succ.state)

                    # if player_color == "W":
                    if player_color == "W":
                        mv = MIN_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)
                    else:
                        mv = MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)

                    val = max(val,mv)
                    # else:
                    #     val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))
                    all_val.append((mv,[cell,moves]))

                    # else:
                    #     val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))

                    if val >= beta:
                        # print "prune"
                        return val,max(all_val)

                    alpha = max(alpha,val)

            
# # if no valid move available for the players in camp
        else:
            # valid_in = []
            valid_out = defaultdict(list)
            for cell in out_camp:
                
                jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
                single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
                # print single_out,single_in ,jump_out,jump_in

                if jump_out:
                    valid_out[cell] += jump_out

                if single_out:
                    valid_out[cell] += single_out
                

            # If possible outer move for player outside camp
            if valid_out:
                # print valid_out

                for cell in valid_out:
                    
                    for moves in valid_out[cell]:
                        move = moves[-1]
                        # total_move += 1
                        successor = copy.deepcopy(state)
                        successor[cell[0]][cell[1]] = "."
                        successor[move[0]][move[1]] = player_color
                        succ = Grid_Halma()
                        succ.state = successor
                        # if player_color == "W":
                        if player_color == "W":
                            mv = MIN_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)
                        else:
                            mv = MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)

                        val = max(val,mv)
                        # else:
                        #     val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))
                        all_val.append((mv,[cell,moves]))

                        # else:
                            # val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))
                        if val >= beta:
                            # print "prune"
                            return val,max(all_val)
                        alpha = max(alpha,val)

            # Terminal reached no possibe move
            # else:
            #     print "Terminal reached"
            #     return

    # All players outside the camp    
    else: 

        valid_out = defaultdict(list)

        for cell in out_camp:
            
            jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
            single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
            # print single_out,single_in ,jump_out,jump_in
            if jump_out:
                valid_out[cell] += jump_out

            if single_out:
                valid_out[cell] += single_out
            

        # print sum([len(valid_out[i]) for i in valid_out]),sum([len(valid_in[i]) for i in valid_in])
        # print valid_out

        # If possible outer move for player outside camp
        if valid_out:
            # print valid_out
            for cell in valid_out:
                for moves in valid_out[cell]:
                    move = moves[-1]
                    # total_move += 1

                    
                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor
                    

                    # if player_color == "W":
                    if player_color == "W":
                        mv = MIN_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)
                    else:
                        mv = MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)

                    val = max(val,mv)
                    # else:
                    #     val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))
                    all_val.append((mv,[cell,moves]))

                    # else:
                        # val = max(val,MIN_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta))

                    if val >= beta:
                        # print "prune"
                        return val,max(all_val)

                    alpha = max(alpha,val)

    

    # print (all_val)
    return val,max(all_val)



def MIN_VALUE(state,player_color,depth,cuttoff,alpha,beta):
    # global total_move
    in_camp,out_camp = check_if_camp_empty(state,player_color)
    # print (in_camp,out_camp)
    # print depth
    if depth == cuttoff or reached_terminal(state):
        # return 0
        return evalFN(state)

    val = float("inf")

    # if some players present in the camp
    if in_camp:
        valid_in = defaultdict(list)
        valid_out = defaultdict(list)

        # t0 = time.time()
        for cell in in_camp:
            
            jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
            single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
            # print single_out,single_in ,jump_out,jump_in

            if jump_out:
                valid_out[cell] += jump_out

            if single_out:
                valid_out[cell]+= single_out

            
            if (not single_out and not jump_out) and jump_in:
                valid_in[cell] += jump_in


            if (not single_out and not jump_out) and single_in:
                valid_in[cell] += single_in

            
        # Call DFS recursively on childeren if exist 
        # If there are possible moves to take titles from camp to outside 
        if valid_out:
            # print valid_out
            for cell in valid_out:
                # total_move += len(valid_out[cell])
                for moves in valid_out[cell]:
                    move = moves[-1]
                    # total_move += 1
                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor
                    # print_grid(succ.state)

                    # if player_color == "W":
                        # val = min(val,MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta))
                    # else:
                    if player_color == "B":
                        mv = MAX_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)[0]
                    else:
                        mv = MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)[0]

                    # print mv
                    val = min(val,mv)

                    if val <= alpha:
                        # print "min prune"
                        return val

                    beta  = min(beta,val)

        elif valid_in:
            # print valid_in
            for cell in valid_in:
                for moves in valid_in[cell]:
                    move = moves[-1]
                    # total_move += 1
                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor
                    # print_grid(succ.state)

                    # if player_color == "W":
                    #     val = min(val,MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta))
                    # else:
                    if player_color == "B":
                        mv = MAX_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)[0]
                    else:
                        mv = MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)[0]


                    # print mv
                    val = min(val,mv)

                    if val <= alpha:
                        # print "min prune"
                        return val

                    beta  = min(beta,val)
            
# # if no valid move available for the players in camp
        else:
            # valid_in = []
            valid_out = defaultdict(list)
            for cell in out_camp:
                
                jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
                single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
                # print single_out,single_in ,jump_out,jump_in

                if jump_out:
                    valid_out[cell] += jump_out

                if single_out:
                    valid_out[cell] += single_out
                

            # If possible outer move for player outside camp
            if valid_out:
                # print valid_out

                for cell in valid_out:
                    
                    for moves in valid_out[cell]:
                        move = moves[-1]
                        # total_move += 1
                        successor = copy.deepcopy(state)
                        successor[cell[0]][cell[1]] = "."
                        successor[move[0]][move[1]] = player_color
                        succ = Grid_Halma()
                        succ.state = successor
                        # if player_color == "W":
                        #     val = min(val,MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta))
                        # else:
                        if player_color == "B":
                            mv = MAX_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)[0]
                        else:
                            mv = MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)[0]


                        # print mv
                        val = min(val,mv)

                        if val <= alpha:
                            # print "min prune"
                            return val

                        beta  = min(beta,val)

            # Terminal reached no possibe move
            # else:
            #     print "Terminal reached"
            #     return
    # All players outside the camp    
    else:

        valid_out = defaultdict(list)
        for cell in out_camp:
            
            jump_out,jump_in = play_jump_move(state,cell[0],cell[1],player_color)
            single_out,single_in = play_single_move_when_in_camp(state,cell[0],cell[1],player_color)
            # print single_out,single_in ,jump_out,jump_in

            if jump_out:
                valid_out[cell] += jump_out

            if single_out:
                valid_out[cell] += single_out
            
        # If possible outer move for player outside camp
        if valid_out:
            # print valid_out
            for cell in valid_out:
                for moves in valid_out[cell]:
                    move = moves[-1]
                    # total_move += 1
                    successor = copy.deepcopy(state)
                    successor[cell[0]][cell[1]] = "."
                    successor[move[0]][move[1]] = player_color
                    succ = Grid_Halma()
                    succ.state = successor

                    # if player_color == "W":
                    #     val = min(val,MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta))
                    # else:

                    if player_color == "B":
                        mv = MAX_VALUE(succ.state,"W",depth+1,cuttoff,alpha,beta)[0]
                    else:
                        mv = MAX_VALUE(succ.state,"B",depth+1,cuttoff,alpha,beta)[0]


                    # print mv
                    val = min(val,mv)

                    if val <= alpha:
                        # print "min prune"
                        return val

                    beta  = min(beta,val)

    return val


def print_grid(grid):

    for r_ind,r in enumerate(grid):
        for c_ind,c in enumerate(grid[r_ind]):
            print grid[r_ind][c_ind],
        print 




if __name__ == "__main__":

    input_filename = "input.txt"
   
    color_map = {"W":"WHITE" , "B" : "BLACK"}

    input_f=open(input_filename, "r")

    input = input_f.readlines()

    mode = input[0].strip()
    player = input[1].strip()
    time_game = input[2].strip()

    grid = Grid_Halma()

    player_cells = set()
    opponent_cells = set()

    for i in range(3,19):
        grid.state.append([])

        r = i-3
        for c,color in enumerate(input[i].strip()):


            grid.state[r].append(color)

            if color != "." and color_map[color] == player :
                player_cells.add((r,c))
            elif color != ".":
                opponent_cells.add((r,c))


    opponent_camp = set([(0,0),(0,1),(0,2),(0,3),(0,4),
                         (1,0),(1,1),(1,2),(1,3),(1,4),
                         (2,0),(2,1),(2,2),(2,3), 
                         (3,0),(3,1),(3,2),
                         (4,0),(4,1)]
                     )
    # player_camp = [(15-c[0],15-c[1]) for c in opponent_cells]

    player_camp = set([(15, 13), (13, 13), (14, 13), (11, 14), (15, 12), (13, 12), (12, 13), (15, 11), (14, 14), (15, 15), (12, 14), (13, 15), (14, 15), (15, 14), (14, 11), (12, 15), (13, 14), (14, 12), (11, 15)])
    



    if mode == "SINGLE":
        to_depth = 1
    else:
        to_depth=  2

    f = open("output.txt","w+")

    if player == "WHITE":
        evl,a = MAX_VALUE(grid.state,"W",0,to_depth,float("-inf"),float("inf"))
        _,a = a
        curr,move = a

        move_last = move[-1]

        if len(move) == 1:
            if curr[1]-move_last[1] <= 1 and curr[0]-move_last[0] <= 1:
                f.write("E "+ str(curr[1]) + ","+ str(curr[0]) +" "+ str(move_last[1])+","+str(move_last[0]))
                f.close()
            else:
                f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move_last[1])+","+str(move_last[0]))
                f.close()
        else:

            for c in move[:-1]:
                move_last = c
                f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move_last[1])+","+str(move_last[0]) + "\n")

                curr = c

            f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move[-1][1])+","+str(move[-1][0]))
            f.close()

    else:

        evl,a = MAX_VALUE(grid.state,"B",0,to_depth,float("-inf"),float("inf"))
        _,a = a
        curr,move = a

        move_last = move[-1]

        if len(move) == 1:
            if max(abs(curr[1]-move_last[1]) , abs(curr[0]-move_last[0])) == 1:
                f.write("E "+ str(curr[1]) + ","+ str(curr[0]) +" "+ str(move_last[1])+","+str(move_last[0]))
                f.close()
            else:
                f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move_last[1])+","+str(move_last[0]))
                f.close()
        else:

            for c in move[:-1]:
                move_last = c
                f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move_last[1])+","+str(move_last[0]) + "\n")

                curr = c

            f.write("J "+str(curr[1]) + ","+ str(curr[0]) +" "+str(move[-1][1])+","+str(move[-1][0]))
            f.close()

