import bpy
import math as m
import random as rand
import divider as d
import COM
import vol

def del_existing():
    """Remove existing objects from the scene"""
    del_obj = [item.name for item in bpy.data.objects if item.type == "MESH" or "LAMP"]
    for obj in del_obj:
        bpy.data.objects[obj].select = True
    bpy.ops.object.delete()

def makeMaterial(name, diffuse, specular, alpha,transpar=False):
    """Make a material based on diffuse, specular and alpha values """
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'PHONG'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    if transpar:
        mat.use_transparency = True
    return mat

def setMaterial(ob, mat):
    """Sets the material property to an object"""
    me = ob.data
    me.materials.append(mat)

def add_lamp(lname,srctype,location):
    """Add a lamp to scene for a given source and location"""
    scene = bpy.context.scene
    newl = bpy.data.lamps.new(name=lname,type=srctype)
    objl = bpy.data.objects.new(name=lname, object_data = newl)
    scene.objects.link(objl)
    objl.location=location
    #print(list(bpy.data.objects))
    bpy.data.objects[lname].select = True
    bpy.data.objects["hemi"].data.energy = 0.9


def add_camera():
    """Add a camera to scene at a fixed location"""
    cam = bpy.ops.object.camera_add(view_align=True, location=(0.0,34,20.0),rotation=(m.radians(50), 0.0, m.radians(180)))
    
def create_some_object(ii,y_co,mass):
    """Create a random object with random diffuse and specular coefficients"""
    name = ''
    diff = (rand.uniform(0,1),rand.uniform(0,1),rand.uniform(0,1))
    spec = (rand.uniform(0,1),rand.uniform(0,1),rand.uniform(0,1))
    alp = rand.uniform(0,1)
    if ii % 5 == 0:
        x_co = 8.1
        name =  "obj_torus"+str(ii)
        bpy.ops.mesh.primitive_torus_add(location = (x_co,y_co,2))
        selobj = bpy.context.active_object
        selobj.name = name
        selobj.game.mass = mass
        selobj.scale = (1.5,1.5,1.5)
    if ii % 5 == 1:
        x_co = 3.5
        name =  "obj_cube"+str(ii)
        bpy.ops.mesh.primitive_cube_add(location = (x_co,y_co,2))
        selobj = bpy.context.active_object
        selobj.name = name
        selobj.game.mass = mass
        selobj.scale = (2,2,2)
    if ii % 5 == 2:
        x_co =-1
        name =  "obj_cone"+str(ii)
        bpy.ops.mesh.primitive_cone_add(location = (x_co,y_co,2))
        selobj = bpy.context.active_object
        selobj.name = name
        selobj.game.mass = mass
        selobj.scale = (2,2,2)
    if ii % 5 == 3:
        x_co = -5.4
        name =  "obj_sphere"+str(ii)
        bpy.ops.mesh.primitive_uv_sphere_add(location = (x_co,y_co,2))
        selobj = bpy.context.active_object
        selobj.name = name
        selobj.game.mass = mass
        selobj.scale = (2,2,2)
    if ii % 5 == 4:
        x_co = -9.0
        name =  "obj_monkey"+str(ii)
        bpy.ops.mesh.primitive_monkey_add(location = (x_co,y_co,2))
        selobj = bpy.context.active_object
        selobj.name = name
        selobj.game.mass = mass
        selobj.scale = (1.2,1.2,1.2)
    tempmat = makeMaterial(name, diff, spec, alp)
    setMaterial(bpy.context.active_object,tempmat)

def create_logic_bricks():
    """This method creates the game engine logic bricks for our scene"""
    sensors = bpy.context.scene.objects['Cylinder'].game.sensors
    controllers = bpy.context.scene.objects['Cylinder'].game.controllers
    actuators = bpy.context.scene.objects['Cylinder'].game.actuators
    bpy.ops.logic.sensor_add(type='ALWAYS', object="Cylinder",name="sensor1")
    sensors['sensor1'].use_pulse_true_level = True
    bpy.ops.logic.controller_add(type='PYTHON',object="Cylinder",name="controller1")
    controllers['controller1'].text = bpy.data.texts['pistonMover.py']
    sensors['sensor1'].link(controllers['controller1'])
    bpy.ops.logic.actuator_add(type="GAME",object="Cylinder",name="actuator1")
    actuators['actuator1'].mode = "QUIT"
    controllers['controller1'].link(actuator = actuators['actuator1'])
    bpy.context.scene.game_settings.logic_step_max = 50
    bpy.context.scene.game_settings.physics_step_max = 50
    bpy.context.scene.game_settings.physics_step_sub = 5

def get_volume_params():
    """Returns the co-ordinates of the compression chamber(or box) """
    positions = {}
    for item in bpy.data.objects:         
        if item.name == "Cube":
            positions['h1'] = item.location.z
        if item.name == "Cube.003":
            positions['h2'] = item.location.z
        if item.name == "Cube.002":
            positions['b1'] = item.location.x
        if item.name == "Cube.001":
            positions['b2'] = item.location.x
        if item.name == "Cube.004":
            positions['l1'] = item.location.y
        if item.name == "Cylinder":
            positions['l2'] = item.location.y
    return positions


def make_chamber():
    '''Create a box like structure which is used to pack the objects'''
    plane_mat = makeMaterial('planemat', (0.01,0.01,0.01), (0.05,0.05,0.5), 1)
    plane_mat2 = makeMaterial('planemat2', (0.6,0.1,0.1), (0.5,0.5,0), 1)
    plane_mat3 = makeMaterial('planemat3', (0.0,0.5,0.0), (0.5,0.5,0), 1)
    plane_mat4 = makeMaterial('planemat4', (0.0,0.0,0.5), (0.5,0.5,0), 1)
    #BASE CUBE
    bpy.ops.mesh.primitive_cube_add(location = (0,18,-0.5))
    bpy.data.objects["Cube"].select = True
    selobj = bpy.context.active_object
    selobj.scale = (50,90,1)
    setMaterial(bpy.context.object, plane_mat)
    #COMPRESSION CHAMBER 1
    bpy.ops.mesh.primitive_cube_add(location = (-11.4,-18,0))
    bpy.data.objects["Cube.001"].select = True
    bpy.ops.transform.rotate(value=m.radians(90),axis=(0,1,0))
    bpy.ops.transform.resize(value=(0.5,28,5))
    bpy.ops.transform.translate(value=(0,28,5))
    setMaterial(bpy.context.object, plane_mat3)
    #COMPRESSION CHAMBER 2
    bpy.ops.mesh.primitive_cube_add(location = (11,-18,0))
    bpy.data.objects["Cube.002"].select = True
    bpy.ops.transform.rotate(value=m.radians(90),axis=(0,1,0))
    bpy.ops.transform.resize(value=(0.5,28,5))
    bpy.ops.transform.translate(value=(0,28,5))
    setMaterial(bpy.context.object, plane_mat4)
    #PLANE ON THE TOP
    bpy.ops.mesh.primitive_cube_add(location = (0,11,11.01))
    selobj = bpy.context.active_object
    selobj.scale = (11.5,28.5,0.5)
    blue = makeMaterial('transcube', (0.16,0.05,0.8), (0.5,0.5,0), 0.2,transpar = True)
    #setMaterial(bpy.context.object, blue)
    bpy.data.materials["transcube"].use_transparency = True
    bpy.data.materials["transcube"].transparency_method = 'RAYTRACE'
    bpy.data.materials["transcube"].raytrace_transparency.ior = 1
    bpy.data.materials["transcube"].alpha = 0.0
    setMaterial(bpy.context.object, blue)
    #Piston Frame
    bpy.ops.mesh.primitive_cube_add(location = (0,37.2,5))
    bpy.data.objects["Cube.004"].select = True
    bpy.ops.transform.rotate(value=m.radians(90),axis=(1,0,0))
    bpy.ops.transform.resize(value=(10.3,0.5,5))
    #setMaterial(bpy.context.object, blue)
    #Piston Handle
    bpy.ops.mesh.primitive_cylinder_add(location = (0,47.7,5))
    bpy.data.objects['Cylinder'].select = True
    bpy.ops.transform.rotate(value=m.radians(90),axis=(1,0,0))
    bpy.ops.transform.resize(value=(1,9.8,1))
    #MAke the handle and plate one object i.e. Piston
    bpy.data.objects['Cube.004'].select = True
    bpy.data.objects['Cylinder'].select = True
    bpy.ops.object.join()
    #PLANE ON THE BACK
    bpy.ops.mesh.primitive_cube_add(location = (-18,-18,0))
    bpy.data.objects["Cube.004"].select = True
    bpy.ops.transform.rotate(value=m.radians(90),axis=(1,0,0))
    bpy.ops.transform.resize(value=(-11,4,5))
    bpy.ops.transform.translate(value=(18,-4,5))
    setMaterial(bpy.context.object, plane_mat2)
    bpy.data.objects["Cube.004"].select = False

if __name__ == "__main__":
    del_existing()
    make_chamber()
    box_dim = []
    obj_list = []
    for item in bpy.data.objects:         
        if item.name.startswith('Cube') and item.name != 'Cube.004':
            temp_dict = {}
            temp_dict['x'] = item.location.x
            temp_dict['y'] = item.location.y
            temp_dict['z'] = item.location.z                        
            temp_dict['mass'] = item.game.mass
            temp_dict['name'] = item.name
            box_dim.append(temp_dict)
            obj_list.append(temp_dict)
    com = (COM.COM(box_dim))
    print("COM BEFORE::"+str(com))
    obj_masses = d.divider(d.create_random_list(51))
    pos1 = 0
    pos2 = 0
    y_co1 = com['y'] - 4.3
    y_co2 = com['y'] + 4.3
    for ii in range(0,51):
        if ii % 2 == 0:
            try:
                create_some_object(ii,y_co1,obj_masses['list1'][pos1])
            except IndexError:
                pass
            pos1 += 1
        else:
            create_some_object(ii,y_co2,obj_masses['list2'][pos2])
            pos2 += 1
        if ii % 10 == 0 and ii!=0:
            y_co1 -= 4.3
            y_co2 += 4.3
    #bpy.ops.mesh.primitive_cube_add(location = (com['x'],com['y'],com['z']))
    add_lamp("hemi","HEMI", (0,0,19.9))
    add_camera()
    bpy.context.scene.use_gravity = False
    bpy.context.scene.frame_end = 150
    bpy.context.scene.render.engine ='BLENDER_GAME'
    itemtypes = ['Cube.001','Cube.002','Cube.003','Cube', 'Plane.001','Cube.004']
    for item in bpy.data.objects:
        if item.type == 'MESH' and item.name not in itemtypes:
            item.select = True
            bpy.data.objects[item.name].game.physics_type = 'RIGID_BODY'
            bpy.data.objects[item.name].game.use_actor = True
            bpy.data.objects[item.name].game.use_collision_bounds = True
            if (item.name).find("cone") >= 0:
                bpy.data.objects[item.name].game.collision_bounds_type = 'CONE'
            elif (item.name).find("cube") >= 0:
                bpy.data.objects[item.name].game.collision_bounds_type = 'BOX'
            elif (item.name).find("sphere") >= 0:
                bpy.data.objects[item.name].game.collision_bounds_type = 'SPHERE'
            else:
                bpy.data.objects[item.name].game.collision_bounds_type = 'CONVEX_HULL'
        item.select = False
        if item.name.startswith('obj_'):
            temp_dict = {}
            temp_dict['x'] = item.location.x
            temp_dict['y'] = item.location.y
            temp_dict['z'] = item.location.z                        
            temp_dict['mass'] = item.game.mass
            temp_dict['name'] = item.name
            obj_list.append(temp_dict)  
    bpy.data.objects['Cube.004'].select = True
    bpy.data.objects['Cube.004'].game.mass = 500
    bpy.data.objects['Cube.004'].select = False
    bpy.data.objects['Cylinder'].select = True
    bpy.data.objects['Cylinder'].game.mass = 150
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    com_with_obj = (COM.COM(obj_list))
    positions = get_volume_params()
    print(positions)
    print("VOL_before "+str(vol.volume(positions)))
    #print("COM_before "+str(com_with_obj))
    create_logic_bricks()
    bpy.context.scene.render.engine = 'BLENDER_GAME'
    bpy.ops.wm.blenderplayer_start()