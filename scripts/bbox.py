import bpy
import bmesh
import random
import numpy as np
from pathlib import Path
# PLATE
import bpycv
import cv2
import bpy_extras
from mathutils import Vector
import json


def rename_plate(letters: str):
    x=-0.16
    bpy.ops.object.select_all(action='SELECT')
    objs=bpy.data.objects
    placa=objs['PLACA']
    placa.rotation_euler = (0, 0, 0)
    placa.location = (0, 0, 0)
    objs_temp=[]
    for idx, i in enumerate(letters):
        copy = objs[i].copy()
        current_x, current_y, current_z = copy.dimensions
        # Tratamento especial para 'I' e '1'
        if i in ('I', '1'):
            copy.dimensions = [0.01619, 0.069, current_z]
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
        
        # Se for o terceiro caractere, adicionar um espaço extra.
        if idx == 2:
            x = x + 0.08  # Ajuste o valor '0.08' pro tamanho da lacuna desejado.
        else:
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
#        letras_placa.append('-')
        letras_placa.extend(random.sample(numbers, 2))
    else:
        letras_placa.extend(random.sample(alfabeto, 3))
#        letras_placa.append('-')
        letras_placa.extend(random.sample(numbers, 4))

    return ''.join(letras_placa)


def save_coco_annotations_to_json(filename, annotations):
    data = {
        "annotations": []
    }

    for ann in annotations:
        entry = {
            "name": ann[0],
            "bbox": [ann[1][0], ann[1][1], ann[1][2], ann[1][3]]
        }
        data["annotations"].append(entry)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


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
        return number_celsius * 3.1415926 / 180
    
    ang_x = calc_rad(random.uniform(70, 110))
    
    ang_y = calc_rad(random.uniform(-2, 2))
    ang_z = calc_rad(random.uniform(-30, 30))
    
    # Mantenha as posições atuais para os eixos X e Z
    pos_x = obj_plate.location.x
    pos_y = obj_plate.location.y
    pos_z = obj_plate.location.z
    
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
    # Ajuste a resolução antes de renderizar
    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 130
    
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


def get_points(path_txt, save_image_points = False, path_save_image_points = None)   :

    def get_2d_position_from_3d(obj, camera=None, scene=bpy.context.scene, coord_3d=(0,0,0)):
        co = obj.matrix_world @ coord_3d
        # calculate 2d image coordinates
        co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, co)
        render_scale = bpy.context.scene.render.resolution_percentage / 100
        render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
        )

        # this is the result
        return (
            (co_2d.x * render_size[0]),
            (co_2d.y * render_size[1])
        )
        
    bpy.context.scene.cursor.location = bpy.data.objects["PLACA"].matrix_world @ bpy.data.objects["PLACA"].data.vertices[0].co
    
    data = bpycv.render_data()
    image = data['image'].copy()
    camera = bpy.data.objects['Camera']
    plane = bpy.context.object
    data = bpycv.render_data()
    pos = []
    for v in plane.data.vertices:
        # local to global coordinates
        p = list(get_2d_position_from_3d(plane, camera=camera, coord_3d=v.co))
        p[1] = image.shape[0] - p[1]  # opencv trabalha com quarto quadrante
        pos.append(p)


    
    pos[0], pos[2] = pos[2], pos[0]
    pos[1], pos[3] = pos[3], pos[1]
    pos[2], pos[3] = pos[3], pos[2]

    pos = np.array(pos, dtype=int)  # mais fácil pra castear as listas todas pra int
    colors=iter((  # to usando pra verificar se a ordem dos pontos tá certa
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255),
    ))
    
    pos_str=''
    if save_image_points:
        for p in pos:
            cv2.circle(image, p, 5, next(colors), -1)
            x = round(p[0]/image.shape[1],2)
            y = round(p[1]/image.shape[0],2)
            pos_str = pos_str + ''.join(f'{x},{y};')
            
        
        
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path_save_image_points, image_bgr)
    
    with open(path_txt, 'w') as file:
        file.write(pos_str)
        

def get_bbox(object_3d, camera, scene):
    """
    Calcula a bounding box 2D de um objeto 3D em relação a uma câmera e cena.
    """
    min_x, max_x, min_y, max_y = float('inf'), -float('inf'), float('inf'), -float('inf')
    
    for vertex in object_3d.bound_box:
        co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, object_3d.matrix_world @ Vector(vertex))
        min_x, max_x = min(min_x, co_2d.x), max(max_x, co_2d.x)
        min_y, max_y = min(min_y, co_2d.y), max(max_y, co_2d.y)
        
    render_scale = bpy.context.scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    
    min_x *= render_size[0]
    max_x *= render_size[0]
    min_y = render_size[1] - (min_y * render_size[1])
    max_y = render_size[1] - (max_y * render_size[1])
    
    return (min_x, min_y, max_x - min_x, max_y - min_y)

def save_coco_annotations(filename, annotations):
    with open(filename, 'w') as f:
        for ann in annotations:
            f.write(f"{ann[0]},{ann[1][0]},{ann[1][1]},{ann[1][2]},{ann[1][3]}\n")


    
if __name__=="__main__":
    for i in range(5):
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.5    
        delete_letters('PLACA')
        set_point_light()
        letras_placa=random_letters(False)
        obj_all, plate=rename_plate(letras_placa)
        annotations = []
        camera = bpy.data.objects['Camera']
        scene = bpy.context.scene
        for obj in obj_all:
            bbox = get_bbox(obj, camera, scene)
            annotations.append((obj.name, bbox))
    
        # Salve as anotações COCO em um arquivo.
        save_coco_annotations_to_json(f'/home/vicrrs/Documentos/CILIA/placas/images_plates/ann/{letras_placa}_coco.json', annotations)
        
        pos_camera = move_plate(plate)
        render_image(Path(f'/home/vicrrs/Documentos/CILIA/placas/images_plates/{letras_placa}'))
            
        path_txt = f'/home/vicrrs/Documentos/CILIA/placas/images_plates/ann/{letras_placa}.txt'
        save_image_points = True 
        path_save_image_points = f"/home/vicrrs/Documentos/CILIA/placas/img/{letras_placa}.jpg"
        get_points(path_txt, save_image_points, path_save_image_points)