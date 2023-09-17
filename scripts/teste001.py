import bpy

largura = 0.4 
altura = 0.13  


bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
plane_obj = bpy.context.object
plane_obj.scale.x = largura
plane_obj.scale.y = altura
plane_obj.location.z = 0

bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0.1))
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.text_insert(text="ABC-1234")
bpy.ops.object.mode_set(mode='OBJECT')

text_obj = bpy.context.object
text_obj.scale = (0.1, 0.1, 0.1)
text_obj.location = (0, 0, 0.1)
