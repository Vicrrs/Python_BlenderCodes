import bpy
import random
import numpy as np

def create_black_material():
    mat = bpy.data.materials.new(name="BlackMaterial")
    mat.diffuse_color = (0, 0, 0, 1)
    return mat

def delete_letters(parentName):
    def getChildren(parent_name: str):
        objs = bpy.data.objects[:]
        parent_obj = bpy.data.objects.get(parentName)
        children = [ob for ob in objs if ob.parent == parent_obj]
        return children

    bpy.ops.object.select_all(action='DESELECT')
    obj_r = getChildren(parent_name=parentName)

    if bpy.context.object:
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    [bpy.data.objects[i.name].select_set(True) for i in obj_r]
    bpy.ops.object.delete()

def move_plate(obj_plate):
    def calc_rad(number_celsius):
        return number_celsius * 3.1415926 / 180

    vector_pos = [2.4, 2, 1.5, 1, 0.5, 0, -0.5, -1, -1.5, -2]
    dic_pos_xz = {
        '2.4': [3.17923, 1.72083],
        '2.0': [3.17923, 1.72083],
        '1.5': [2.67575, 1.5469],
        '1.0': [2.3584, 1.35975],
        '0.5': [2.0558, 1.22091],
        '0.0': [1.70184, 1.02867],
        '-0.5': [1.36364, 0.812528],
        '-1.0': [1.0095, 0.64],
        '-1.5': [0.679947, 0.431604],
        '-2.0': [0.409576, 0.27515]
    }
    pos_y = np.random.choice(vector_pos, 1)[0]
    vec_pos_temp = dic_pos_xz[str(pos_y)]

    pos_x = random.uniform(-vec_pos_temp[0], vec_pos_temp[0])
    pos_z = random.uniform(-vec_pos_temp[1], vec_pos_temp[1])

    mid_x = (vec_pos_temp[0] + vec_pos_temp[0]) / 2
    mid_z = (vec_pos_temp[0] + vec_pos_temp[0]) / 2

    if pos_y >= 0:
        ang_y = random.uniform(-7, 7)

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
            ang_z = random.uniform(-61, 61)

        elif mid_z >= abs(pos_z):
            # não está no meio em z pelo positivo
            ang_z = random.uniform(-2, 61)

        else:
            ang_z = random.uniform(-65, 65)

    else:
        ang_y = random.uniform(-4, 4)
        # próximo da câmera
        if mid_x >= abs(pos_x):
            ang_x = random.uniform(30, 160)

        else:
            ang_x = random.uniform(60, 129)

        if mid_z >= abs(pos_z):
            # não está no meio em z pelo negativo
            ang_z = random.uniform(-30, 30)

        else:
            ang_z = random.uniform(12, 19)

    ang_x, ang_y, ang_z = calc_rad(int(ang_x)), calc_rad(int(ang_y)), calc_rad(int(ang_z))

    obj_plate.location = (pos_x, pos_y, pos_z)
    obj_plate.rotation_euler[0] = ang_x
    obj_plate.rotation_euler[1] = ang_y
    obj_plate.rotation_euler[2] = ang_z

def arrange_on_plate(s):
    if not s or len(s) != 8 or s[3] != "-":
        print("String no formato incorreto")
        return

    plate = bpy.data.objects.get("Placa")
    if not plate:
        print("Mesh 'Placa' não encontrado.")
        return

    # Deleta as letras existentes da placa
    delete_letters('Placa')

    black_material = create_black_material()

    char_width = 0.044  # Largura das letras na placa
    char_height = 0.065  # Altura das letras na placa
    z_offset = 0.002  # Posicione as letras 0.002m à frente da placa
    x_start = -((len(s) - 1) * char_width) / 2

    # Espaçamento entre as letras (centros)
    spacing = 0.4

    for idx, char in enumerate(s):
        original_char_obj = bpy.data.objects.get(char)
        if original_char_obj:
            char_obj_copy = original_char_obj.copy()
            char_obj_copy.data = original_char_obj.data.copy()
            char_obj_copy.animation_data_clear()

            # Define a placa como pai da letra
            char_obj_copy.parent = plate
            char_obj_copy.matrix_parent_inverse.identity()

            bpy.context.collection.objects.link(char_obj_copy)

            x_pos = x_start + idx * spacing  # Ajusta a posição X
            char_obj_copy.location = (x_pos, 0, z_offset)  # Centralize verticalmente

            # Ajuste o tamanho da cópia para preservar as dimensões originais
            char_obj_copy.scale = (1, 1, 1)  # Isso deve manter as dimensões originais
            
            char_obj_copy.active_material = black_material

            # Adicione uma chamada à função move_plate aqui para mover a placa
            move_plate(plate)



if __name__ == "__main__":
    arrange_on_plate("GVT-1234")
    # Adicione a chamada da função move_plate aqui para mover a câmera
    move_plate(bpy.data.objects['Placa'])
