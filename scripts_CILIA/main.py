import bpy
import bmesh
import random
import numpy as np
from pathlib import Path
# PLATE
import bpycv
import cv2


def rename_plate(letters: str):
    x = -0.16
    bpy.ops.object.select_all(action='SELECT')
    objs = bpy.data.objects
    placa = objs['PLACA']
    placa.rotation_euler = (0, 0, 0)
    placa.location = (0, 0, 0)
    objs_temp = []
    for i in letters:
        copy = objs[i].copy()
        current_x, current_y, current_z = copy.dimensions
        if i in ('I', '1'):
            copy.dimensions = [0.01619, 0.069, current_z]
        elif i in ('-'):
            # Centralizar o '-' entre a última letra e o primeiro número
            last_letter_x = x + current_x
            first_number_x = last_letter_x + 0.039
            hyphen_x = (last_letter_x + first_number_x) / 2
            copy.location = (hyphen_x, -0.046764, 0.0004)
            copy.dimensions = [0.01319, 0.017, current_z]
        else:
            copy.dimensions = [0.039, 0.069, current_z]
        copy.location = (x, -0.046764, 0.0004)
        bpy.context.collection.objects.link(copy)
        objs_temp.append(copy)

        bpy.ops.object.select_all(action='DESELECT')
        copy.select_set(True)
        placa.select_set(True)
        bpy.context.view_layer.objects.active = placa
        bpy.ops.object.parent_set()
        x = x + 0.04
    placa.rotation_euler[0] = 1.5708
    bpy.ops.object.select_all(action='DESELECT')
    return objs_temp, placa



def random_letters(is_mercosul=True):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letras_placa = []

    if is_mercosul:
        letras_placa.extend(random.sample(alfabeto, 3))
        letras_placa.append(random.choice(numbers))
        letras_placa.extend(random.sample(alfabeto, 1))
        letras_placa.append('-')
        letras_placa.extend(random.sample(numbers, 2))
    else:
        letras_placa.extend(random.sample(alfabeto, 3))
        letras_placa.append('-')
        letras_placa.extend(random.sample(numbers, 4))

    return ''.join(letras_placa)



def delete_letters(parentName):
    def getChildren(parent_name: str): 
        
        objs=bpy.data.objects[:]
        
        parent_obj = bpy.data.objects[parentName]
        children = [] 
        for ob in objs: 
            if ob.parent == parent_obj: 
                if not ob.name == 'Plane.003':
                 children.append(ob) 
        return children 
    
    bpy.ops.object.select_all(action='SELECT')
    obj_r=getChildren(parent_name=parentName)
    
    if bpy.context.object:
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.select_all(action='DESELECT')
    [bpy.data.objects[i.name].select_set(True) for i in obj_r]
    bpy.ops.object.delete()


def move_plate(obj_plate):
    def calc_rad(number_celsius):
        return number_celsius*3.1415926/180
    
    vector_pos=[2.2,2,1.5,1,0.5,0,-0.5,-1,-1.5,-2.2]
    dic_pos_xz={ '2.2' : [3.17923, 1.72083],
                '2.0':[3.17923, 1.72083],
                '1.5':[2.67575, 1.4769],
                '1.0':[2.3584, 1.3],
                '0.5':[2.0558, 1.03091],
                '0.0':[1.70184, 0.90867],
                '-0.5':[1.36364, 0.7],
                '-1.0':[1.0095, 0.55],
                '-1.5':[0.679947, 0.331604],
                '-2.2':[0.317949, 0.068359]
        
    }
    pos_y = np.random.choice(vector_pos, 1)[0]
    vec_pos_temp=dic_pos_xz[str(pos_y)]
    
    pos_x=random.uniform(-vec_pos_temp[0], vec_pos_temp[0])
    pos_z=random.uniform(-vec_pos_temp[1], vec_pos_temp[1])
    
    mid_x= (vec_pos_temp[0]+vec_pos_temp[0])/2
    mid_z= (vec_pos_temp[0]+vec_pos_temp[0])/2
    
    
    
    if pos_y>=0:
        ang_y= random.uniform(-70, 70)
        
        if -mid_x <= pos_x:
            # não está no meio em x pelo negativo
            ang_x = random.uniform(40, 125)
        
        elif mid_x >= abs(pos_x):
            # não está no meio em x pelo positivo
            ang_x = random.uniform(-2, 61)
        
        else:
            # está no meio 
            ang_x = random.uniform(30, 150)
        
        if -mid_z <= pos_z:
            # não está no meio em z pelo negativo
            ang_z = random.uniform(-45, 45)
        
        elif mid_z >= abs(pos_z):
            # não está no meio em z pelo positivo
            ang_z = random.uniform(-2, 45)
        
        else:
            ang_z = random.uniform(-18, 27)
            
    else:
        ang_y= random.uniform(-80, 80)
        # próximo da câmera
        if mid_x >= abs(pos_x):
            ang_x = random.uniform(30, 100)
        
        else:
            ang_x = random.uniform(60, 100)
        
        if mid_z >= abs(pos_z):
            # não está no meio em z pelo negativo
            ang_z = random.uniform(-40, 40)
        
        else:
            ang_z = random.uniform(10, 63)
    
    ang_x, ang_y, ang_z = calc_rad(int(ang_x)), calc_rad(int(ang_y)), calc_rad(int(ang_z)) 
    
    obj_plate.location = (pos_x, pos_y, pos_z)
    obj_plate.rotation_euler[0] = ang_x
    obj_plate.rotation_euler[1] = ang_y
    obj_plate.rotation_euler[2] = ang_z
    
    
def render_image(path):
    """
    Renderiza a câmera em foco atualmente para o arquivo `path`.
    """
    import bpy
    p = Path(path).resolve()
    if not p.is_absolute():
        raise Exception("caminho para renderizar a imagem não é absoluto. Dica: use o método resolve do pathlib.Path para obter")
    print(f"renderizando para o arquivo {str(p)}...")
    bpy.context.scene.render.filepath = str(p)
    bpy.ops.render.render(write_still=True)
    

def set_point_light(size_square=(2,2), center_y=-3.2):
    # set point of light
    point_light = bpy.data.objects["Point"]
    # add constraint to location of this point
    x = random.uniform(-size_square[0], size_square[0])
    z = random.uniform(-size_square[1], size_square[1])
    loc=(x, center_y, z)
    #set color
    color = (random.random(), random.random(), random.random())
    #set intensity 
    intensity = random.uniform(0, 500)  


    point_light.location = loc
    point_light.data.energy = intensity
    point_light.data.color = color  


def get_points():
    def get_2d_position_from_3d(obj, camera=None, scene=bpy.context.scene, coord_3d=(0,0,0)):
        co = coord_3d @ obj.matrix_world
        # calculate 2d image coordinates
        co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, co)
        render_scale = bpy.context.scene.render.resolution_percentage / 100
        render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
        )

        # this is the result
        return (co_2d.x * render_size[1],
                        co_2d.y * render_size[0])

    plane = bpy.context.object
    data = bpycv.render_data()
    

    camera = bpy.data.objects['Camera']
    image = data['image'].copy()
    pos = []
    
    for v in plane.data.vertices:
        # local to global coordinates
        p = list(get_2d_position_from_3d(plane, camera=camera, coord_3d=v.co))
        p[1] = image.shape[0] - p[1]  # opencv trabalha com quarto quadrante
        pos.append(p)

    pos[1], pos[3] = pos[3], pos[1]  # arrumar a ordem pras cores ficarem certas e não ficar bugado
    pos[1], pos[2] = pos[2], pos[1]

    pos = np.array(pos, dtype=int)  # mais fácil pra castear as listas todas pra int
    colors=iter((  # to usando pra verificar se a ordem dos pontos tá certa
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255),
    ))
    with open('D:/CILIA/blender/images/teste.txt', 'w') as file:
        file.write(f'{pos}')
    for p in pos:
        cv2.circle(image, p, 5, next(colors), -1)
        
    [[x1, y1],[x2, y2],[x3, y3],[x4, y4]] = pos
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite("/home/vicrrs/Documentos/CILIA/blender/images/teste.png", image_bgr)


    
if __name__=="__main__":
    delete_letters('PLACA')
    set_point_light()
    letras_placa = random_letters(False)
    obj_all, plate=rename_plate(letras_placa)
    pos_camera = move_plate(plate) 
    render_image(Path(f'/home/vicrrs/Documentos/CILIA/blender/images/{letras_placa}'))
    get_points()