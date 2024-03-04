import json
from PIL import Image, ImageDraw

# Carregar o arquivo JSON
with open('/home/vicrrs/CILIA/placas/placa_antiga/images_plates/SQM4873_coco.json', 'r') as file:
    data = json.load(file)

# Suponha que você tenha a imagem original em 'original_image.png'
original_image_path = '/home/vicrrs/CILIA/placas/placa_antiga/images_plates/SQM4873.png'
original_image = Image.open(original_image_path)
width, height = original_image.size

# Crie uma imagem para o mapa de segmentação de instâncias
instance_segmentation_map = Image.new('RGB', (width, height))

# Processar cada anotação e desenhar as bounding boxes nas máscaras
for ann in data['annotations']:
    # Crie uma máscara para a instância atual
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Desenhe a bounding box na máscara
    bbox = ann['bbox']
    inst_id = ann['inst_id']
    draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])], fill=255)
    
    # Salve a máscara da instância individual (opcional)
    mask.save(f'/home/vicrrs/CILIA/placas/placa_antiga/images_plates/mask_{inst_id}.png')
    
    # Desenhe a instância no mapa de segmentação com um valor de pixel único
    draw = ImageDraw.Draw(instance_segmentation_map)
    unique_color = (inst_id, inst_id, inst_id)  # A cor é uma representação do inst_id
    draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])], fill=unique_color)

# Salve o mapa de segmentação de instâncias
instance_segmentation_map.save('/home/vicrrs/CILIA/placas/placa_antiga/images_plates/instance_segmentation_map.png')
