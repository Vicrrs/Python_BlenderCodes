import bpy
import bmesh
import random
import numpy as np
from pathlib import Path
# PLATE

def rename_plate(letters: str):
    x=-0.16
    
    bpy.ops.object.select_all(action='SELECT')
    objs=bpy.data.objects
    placa=objs['PLACA']
    placa.rotation_euler = (0, 0, 0) 
    placa.location = (0, 0, 0) 
    objs_temp=[]

    for i in letters:
        copy = objs[i].copy()
        current_x, current_y, current_z = copy.dimensions
        
        # Tratamento especial para 'I' e '1'
        if i in ('I', '1'):
            copy.dimensions = [0.01619, 0.069, current_z]
        elif i in ('-'):
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
        x = x + 0.046

    placa.rotation_euler[0] = 1.5708
    bpy.ops.object.select_all(action='DESELECT')
    
    return objs_temp, placa

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
    
    vector_pos=[2.4,2,1.5,1,0.5,0,-0.5,-1,-1.5,-2]
    dic_pos_xz={ '2.4' : [3.17923, 1.72083],
                '2.0':[3.17923, 1.72083],
                '1.5':[2.67575, 1.5469],
                '1.0':[2.3584, 1.35975],
                '0.5':[2.0558, 1.22091],
                '0.0':[1.70184, 1.02867],
                '-0.5':[1.36364, 0.812528],
                '-1.0':[1.0095, 0.64],
                '-1.5':[0.679947, 0.431604],
                '-2.0':[0.409576, 0.27515]
        
    }
    pos_y = np.random.choice(vector_pos, 1)[0]
    vec_pos_temp=dic_pos_xz[str(pos_y)]
    
    pos_x=random.uniform(-vec_pos_temp[0], vec_pos_temp[0])
    pos_z=random.uniform(-vec_pos_temp[1], vec_pos_temp[1])
    
    mid_x= (vec_pos_temp[0]+vec_pos_temp[0])/2
    mid_z= (vec_pos_temp[0]+vec_pos_temp[0])/2
    
    
    
    if pos_y>=0:
        ang_y= random.uniform(-7, 7)
        
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
        ang_y= random.uniform(-4, 4)
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
    
if __name__=="__main__":
    delete_letters('PLACA')
        
    letras_placa= 'ABC-1234'
    obj_all, plate=rename_plate(letras_placa)
    move_plate(plate)
    render_image(Path(f'/CILIA/blender/images/{letras_placa}'))
    