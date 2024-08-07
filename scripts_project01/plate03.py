import bpy
import numpy as np
import random
import math


def create_black_material():
    mat = bpy.data.materials.new(name="BlackMaterial")
    mat.diffuse_color = (0, 0, 0, 1)
    return mat

def arrange_on_plate(s):
    if not s or len(s) != 8 or s[3] != "-":
        print("String no formato incorreto")
        return None    
    plate = bpy.data.objects.get("Placa")
    if not plate:
        print("Mesh 'Placa' não encontrado.")
        return None    
    
    black_material = create_black_material()
    char_width = 0.046
    char_height = 0.065
    y_offset = char_height / 2
    z_offset = 0.0075
    x_start = -((len(s) - 1) * char_width) / 2 - 0.01    
    
    for idx, char in enumerate(s):
        original_char_obj = bpy.data.objects.get(char)
        if original_char_obj:
            char_obj_copy = original_char_obj.copy()
            char_obj_copy.data = original_char_obj.data.copy()
            char_obj_copy.animation_data_clear()
            bpy.context.collection.objects.link(char_obj_copy)
            x_pos = x_start + idx * char_width
            char_obj_copy.location = (x_pos, -0.03, z_offset)
            char_obj_copy.active_material = black_material
            char_obj_copy.parent = plate
            char_obj_copy.matrix_parent_inverse = plate.matrix_world.inverted()

            # Ajuste a rotação da letra para ser paralela à placa
            char_obj_copy.rotation_euler = (math.radians(90), 0, 0)  # Rotação em torno do eixo X

        else:
            print(f"Objeto para o caractere '{char}' não encontrado.")

def delete_letters(parentName):
    def getChildren(parent_name: str):
        objs = bpy.data.objects[:]
        parent_obj = bpy.data.objects.get(parentName)
        if not parent_obj:
            print(f"Parent object '{parentName}' not found.")
            return []
        return [ob for ob in objs if ob.parent == parent_obj and ob.name != 'Plane']    
    bpy.ops.object.select_all(action='DESELECT')
    obj_r = getChildren(parent_name=parentName)    
    for obj in obj_r:
        bpy.data.objects[obj.name].select_set(True)    
    bpy.ops.object.delete()
        

def random_position_for_plate():
    x_limit = 0.2
    y_limit = 0.05
    z_limit = 0.5
    x = random.uniform(-x_limit, x_limit)
    y = random.uniform(-y_limit, y_limit)
    z = random.uniform(0, z_limit)
    return (x, y, z)# Delete previous letters


delete_letters("Placa")# Move the plate to a random position
placa = bpy.data.objects.get("Placa")
if placa:
    placa.location = random_position_for_plate() # Arrange new letters on the plate
arrange_on_plate("ABC-1234")
print("Placa atualizada com sucesso.")