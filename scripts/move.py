import bpy

# Selecionando o objeto
obj = bpy.context.scene.objects["Object_Name"]

# Movendo para cima
obj.location.z += 1

# Movendo para baixo
obj.location.z -= 1

# Aumentando a escala
obj.scale.z += 1

# Diminuindo a escala
obj.scale.z -= 1

# Rotacionando o objeto
obj.rotation_euler.z += 1
obj.rotation_euler.z += 1

# Movendo no eixo x
obj.location.x += 1

# Movendo no eixo y
obj.location.y += 1
