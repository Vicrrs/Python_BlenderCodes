"""
Rotacao: O código rotaciona o objeto em 180 graus ao longo dos eixos X e Y.
AjusteZ: Ajusta a posição do objeto no eixo Z para que o ponto mais baixo fique alinhado com a origem do eixo Z.
DelecaoForaCircunferencia: Seleciona vértices dentro de uma circunferência definida e inverte a seleção para deletar os vértices fora dessa área.
"""

import bpy
import bmesh
import math

# Atribui à variável 'obj' o objeto ativo atual no contexto do Blender.
obj = bpy.context.active_object  

# Muda o modo para 'OBJECT' para garantir que as operações a seguir usem as coordenadas globais do objeto.
bpy.ops.object.mode_set(mode='OBJECT')  

# Rotaciona o objeto em 180 graus no eixo X (converte graus em radianos).
obj.rotation_euler.x = math.radians(180)
# Rotaciona o objeto em 180 graus no eixo Y (converte graus em radianos).  
obj.rotation_euler.y = math.radians(180)  

#  Aplica a transformação de rotação ao objeto, sem alterar sua localização ou escala.
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)  

# Encontra o ponto mais baixo do objeto ao longo do eixo Z.
lowest_point = min(vertex.co.z for vertex in obj.data.vertices)  

# Ajusta a localização do objeto no eixo Z de forma que o ponto mais baixo fique alinhado com a origem do eixo Z.
obj.location.z -= lowest_point  
# Atualiza a view layer para aplicar as transformações feitas no objeto.
bpy.context.view_layer.update()  

cx, cy = 0.0, 0.0  # Define as coordenadas (x, y) do centro da circunferência.
raio = 0.38  # Define o raio da circunferência.

bpy.ops.object.mode_set(mode='EDIT')  # Entra no modo de edição para selecionar os vértices da malha.
bpy.ops.mesh.select_mode(type="VERT")  # Define o modo de seleção para trabalhar com vértices.
bpy.ops.mesh.select_all(action='DESELECT')  # Deseleciona todos os vértices para começar a seleção do zero.
bpy.ops.object.mode_set(mode='OBJECT')  # Retorna ao modo de objeto para trabalhar com os dados do objeto diretamente.

mesh = obj.data  # Atribui à variável 'mesh' os dados da malha do objeto ativo.

for vertex in mesh.vertices:  # Itera sobre cada vértice na malha.
    global_vertex_location = obj.matrix_world @ vertex.co  # Converte a localização do vértice para coordenadas globais.
    # Calcula a distância do vértice até o centro da circunferência.
    dist = math.sqrt((global_vertex_location.x - cx) ** 2 + (global_vertex_location.y - cy) ** 2)
    if dist <= raio:  # Se a distância é menor ou igual ao raio, o vértice está dentro da circunferência.
        vertex.select = True  # Seleciona o vértice.

# Entra no modo de edição para visualizar os vértices selecionados.
bpy.ops.object.mode_set(mode='EDIT')  

# Inverte a seleção atual de vértices (os que estavam fora da circunferência agora estão selecionados).
bpy.ops.mesh.select_all(action='INVERT')  

# Deleta os vértices que estão selecionados após a inversão.
bpy.ops.mesh.delete(type='VERT')  