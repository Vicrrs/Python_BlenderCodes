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
    
    
def render_image(path, grayscale=False):
    """
    Renderiza a câmera em foco atualmente para o arquivo `path`.
    Se 'grayscale' for True, a imagem será convertida para escala de cinza.
    """
    import bpy
    p = Path(path).resolve()
    if not p.is_absolute():
        raise Exception("caminho para renderizar a imagem não é absoluto.")
    print(f"renderizando para o arquivo {str(p)}...")
    bpy.context.scene.render.filepath = str(p)
    # Ajuste a resolução antes de renderizar
    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 130
    
    bpy.ops.render.render(write_still=True)

    if grayscale:
        # Converte a imagem renderizada para escala de cinza e salva
        img = bpy.data.images.load(str(p))
        img.colorspace_settings.name = 'Non-Color'
        img.save_render(str(p))
        img.user_clear()
        bpy.data.images.remove(img)
    

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


def generate_gray_scale_mapping():
    """
    Gera um mapeamento pré-definido de valores em escala de cinza para caracteres alfanuméricos.
    """
    gray_scale_values = {
    'A': 0.9, 'B': 0.28234324324, 'C': 0.14, 'D': 0.13, 'E': 0.15, 'F': 0.16, 'G': 0.17, 'H': 0.18,
    'I': 0.9, 'J': 0.20, 'K': 0.21, 'L': 0.22, 'M': 0.23, 'N': 0.24, 'O': 0.25, 'P': 0.26,
    'Q': 0.9, 'R': 0.28, 'S': 0.29, 'T': 0.30, 'U': 0.31, 'V': 0.32, 'W': 0.33, 'X': 0.34,
    'Y': 0.35, 'Z': 0.36,
    '0': 0.9, '1': 0.9, '2': 0.9, '3': 0.9, '4': 0.9, '5': 0.9, '6': 0.9, '7': 0.9,
    '8': 0.9, '9': 0.9
    }

    return gray_scale_values


def set_letter_gray_scale_material(obj, gray_scale_value):
    """
    Define o material de uma letra para uma escala de cinza específica.
    """
    mat = bpy.data.materials.new(name="LetterGrayScaleMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (gray_scale_value, gray_scale_value, gray_scale_value, 1)

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def apply_predefined_gray_scale_to_letters(objs, gray_scale_mapping, apply_gray_scale=True):
    """
    Aplica uma escala de cinza predefinida a cada letra/objeto com base no mapeamento fornecido.
    Se `apply_gray_scale` for False, não altera os materiais.
    """
    if not apply_gray_scale:
        return

    for obj in bpy.context.scene.objects:
        if obj.name in gray_scale_mapping:  # Certifique-se de que o nome do objeto corresponde a uma chave em gray_scale_mapping
            gray_scale_value = gray_scale_mapping[obj.name]
            set_letter_gray_scale_material(obj, gray_scale_value)
            print(f"Aplicado cinza {gray_scale_value} ao objeto {obj.name}")


def set_plate_material(obj_plate):
    """
    Define o material do objeto 'PLACA' para 'auto.inst_material.0'.
    """
    mat = bpy.data.materials.get("auto.inst_material.0")
    if not mat:
        raise ValueError("Material 'auto.inst_material.0' não encontrado.")

    if obj_plate.data.materials:
        obj_plate.data.materials[0] = mat
    else:
        obj_plate.data.materials.append(mat)
        

def set_plate_original_material(obj_plate):
    """
    Define o material do objeto 'PLACA' para 'Material.003'.
    """
    mat = bpy.data.materials.get("Material.003")
    if not mat:
        raise ValueError("Material 'Material.003' não encontrado.")

    if len(obj_plate.data.materials) == 0:
        obj_plate.data.materials.append(mat)
    else:
        obj_plate.data.materials[0] = mat


def save_gray_scale_mapping(mapping, filename):
    """
    Salva o mapeamento da escala de cinza em um arquivo de texto.
    """
    with open(filename, 'w') as file:
        for alphanum, gray_value in mapping.items():
            file.write(f"{alphanum}: {gray_value}\n")




def restore_original_materials(objs, original_materials):
    # Restaurando os materiais originais dos objetos
    for obj in objs:
        if obj.name in original_materials:  # Verifica se o objeto está no dicionário de materiais originais
            for i, mat in enumerate(obj.data.materials):
                obj.data.materials[i] = original_materials[obj.name][i]


def save_original_materials(objs):
    # Salvando os materiais originais dos objetos
    original_materials = {obj: [mat for mat in obj.data.materials] for obj in objs}
    return original_materials



def render_plate_with_original_colors(objs, plate, letras_placa, original_materials):
    # Restaura os materiais originais antes de renderizar a imagem original
    restore_original_materials(objs, original_materials)
    
    # Renderizando a placa com as cores originais
    render_image(Path(f'/media/tkroza/Dados/CILIA/placas/Placa_antiga/images_plates/ORIGINAL_{letras_placa}'))

def render_plate_with_gray_scale(objs, plate, letras_placa, gray_scale_mapping):
    # Aplicando material 'auto.inst_material.0' à placa
    set_plate_material(plate)  # Corrigido o nome da função aqui
    
    # Aplicando escala de cinza predefinida às letras e renderizando a placa
    apply_predefined_gray_scale_to_letters(objs, gray_scale_mapping, apply_gray_scale=True)
    render_image(Path(f'/media/tkroza/Dados/CILIA/placas/Placa_antiga/images_plates/GRAY_{letras_placa}'))
    
if __name__ == "__main__":
    gray_scale_mapping = generate_gray_scale_mapping()  # Gera o mapeamento fixo
    
    for i in range(2):
        # Certifique-se de que isso remove todas as letras e números corretamente
        delete_letters('PLACA')
        # Configura a luz pontual
        set_point_light()
        # Gera letras aleatórias para a placa
        letras_placa = random_letters(False)
        # Renomeia a placa com as letras geradas
        obj_all, plate = rename_plate(letras_placa)
        # Prepara as anotações para armazenar informações da placa
        annotations = []
        # Seleciona a câmera e a cena para cálculos de renderização
        camera = bpy.data.objects['Camera']
        scene = bpy.context.scene
        # Calcula a bounding box rotacionada e a rotação dos objetos de letras
        for obj in obj_all:
            bbox = get_rotated_bbox(obj, camera, scene)
            rotation = get_rotation_in_degrees(obj)
            annotations.append((obj.name, bbox, rotation))
        
        # Salva os materiais originais antes de qualquer renderização
        original_materials = save_original_materials(obj_all)
        
        # Renderiza a placa com as cores originais
        render_plate_with_original_colors(obj_all, plate, letras_placa, original_materials)
        
        # Restaura os materiais originais após renderizar a imagem original
        restore_original_materials(obj_all, original_materials)
        
        # Renderiza a placa com as letras em escala de cinza usando o mapeamento fixo
        render_plate_with_gray_scale(obj_all, plate, letras_placa, gray_scale_mapping)
        
        # Restaura os materiais originais após renderizar em escala de cinza
        restore_original_materials(obj_all, original_materials)
        
        # Deleta os objetos de letras e números para a próxima iteração
        delete_letters('PLACA')

