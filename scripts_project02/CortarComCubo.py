"""
Selecionar Objeto: Seleciona um objeto específico para realizar a operação de corte.
Criar Cortador: Cria um cubo que será utilizado como ferramenta de corte.
Ajustar Posição e Escala do Cortador: Posiciona o cortador adequadamente em relação ao objeto que será cortado e ajusta sua escala para garantir que abrange a área desejada.
Aplicar Operação Booleana: Utiliza o cortador para aplicar uma operação booleana de diferença, efetivamente cortando o objeto selecionado.
Atualizar Cena: Atualiza a cena para refletir as mudanças feitas pela operação booleana.
Aplicar Modificador: Aplica o modificador booleano ao objeto, concretizando o corte.
Excluir Cortador: Remove o objeto cortador da cena, pois não é mais necessário após a aplicação do corte.
"""


import bpy

# Substitua 'nome_do_objeto' pelo nome do seu objeto que você deseja cortar
nome_do_objeto = "mesh"
objeto_a_cortar = bpy.data.objects[nome_do_objeto]

# Certifique-se de que estamos em modo de objeto
bpy.ops.object.mode_set(mode='OBJECT')

# Cria um cubo para usar como cortador
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
cortador = bpy.context.object
cortador.name = 'Cortador'

# Ajuste a posição do cortador para estar abaixo do objeto a cortar
# A posição no eixo Z deve ser negativa para estar abaixo do objeto
# A escala em Z deve ser grande o suficiente para abranger toda a parte inferior do objeto
cortador.location.z = -1  # Ajuste isso conforme necessário
cortador.scale.x = 10
cortador.scale.y = 10
cortador.scale.z = 1.1 # Ajuste para que a altura seja suficiente para cobrir a parte inferior

# Agora aplica a operação booleana
mod_bool = objeto_a_cortar.modifiers.new(type="BOOLEAN", name="Corte")
mod_bool.object = cortador
mod_bool.operation = 'DIFFERENCE'

# Atualiza a cena para garantir que a adição do cortador seja reconhecida
bpy.context.view_layer.update()

# Aplica o modificador booleano
bpy.context.view_layer.objects.active = objeto_a_cortar
bpy.ops.object.modifier_apply(modifier=mod_bool.name)

# Exclui o cortador, já que não é mais necessário
bpy.data.objects.remove(cortador)