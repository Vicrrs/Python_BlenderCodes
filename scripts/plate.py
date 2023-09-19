# Copiando text para uma placa pre moldada:

import bpy

def create_black_material():
    mat = bpy.data.materials.new(name="BlackMaterial")
    mat.diffuse_color = (0, 0, 0, 1)
    return mat

def arrange_on_plate(s):
    if not s or len(s) != 8 or s[3] != "-":
        print("String no formato incorreto")
        return

    plate = bpy.data.objects.get("Placa")
    if not plate:
        print("Mesh 'Placa' não encontrado.")
        return

    black_material = create_black_material()
    
    char_width = 0.046
    char_height = 0.035
    y_offset = char_height / 2
    z_offset = 0.0075  # ajuste conforme a sua necessidade
    x_start = -((len(s) - 1) * char_width) / 2 - 0.03  # Ajuste o valor -0.1 para mover mais para a esquerda

    for idx, char in enumerate(s):
        original_char_obj = bpy.data.objects.get(char)
        if original_char_obj:
            char_obj_copy = original_char_obj.copy()
            char_obj_copy.data = original_char_obj.data.copy()
            char_obj_copy.animation_data_clear()
            bpy.context.collection.objects.link(char_obj_copy)
            
            x_pos = x_start + idx * char_width
            char_obj_copy.location = (x_pos, -0.04, z_offset) # movendo em relacao ao eixo y
            
            char_obj_copy.active_material = black_material

            char_obj_copy.parent = plate
            char_obj_copy.matrix_parent_inverse = plate.matrix_world.inverted()
            
        else:
            print(f"Objeto para o caractere '{char}' não encontrado.")

arrange_on_plate("ABC-1234")