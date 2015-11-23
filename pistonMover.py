import bpy as bge
import COM
import vol

def calc_com():
    '''Calculate the Center of Mass inside game-engine'''
    obj_list_real = []
    for item in bge.logic.getCurrentScene().objects:
        try:
            if item.name.startswith('Cube') and item.name != 'Cube.004':
                temp_dict = {}
                temp_dict['x'] = item.worldPosition.x
                temp_dict['y'] = item.worldPosition.y
                temp_dict['z'] = item.worldPosition.z                   
                temp_dict['mass'] = item.mass
                obj_list_real.append(temp_dict)
            if item.name.startswith('obj_'):
                temp_dict = {}
                temp_dict['x'] = item.worldPosition.x
                temp_dict['y'] = item.worldPosition.y
                temp_dict['z'] = item.worldPosition.z                     
                temp_dict['mass'] = item.mass
                obj_list_real.append(temp_dict)
        except AttributeError:
            pass    
    com = COM.COM(obj_list_real)
    print("COM_after::"+str(com))
    return com

def get_vol_positions():
    '''Get the postions of the objects for calculating volume'''
    positions = {}
    for item in bge.logic.getCurrentScene().objects:         
        if item.name == "Cube":
            positions['h1'] = item.worldPosition.z
        if item.name == "Cube.003":
            positions['h2'] = item.worldPosition.z
        if item.name == "Cube.002":
            positions['b1'] = item.worldPosition.x
        if item.name == "Cube.001":
            positions['b2'] = item.worldPosition.x
        if item.name == "Cube.004":
            positions['l1'] = item.worldPosition.y
        if item.name == "Cylinder":
            positions['l2'] = item.worldPosition.y
    return positions

def getPistonpos():
    ''' Get the piston postion in the scene inside game-engine'''
    pistonpos = 0
    for item in bge.logic.getCurrentScene().objects:
        if item.name == "Cylinder":
            pistonpos = item.worldPosition.y
            break
    return pistonpos

def main():
    '''Triggered when the game-engine is started'''
    cont = bge.logic.getCurrentController()
    player = cont.owner
    scene = bge.logic.getCurrentScene()
    keyboard = bge.logic.keyboard
    player.localPosition.y -= 0.1
    pistonpos = 0
    flag = False
    gameactu = cont.actuators['actuator1']
    try:
        pistonpos = bge.logic.globalDict['pistonpos']
        flag = True
    except KeyError:
        bge.logic.globalDict['pistonpos'] = getPistonpos()
    posdiff = abs(getPistonpos() - pistonpos)
    if posdiff < 0.0001 and flag:
        print(posdiff)
        try:
            if bge.logic.globalDict['trials'] > 1:
                calc_com()
                v = vol.volume(get_vol_positions())
                print("VOL_after::"+str(v))
                cont.activate(gameactu)
            else:
                bge.logic.globalDict['trials'] += 1
        except:
            bge.logic.globalDict['trials'] = 1
        
    bge.logic.globalDict['pistonpos'] = getPistonpos()
    if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.DOWNARROWKEY]:
        calc_com()
    
main()