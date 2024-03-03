import bpy

# Cria a placa
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
placa = bpy.context.active_object
placa.dimensions = [0.4, 0.13, 0]

# Defina a cor da placa (por exemplo, branco)
mat_placa = bpy.data.materials.new(name="Material Placa")
mat_placa.diffuse_color = (1, 1, 1, 1)  # RGBA para branco
placa.data.materials.append(mat_placa)

# Cria o texto
bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
texto = bpy.context.active_object
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.text_insert(text="ABC-1234")
bpy.ops.object.mode_set(mode='OBJECT')

# Ajusta o tamanho e posiciona o texto na placa
texto.scale = [0.05, 0.05, 0.05]
texto.location = [-0.15, -0.05, 0.001]

# Defina a cor do texto (por exemplo, preto)
mat_texto = bpy.data.materials.new(name="Material Texto")
mat_texto.diffuse_color = (0, 0, 0, 1)  # RGBA para preto
texto.data.materials.append(mat_texto)

# Alterar a fonte do texto (você precisa ter um arquivo .ttf disponível)
caminho_para_fonte = "/media/vicrrs/Novo volume/CILIA/mandatory-font/Mandatory-O2Vp.ttf"
texto.data.font = bpy.data.fonts.load(caminho_para_fonte)