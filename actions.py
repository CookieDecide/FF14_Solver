import time

progress100 = 0
quality100 = 0

def set100(progress, quality):
    global progress100, quality100
    progress100 = progress
    quality100 = quality

def getProgressMultiply(venerationval, musclememoryval):
    mult = 1
    if(venerationval > 0):
        mult += 0.5
    if(musclememoryval > 0):
        mult += 1
    return mult

def getQualityMultiply(innerquietval, innovationval, greatstridesval):
    mult = 1
    if(innovationval > 0):
        mult += 0.5
    if(greatstridesval > 0):
        mult += 1
    return mult

def computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, synthesis, touch, byregot):
    if(synthesis):
        musclememoryval = 0
    else:
        musclememoryval -= 1
    if(touch):
        greatstridesval = 0
    else:
        greatstridesval -= 1

    if(byregot):
        innerquietval = 0
    if(venerationval > 0):
        venerationval -= 1
    if(innovationval > 0):
        innovationval -= 1
    if(wastenotval > 0):
        wastenotval -= 1

    return venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval



def basic_synthesis(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress += progress100 * 1.2 * getProgressMultiply(venerationval, musclememoryval)
    durability -= durabilitycost
    cp -= 0
    quality = quality
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, True, False, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def basic_touch(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress = progress
    durability -= durabilitycost
    cp -= 0
    quality += quality100 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    innerquietval = min(10, innerquietval+1)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def master_mend(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#check for maxdurability
    progress = progress
    durability += 30
    durability = min(durability, maxdurability)
    cp -= 88
    quality = quality
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def waste_not(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#half durability cost for 4 steps
    cp -= 56
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(wastenotval < 4):
        wastenotval = 4
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def veneration(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#+50% synthesis for 4 steps
    cp -= 18
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(venerationval < 4):
        venerationval = 4
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def standard_touch(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#combo basic touch cp=18
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress = progress
    durability -= durabilitycost
    cp -= 32
    quality += quality100 * 1.25 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    innerquietval = min(10, innerquietval+1)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def great_strides(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#+100% touch 3 steps 1 time
    cp -= 32
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(greatstridesval < 3):
        greatstridesval = 3
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def innovation(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#+50% touch for 4 steps
    cp -= 18
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(innovationval < 4):
        innovationval = 4
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def waste_not2(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#half durability cost 8 steps
    cp -= 98
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(wastenotval < 8):
        wastenotval = 8
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def Byregots_blessing(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#innerquiet
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress = progress
    durability -= durabilitycost
    cp -= 24
    quality += quality100 * (1 + innerquietval * 0.2) * getQualityMultiply(0, innovationval, greatstridesval)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, True)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def muscle_memory(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#only on first step, next 5 steps +100% synthesis 1 time
    progress += progress100 * 3 * getProgressMultiply(venerationval, musclememoryval)
    durability -= 10
    cp -= 6
    quality = quality
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, True, False, False)
    if(musclememoryval < 5):
        musclememoryval = 5
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def careful_synthesis(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress += progress100 * 1.5 * getProgressMultiply(venerationval, musclememoryval)
    durability -= durabilitycost
    cp -= 7
    quality = quality
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, True, False, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def manipulation(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#durability +5 for 8 steps
    cp -= 96
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, False, False)
    if(manipulationval < 8):
        manipulationval = 5
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def prudent_touch(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#only when waste not not active
    if(wastenotval > 0):
        return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval
    progress = progress
    durability -= 5
    cp -= 25
    quality += quality100 * 1 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    innerquietval = min(10, innerquietval+1)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def reflect(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#only on first step, innerquality +1
    progress = progress
    durability -= 10
    cp -= 6
    quality += quality100 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, False)
    innerquietval = min(10, innerquietval+2)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def preparatory_touch(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#innerquality +1
    durabilitycost = 20
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress = progress
    durability -= durabilitycost
    cp -= 40
    quality += quality100 * 2 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, False, True, False)
    innerquietval = min(10, innerquietval+2)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def groundwork(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):#only half effective if durability is less than cost
    durabilitycost = 20
    if(wastenotval > 0):
        durabilitycost *= 0.5
    if(durability < durabilitycost):
        progress += progress100 * 1.5 * getProgressMultiply(venerationval, musclememoryval)
    else:
        progress += progress100 * 3 * getProgressMultiply(venerationval, musclememoryval)
    durability -= durabilitycost
    cp -= 18
    quality = quality
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, True, False, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def delicate_synthesis(progress, quality, durability, maxdurability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, innersteps):
    durabilitycost = 10
    if(wastenotval > 0):
        durabilitycost *= 0.5
    progress += progress100 * getProgressMultiply(venerationval, musclememoryval)
    durability -= durabilitycost
    cp -= 32
    quality += quality100 * (1+innerquietval*0.1) * getQualityMultiply(innerquietval, innovationval, greatstridesval)
    venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval = computebuffs(venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval, True, True, False)
    return progress, quality, durability, cp, venerationval, musclememoryval, innerquietval, innovationval, greatstridesval, wastenotval, manipulationval

def getActions():
    actions = [basic_synthesis, basic_touch, master_mend, waste_not, veneration, standard_touch, great_strides, innovation, waste_not2, Byregots_blessing, careful_synthesis, manipulation, preparatory_touch, groundwork, delicate_synthesis]
    return actions

def getFirstActions():
    first_actions = [reflect, muscle_memory]
    return first_actions