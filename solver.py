import actions
import random
import time
import sqlite3
import math

glob_maxsteps = 0
glob_maxprogress = 0
glob_maxquality = 0
glob_maxdurability = 0
glob_cp = 0
glob_miniterations = 0

def checkProgress(progress, cp, steps, maxsteps, maxprogress, durability, manipulationval):
    if(progress >= maxprogress)and(cp>=0):
        return 1, durability, manipulationval
    elif(steps >= maxsteps)or(durability <= 0)or(cp <= 0):
        return 0, durability, manipulationval
    elif(manipulationval > 0):
        manipulationval -= 1
        durability += 5
        return 2, durability, manipulationval
    else:
        return 2, durability, manipulationval

'''
def step(progress, quality, steps, maxsteps, maxprogress, maxquality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval):
    global maximumquality
    actionlist = actions.actions
    if(steps==0):
        for action in actions.first_actions:
            actionlist.append(action)

    for action in random.sample(actionlist, len(actionlist)):
        innersteps = steps
        progressinner, qualityinner, innerdurability, innercp, innervenerationval, innermusclememoryval, innerinnerquietval, innerinnovationval, innergreatstridesval, innerwastenotval, innermanipulationval = action(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps)
        innersteps += 1
        status, innerdurability, innermanipulationval = checkProgress(progressinner, innercp, innersteps, maxsteps, maxprogress, innerdurability, manipulationval)
        if(status == 0):
            #print("Failed")
            continue
        elif(status == 1):
            if(qualityinner > maximumquality):
                maximumquality = qualityinner
                print("Success: " + str(progressinner) + ", " + str(qualityinner))
                print(innersteps)
                print(innercp)
                print(innerdurability)
        elif(status == 2):
            step(progressinner, qualityinner, innersteps, maxsteps, maxprogress, maxquality, innerdurability, maxdurability, innercp, innervenerationval, innermusclememoryval, innerinnerquietval, innerinnovationval, innergreatstridesval, innerwastenotval, innermanipulationval)
'''

def setGlob(maxsteps, maxprogress, maxquality, maxdurability, cp, miniterations):
    global glob_maxsteps, glob_maxprogress, glob_maxquality, glob_maxdurability, glob_cp, glob_miniterations
    glob_maxsteps, glob_maxprogress, glob_maxquality, glob_maxdurability, glob_cp, glob_miniterations = maxsteps, maxprogress, maxquality, maxdurability, cp, miniterations



def computeMacro(macro):#30, 1780, 4600, 80, 80, 563
    maxsteps = glob_maxsteps
    maxprogress = glob_maxprogress
    maxquality = glob_maxquality
    maxdurability = glob_maxdurability
    cp = glob_cp
    progress = 0 
    quality = 0 
    steps = 0 
    venerationval = 0 
    musclememoryval = 0 
    innerquietval = 0 
    innovationval = 0 
    greatstridesval = 0 
    wastenotval = 0 
    manipulationval = 0
    durability = maxdurability
    

    for action in macro:
        progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = action(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, steps)
        steps += 1
        status, durability, manipulationval = checkProgress(progress, cp, steps, maxsteps, maxprogress, durability, manipulationval)
        if(status == 0):
            #print("Failed")
            return progress, quality, steps
        elif(status == 1):
            #if(steps < len(macro)):
            #    return 0, 0, 0
            #print("Success")
            return progress, quality, steps
        elif(status == 2):
            continue
    
    return 0, 0, 0


def simulated_annealing(initial_state):
    """Peforms simulated annealing to find a solution"""
    maxprogress = glob_maxprogress
    maxquality = glob_maxquality

    i = 0
    current_progress = 0
    current_quality = 0
    # Start by initializing the current state with the initial state
    current_state = initial_state
    neighbors = get_neighbors(current_state)

    while ((current_quality < maxquality * 2) or (current_progress < maxprogress)) and (i < 10000):
        for neighbor in neighbors:
            neighbor_progress, neighbor_quality, neighbor_steps = computeMacro(neighbor)
            current_progress, current_quality, current_steps = computeMacro(current_state)

            # if the new solution is better, accept it
            if (neighbor_quality > current_quality) and ((neighbor_progress > maxprogress) or (neighbor_progress > current_progress)):
                current_state = neighbor.copy()
                #print(neighbor_progress)
                #print(neighbor_quality)
                neighbors = get_neighbors(current_state)
                i = 0

            i += 1

    current_progress, current_quality, current_steps = computeMacro(current_state)
    if(current_progress<maxprogress):
        return [], 0, 0, 0
    return current_state, current_steps, current_progress, current_quality
    
def get_neighbors(state):
    """Returns neighbors of the argument state for your solution."""
    neighbors = []

    actionlist = actions.getActions()
    for action in actions.getFirstActions():
        actionlist.append(action)
    
    for action in actionlist:
        neighbor = state.copy()
        neighbor[0] = action
        neighbors.append(neighbor)

    for i in range(1, len(state)):
        for action in actions.getActions():
            neighbor = state.copy()
            neighbor[i] = action
            neighbors.append(neighbor)

    random.shuffle(neighbors)
    return neighbors

def initial():
    job = input("Choose Job:(Alchemist(1),Goldsmith(2),Blacksmith(3),Armorer(4),Culinarian(5),Leatherworker(6),Weaver(7),Carpenter(8))")
    level = input("Choose Recipelevel:")

    con = sqlite3.connect('./DB/recipe.db') 
    cur = con.cursor()
    cur.execute('SELECT * FROM recipe WHERE job = ? AND baseLevel = ?;',(job,level,))
    rows = cur.fetchall()

    index = 0
    for row in rows:
        print([index, row])
        index += 1

    recipeindex = int(input("Choose recipe by index:"))
    recipe = rows[recipeindex]

    print(recipe)

    craftsmanship = int(input("Craftsmanship: "))
    control = int(input("Control: "))

    pprogress = (craftsmanship * 10) / recipe[10] + 2
    pquality = (control * 10) / recipe[12] + 35

    cp = int(input("Maximum CP: "))

    actions.set100(pprogress, pquality)

    return recipe, cp

def main():
    recipe, cp = initial()
    start = time.perf_counter()

    setGlob(100, recipe[1], recipe[4], recipe[2], cp, 100)#maxsteps, maxprogress, maxquality, maxdurability, cp, miniterations

    maximum = [[], 0, 0, 0]
    t=1
    while((maximum[2] < glob_maxprogress) or (maximum[3] < glob_maxquality)) or (t < glob_miniterations):
        steps = 0
        while(steps == 0):
            macro = []
            for i in range(30):
                macro.append(random.choice(actions.getActions()))

            tmpsolution, steps, progress, quality = simulated_annealing(macro)
            solution = []
            for i in range(steps):
                solution.append(tmpsolution[i])

            if(quality > maximum[3]):
                maximum = [solution, steps, progress, quality]
        #print(solution)
        #print(progress)
        #print(quality)
        #print(steps)
        print(t)
        if(t%10==0):
            print(maximum)
        t+=1
        #if((maximum[2] > maxprogress) and (maximum[3] > maxquality)):
        #    break

    print(maximum)

    end = time.perf_counter()
    print(f'Finished in {round(end-start, 2)} second(s)') 
    

if __name__ == '__main__':
    main()