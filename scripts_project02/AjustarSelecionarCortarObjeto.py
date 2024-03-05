"""
1. Ajuste de Rotação e Posição: Rotaciona o objeto em três eixos (X, Y, Z) e ajusta sua posição para que a parte mais baixa toque o plano do chão (z=0).
2. Seleção e Deleção de Vértices Dentro de uma Circunferência: Seleciona vértices dentro de uma circunferência especificada e, em seguida, inverte a seleção para deletar aqueles fora da circunferência.
3. Corte Booleano com um Cubo: Cria um cubo que serve como cortador para modificar o objeto principal através de uma operação booleana de diferença, seguido pela remoção do cortador.
"""

import bpy
import bmesh
import math

def ajustar_objeto(nome_do_objeto, angulo_x, angulo_y, angulo_z):
    obj = bpy.data.objects[nome_do_objeto]

    # Ajusta rotação do objeto
    obj.rotation_euler.x = math.radians(angulo_x)
    obj.rotation_euler.y = math.radians(angulo_y)
    obj.rotation_euler.z = math.radians(angulo_z)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    # Ajusta a posição do objeto para que a parte mais baixa toque o plano do chão (z=0)
    lowest_point = min(vertex.co.z for vertex in obj.data.vertices)
    obj.location.z -= lowest_point

    bpy.context.view_layer.update()

def selecionar_vertices_dentro_da_circunferencia(nome_do_objeto, cx, cy, raio):
    obj = bpy.data.objects[nome_do_objeto]

    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data
    for vertex in mesh.vertices:
        global_vertex_location = obj.matrix_world @ vertex.co
        dist = math.sqrt((global_vertex_location.x - cx) ** 2 + (global_vertex_location.y - cy) ** 2)
        if dist <= raio:
            vertex.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')

def cortar_objeto(nome_do_objeto, posicao_z_cortador, escala_x_cortador, escala_y_cortador, escala_z_cortador):
    objeto_a_cortar = bpy.data.objects[nome_do_objeto]

    # Cria e posiciona o cortador
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
    cortador = bpy.context.object
    cortador.location.z = posicao_z_cortador
    cortador.scale.x = escala_x_cortador
    cortador.scale.y = escala_y_cortador
    cortador.scale.z = escala_z_cortador

    # Aplica corte booleano
    mod_bool = objeto_a_cortar.modifiers.new(type="BOOLEAN", name="Corte")
    mod_bool.object = cortador
    mod_bool.operation = 'DIFFERENCE'
    bpy.context.view_layer.update()

    # Aplica o modificador booleano e remove o cortador
    bpy.context.view_layer.objects.active = objeto_a_cortar
    bpy.ops.object.modifier_apply(modifier="Corte")
    bpy.data.objects.remove(cortador)

if __name__ == '__main__':
    nome_do_objeto = "mesh"
    cx, cy = 0.0, 0.0
    raio = 0.4
    angulo_x, angulo_y, angulo_z = 180, 180, 0
    posicao_z_cortador = -1
    escala_x_cortador, escala_y_cortador, escala_z_cortador = 10, 10, 1.1

    ajustar_objeto(nome_do_objeto, angulo_x, angulo_y)
    selecionar_vertices_dentro_da_circunferencia(nome_do_objeto, cx, cy, raio)
    cortar_objeto(nome_do_objeto, posicao_z_cortador, escala_x_cortador, escala_y_cortador, escala_z_cortador)