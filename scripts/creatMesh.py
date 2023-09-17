import bpy
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)

mesh = bpy.data.meshes.new("PlacaDeCarro")
obj = bpy.data.objects.new("PlacaDeCarro", mesh)

scene = bpy.context.scene
scene.collection.objects.link(obj)

bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bm = bmesh.new()

largura = 0.4  # Largura
altura = 0.13  # Altura

verts = [
    (-largura / 2, -altura / 2, 0.0),
    (largura / 2, -altura / 2, 0.0),
    (largura / 2, altura / 2, 0.0),
    (-largura / 2, altura / 2, 0.0),
]

for v_co in verts:
    bm.verts.new(v_co)

bm.verts.ensure_lookup_table()

faces = [(0, 1, 2, 3)]

for f_idx in faces:
    bm.faces.new([bm.verts[i] for i in f_idx])

bm.to_mesh(mesh)
bm.free()

obj.location.x = 0.0
obj.location.y = 0.0
obj.location.z = 0.0 