import bpy
import bmesh
import math

def renderizar_objeto(nome_do_objeto, caminho_da_imagem):
    # Função para renderizar o objeto e salvar uma imagem
    bpy.ops.render.render(write_still=True)
    bpy.data.images['Render Result'].save_render(caminho_da_imagem)

def medir_contagem_de_poligonos(nome_do_objeto):
    obj = bpy.data.objects[nome_do_objeto]
    mesh = obj.data
    num_vertices = len(mesh.vertices)
    num_faces = len(mesh.polygons)
    num_edges = len(mesh.edges)
    return num_vertices, num_faces, num_edges

def medir_area_superficie(nome_do_objeto):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    area = sum(f.calc_area() for f in bpy.context.active_object.data.polygons)
    bpy.ops.object.mode_set(mode='OBJECT')
    return area

def medir_volume(nome_do_objeto):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    volume = bpy.context.active_object.dimensions.x * bpy.context.active_object.dimensions.y * bpy.context.active_object.dimensions.z
    bpy.ops.object.mode_set(mode='OBJECT')
    return volume

def verificar_precisao_geométrica(nome_do_objeto):
    # Verifica se a precisão geométrica foi mantida após operações de corte e ajuste
    # Exemplo: comparar dimensões antes e depois de ajustes
    obj = bpy.data.objects[nome_do_objeto]
    dimensoes_antes = obj.dimensions.copy()

    # Realiza operações de ajuste, corte, etc.

    dimensoes_depois = obj.dimensions.copy()

    # Comparação de dimensões para verificar precisão
    precisao_x = abs(dimensoes_antes.x - dimensoes_depois.x)
    precisao_y = abs(dimensoes_antes.y - dimensoes_depois.y)
    precisao_z = abs(dimensoes_antes.z - dimensoes_depois.z)

    # Defina um limite de precisão aceitável
    limite_precisao = 0.001  # Ajuste conforme necessário

    if precisao_x < limite_precisao and precisao_y < limite_precisao and precisao_z < limite_precisao:
        print("A precisão geométrica foi mantida.")
    else:
        print("A precisão geométrica não foi mantida.")

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

def suavizar_superficie(nome_do_objeto, niveis_de_subdivisao, intensidade_suavizacao):
    obj = bpy.data.objects[nome_do_objeto]

    # Aplica o modificador Subdivision Surface
    mod_subdiv = obj.modifiers.new(name="Subdivisao", type="SUBSURF")
    mod_subdiv.levels = niveis_de_subdivisao
    mod_subdiv.render_levels = niveis_de_subdivisao
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Subdivisao")

    # Aplica o modificador Smooth
    mod_smooth = obj.modifiers.new(name="Suavizar", type="SMOOTH")
    mod_smooth.factor = intensidade_suavizacao
    # Número de vezes para suavizar a malha. Ajuste conforme necessário.
    mod_smooth.iterations = 10
    bpy.ops.object.modifier_apply(modifier="Suavizar")

def otimizar_malha(nome_do_objeto, modo_de_otimizacao, valor_de_otimizacao):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj

    # Adiciona o modificador Decimate
    mod_decimate = obj.modifiers.new(name="OtimizarMalha", type="DECIMATE")

    # Configura o modificador de acordo com o modo de otimização desejado
    if modo_de_otimizacao == 'COLLAPSE':
        # Modo COLLAPSE: Reduz a contagem de polígonos pela porcentagem fornecida (0 a 1)
        mod_decimate.ratio = valor_de_otimizacao
    elif modo_de_otimizacao == 'UNSUBDIV':
        # Modo UNSUBDIV: Desfaz a subdivisão em uma quantidade específica de vezes
        mod_decimate.iterations = int(valor_de_otimizacao)
    elif modo_de_otimizacao == 'DISSOLVE':
        # Modo DISSOLVE: Usa o ângulo para dissolver arestas planas
        mod_decimate.angle_limit = valor_de_otimizacao
        mod_decimate.decimate_type = 'DISSOLVE'

    # Aplica o modificador
    bpy.ops.object.modifier_apply(modifier="OtimizarMalha")

def preencher_buracos(nome_do_objeto, tamanho_maximo=0):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.fill_holes(sides=tamanho_maximo)
    bpy.ops.object.mode_set(mode='OBJECT')

def corrigir_normais(nome_do_objeto):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

def ajustar_escala(nome_do_objeto, tamanho_desejado):
    obj = bpy.data.objects[nome_do_objeto]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Calcula a maior dimensão atual do objeto
    dimensoes_atuais = obj.dimensions
    maior_dimensao = max(dimensoes_atuais)

    # Calcula o fator de escala necessário para ajustar a maior dimensão ao tamanho desejado
    fator_de_escala = tamanho_desejado / maior_dimensao

    # Aplica o fator de escala
    obj.scale *= fator_de_escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Ajusta o objeto 'Cube' com rotações e posição específicas
ajustar_objeto('Cube', 45, 30, 0)

# Seleciona vértices dentro de uma circunferência centrada em (0, 0) com raio 1
selecionar_vertices_dentro_da_circunferencia('Cube', 0, 0, 1)

# Corta o objeto 'Cube' com um cubo na posição z=1, escala x=0.5, escala y=0.5, escala z=0.5
cortar_objeto('Cube', 1, 0.5, 0.5, 0.5)

# Suaviza a superfície do objeto 'Cube' com 2 níveis de subdivisão e intensidade de suavização 0.5
suavizar_superficie('Cube', 2, 0.5)

# Otimiza a malha do objeto 'Cube' usando o modo 'COLLAPSE' com uma redução de 0.5 da contagem de polígonos
otimizar_malha('Cube', 'COLLAPSE', 0.5)

# Preenche buracos no objeto 'Cube' com um tamanho máximo de 4 lados por buraco
preencher_buracos('Cube', 4)

# Corrige as normais do objeto 'Cube'
corrigir_normais('Cube')

# Ajusta a escala do objeto 'Cube' para ter uma dimensão máxima de 2
ajustar_escala('Cube', 2)

# Renderiza o objeto 'Cube' e salva uma imagem
renderizar_objeto('Cube', '/caminho/para/salvar/imagem.png')

# Mede a contagem de polígonos do objeto 'Cube'
num_vertices, num_faces, num_edges = medir_contagem_de_poligonos('Cube')
print(f"Vertices: {num_vertices}, Faces: {num_faces}, Edges: {num_edges}")

# Mede a área superficial do objeto 'Cube'
area = medir_area_superficie('Cube')
print(f"Area superficial: {area}")

# Mede o volume do objeto 'Cube'
volume = medir_volume('Cube')
print(f"Volume: {volume}")

# Verifica a precisão geométrica do objeto 'Cube'
verificar_precisao_geométrica('Cube')
