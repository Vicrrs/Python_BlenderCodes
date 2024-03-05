"""
Remoção de vértices soltos: Elimina vértices que não fazem parte de nenhuma face ou aresta, limpando a malha de elementos desnecessários que podem complicar a edição ou a visualização.
Dissolução de partes degeneradas: Remove partes da malha que são consideradas degeneradas, como arestas ou faces que não contribuem para a forma geral do objeto e podem causar problemas em simulações ou renderizações.
Mesclagem de vértices próximos: Une vértices que estão dentro de uma certa distância um do outro. Isso é útil para simplificar a malha e remover pequenas imperfeições.
Preenchimento de buracos: Fecha os buracos na malha, baseando-se no número de lados especificado. Essa operação é crucial para restaurar a integridade da malha, especialmente em preparação para impressão 3D ou simulações físicas.
"""


import bpy

# Configurações - substitua com seus valores
merge_distance = 0.0015  # Distância para mesclar vértices
sides = 4  # Número de lados para identificar buracos específicos

# objeto selecionado que seja uma malha

# Acesso ao objeto de malha
obj = bpy.context.object
mesh = obj.data

# Modo de edição para operar na malha
bpy.ops.object.mode_set(mode='EDIT')

# Remove vértices soltos
bpy.ops.mesh.select_loose()
bpy.ops.mesh.delete(type='VERT')

# Remove partes degeneradas
bpy.ops.mesh.dissolve_degenerate()

# Mesclar vértices por distância
bpy.ops.mesh.remove_doubles(threshold=merge_distance)

# Preencher buracos
# Esta é uma operação simplificada, ela vai preencher todos os buracos
# Para preencher buracos baseados em 'sides', seria necessário mais lógica
bpy.ops.mesh.fill_holes(sides=sides)

# Volta para o modo objeto
bpy.ops.object.mode_set(mode='OBJECT')

# Salvar o arquivo Blender
bpy.ops.wm.save_as_mainfile(filepath="caminho_para_seu_arquivo.blend")