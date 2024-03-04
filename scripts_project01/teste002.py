import bpy

# Cria a placa
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
placa = bpy.context.active_object
placa.dimensions = [0.4, 0.13, 0]

# Cria o texto
bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
texto = bpy.context.active_object
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.text_insert(text="ABC-1234")
bpy.ops.object.mode_set(mode='OBJECT')

# Ajusta o tamanho e posiciona o texto na placa
texto.scale = [0.044, 0.065, 0.05]
texto.location = [-0.15, -0.05, 0.001]  # O eixo Z é levemente acima da placa para garantir visibilidade