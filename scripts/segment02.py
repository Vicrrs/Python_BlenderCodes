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
import math
import os
import re


def rename_plate(letters: str):
    x = -0.16
    bpy.ops.object.select_all(action='SELECT')
    objs = bpy.data.objects
    placa = objs['PLACA']
    placa.rotation_euler = (0, 0, 0)
    placa.location = (0, 0, 0)
    objs_temp = []

    for idx, letter in enumerate(letters):
        original = objs.get(letter)
        if original is None:
            print(f"Letra '{letter}' não encontrada. Pulando esta letra.")
            continue

        copy = original.copy()
        copy.data = original.data.copy()
        unique_name = f"{letter}_copy_{idx}"  # Nome único para a cópia
        copy.name = unique_name

        current_x, current_y, current_z = copy.dimensions
        # Tratamento especial para 'I' e '1'
        if letter in ('I', '1'):
            copy.dimensions = [0.01619, 0.069, current_z]
        else:
            copy.dimensions = [0.039, 0.069, current_z]

        copy.location = (x, -0.046764, 0.0004)
        bpy.context.collection.objects.link(copy)
        objs_temp.append((letter, copy))

        bpy.ops.object.select_all(action='DESELECT')
        copy.select_set(True)
        placa.select_set(True)
        bpy.context.view_layer.objects.active = placa
        bpy.ops.object.parent_set()

        # Se for o terceiro caractere, adicionar um espaço extra
        x += 0.08 if idx == 2 else 0.04

    placa.rotation_euler[0] = 1.5708
    bpy.ops.object.select_all(action='DESELECT')

    return objs_temp, placa



def get_rotation_in_degrees(obj):
    """Retorna a rotação do objeto em graus."""
    return tuple(math.degrees(angle) for angle in obj.rotation_euler)


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

def save_coco_annotations_to_json(image_id, image_file, objs_temp, file_path):
    # Define o esqueleto do formato COCO
    coco_data = {
        "images": [
            {
                "file_name": image_file,
                "height": 130,
                "width": 400,
                "id": image_id
            }
        ],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "A"}, {"id": 2, "name": "B"}, {"id": 3, "name": "C"},
            {"id": 4, "name": "D"}, {"id": 5, "name": "E"}, {"id": 6, "name": "F"},
            {"id": 7, "name": "G"}, {"id": 8, "name": "H"}, {"id": 9, "name": "I"},
            {"id": 10, "name": "J"}, {"id": 11, "name": "K"}, {"id": 12, "name": "L"},
            {"id": 13, "name": "M"}, {"id": 14, "name": "N"}, {"id": 15, "name": "O"},
            {"id": 16, "name": "P"}, {"id": 17, "name": "Q"}, {"id": 18, "name": "R"},
            {"id": 19, "name": "S"}, {"id": 20, "name": "T"}, {"id": 21, "name": "U"},
            {"id": 22, "name": "V"}, {"id": 23, "name": "W"}, {"id": 24, "name": "X"},
            {"id": 25, "name": "Y"}, {"id": 26, "name": "Z"},
            {"id": 27, "name": "0"}, {"id": 28, "name": "1"}, {"id": 29, "name": "2"},
            {"id": 30, "name": "3"}, {"id": 31, "name": "4"}, {"id": 32, "name": "5"},
            {"id": 33, "name": "6"}, {"id": 34, "name": "7"}, {"id": 35, "name": "8"},
            {"id": 36, "name": "9"}
        ]
    }
    
    # Start annotation ID from 1
    ann_id = 1
    
    # Para cada objeto, cria uma anotação
    for letter, obj in objs_temp:
        # Obtém o bounding box usando funções existentes, por exemplo, get_rotated_bbox
        bbox = get_rotated_bbox(obj, bpy.data.objects['Camera'], bpy.context.scene)
        
        # Cria a entrada de anotação com o category_id
        annotation = {
            "id": ann_id,
            "image_id": image_id,
            "category_id": obj["inst_id"],  # Aqui usamos o ID de instância como o ID de categoria
            "bbox": [bbox[0], bbox[1], bbox[2], bbox[3]],
            "area": bbox[2] * bbox[3],
            "iscrowd": 0
        }
        
        # Adiciona a anotação à lista
        coco_data["annotations"].append(annotation)
        ann_id += 1
    
    # Salva o arquivo JSON
    with open(file_path, 'w') as f:
        json.dump(coco_data, f, indent=4)



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
    # Pegar a bounding box do objeto 3D
    bbox_corners = [object_3d.matrix_world @ Vector(corner) for corner in object_3d.bound_box]

    min_x, max_x, min_y, max_y = float('inf'), -float('inf'), float('inf'), -float('inf')
    for corner in bbox_corners:
        co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, corner)
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

    # Adicionar um pequeno padding para garantir que a bbox englobe toda a letra.
    padding = 2.2  # Ajuste esse valor conforme necessário.
    min_x = max(min_x - padding, 0)
    min_y = max(min_y - padding, 0)
    max_x = min(max_x + padding, render_size[0])
    max_y = min(max_y + padding, render_size[1])
    
    return (min_x, min_y, max_x - min_x, max_y - min_y)


def get_rotated_bbox(obj, camera, scene):
    """
    Obtém a bounding box de um objeto mesmo após rotações e movimentos.
    """
    # Obtém os cantos da bbox no espaço de mundo, levando em conta as transformações.
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Converte os cantos da bbox para coordenadas de tela.
    bbox_screen_coords = [
        bpy_extras.object_utils.world_to_camera_view(scene, camera, corner) 
        for corner in bbox_corners
    ]
    
    # Calcula as extremidades da bbox nas coordenadas de tela.
    min_x = min(coord.x for coord in bbox_screen_coords)
    max_x = max(coord.x for coord in bbox_screen_coords)
    min_y = min(coord.y for coord in bbox_screen_coords)
    max_y = max(coord.y for coord in bbox_screen_coords)

    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    
    # Converte para coordenadas de pixel.
    min_x *= render_size[0]
    max_x *= render_size[0]
    min_y *= render_size[1]
    max_y *= render_size[1]

    # Retorna as coordenadas (min_x, min_y, width, height).
    return (min_x, min_y, max_x - min_x, max_y - min_y)


def assign_colors_save_image(objs_temp, image_path):
    """
    Atribui uma cor sólida e um ID de instância para cada letra e salva a imagem renderizada.
    :param objs_temp: Lista de objetos letras.
    :param image_path: Caminho para salvar a imagem renderizada.
    """
    # Cria um mapeamento de nomes de objetos para IDs de categoria
    category_mapping = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
        'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
        'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
        '0': 27, '1': 28, '2': 29, '3': 30, '4': 31, '5': 32, '6': 33, '7': 34, '8': 35, '9': 36
    }

    # Define uma lista de cores sólidas. A ordem das cores deve corresponder ao mapeamento de categorias
    solid_colors = [
        (1, 0, 0, 1),      # Vermelho para 'A'
        (0, 1, 0, 1),      # Verde para 'B'
        (0, 0, 1, 1),      # Azul para 'C'
        (1, 1, 0, 1),      # Amarelo para 'D'
        (1, 0, 1, 1),      # Magenta para 'E'
        (0, 1, 1, 1),      # Ciano para 'F'
        (0.5, 0, 0, 1),    # Marrom para 'G'
        (0, 0.5, 0, 1),    # Verde escuro para 'H'
        (0, 0, 0.5, 1),    # Azul escuro para 'I'
        (0.5, 0.5, 0, 1),  # Oliva para 'J'
        (0.5, 0, 0.5, 1),  # Roxo para 'K'
        (0, 0.5, 0.5, 1),  # Azul-Verde para 'L'
        (1, 0.5, 0, 1),    # Laranja para 'M'
        (0.5, 1, 0, 1),    # Verde-Claro para 'N'
        (0.5, 0, 1, 1),    # Violeta para 'O'
        (1, 0, 0.5, 1),    # Rosa para 'P'
        (0, 1, 0.5, 1),    # Turquesa para 'Q'
        (0.5, 1, 1, 1),    # Azul-Céu para 'R'
        (1, 0.5, 1, 1),    # Rosa-Claro para 'S'
        (1, 1, 0.5, 1),    # Creme para 'T'
        (0.3, 0.2, 0.1, 1),# Cor de pele para 'U'
        (0.2, 0.3, 0.4, 1),# Azul-Petróleo para 'V'
        (0.6, 0.3, 0, 1),  # Ocre para 'W'
        (0.4, 0.3, 0.6, 1),# Lavanda para 'X'
        (0.1, 0.6, 0.2, 1),# Jade para 'Y'
        (0.2, 0.6, 0.7, 1),# Azul-Aço para 'Z'
        (0.7, 0.7, 0.7, 1),# Prata para '0'
        (0.8, 0.8, 0.4, 1),# Dourado para '1'
        (0.3, 0.7, 0.9, 1),# Céu-Azul para '2'
        (0.6, 0.4, 0.2, 1),# Bronze para '3'
        (0.8, 0.3, 0.7, 1),# Orquídea para '4'
        (0.7, 0.8, 0.3, 1),# Limão para '5'
        (0.2, 0.7, 0.8, 1),# Ciano-Claro para '6'
        (0.9, 0.3, 0.7, 1),# Malva para '7'
        (0.7, 0.3, 0.8, 1),# Ameixa para '8'
        (0.3, 0.8, 0.7, 1),# Água-Marinha para '9'
    ]

    for letter, obj in objs_temp:  # Adiciona 'letter' aqui
        # Usa a letra original para obter o ID da categoria
        category_id = category_mapping[letter]

        # Seleciona uma cor da lista baseada no ID da categoria
        color = solid_colors[category_id - 1]

        # Cria um novo material com essa cor e o atribui ao objeto
        mat = bpy.data.materials.new(name=f"Material_{category_id}")
        mat.diffuse_color = color
        obj.data.materials.clear()
        obj.data.materials.append(mat)

        # Atribui o ID de instância ao objeto
        obj["inst_id"] = category_id

    # Renderiza a cena com as cores atualizadas
    bpy.context.scene.render.filepath = image_path
    bpy.ops.render.render(write_still=True)



if __name__ == "__main__":
    base_image_dir = '/home/vicrrs/CILIA/placas/placa_antiga/images_plates/'
    base_ann_dir = '/home/vicrrs/CILIA/placas/placa_antiga/images_plates/ann/'
    base_img_dir = '/home/vicrrs/CILIA/placas/placa_antiga/images_plates/img/'

    # Inicie o ID da imagem com 1
    image_id = 1

    for _ in range(5): 
        # Configuração da cena, luz e movimentação da placa
        # As funções chamadas aqui devem ser definidas no mesmo script
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.5    
        delete_letters('PLACA')
        set_point_light()
        letras_placa = random_letters(False)
        obj_all, plate = rename_plate(letras_placa)
        move_plate(plate)

        # O caminho para a imagem renderizada
        image_file_name = f"{letras_placa}.png"
        image_path = os.path.join(base_image_dir, image_file_name)

        # Renderiza a imagem e salve no caminho especificado
        render_image(image_path)

        # Atribui cores e IDs de instância para cada objeto
        assign_colors_save_image(obj_all, image_path)

        # Caminho para o arquivo JSON de anotações COCO
        json_file_name = f"{letras_placa}_coco.json"
        json_file_path = os.path.join(base_ann_dir, json_file_name)

        # Salva as anotações COCO no formato JSON
        save_coco_annotations_to_json(image_id, image_file_name, obj_all, json_file_path)

        # Incrementa o ID da imagem para a próxima iteração
        image_id += 1