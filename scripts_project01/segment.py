import cv2
import numpy as np
import json

def segment_letters(image_path, output_path):
    # Carrega a imagem.
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"A imagem não pôde ser carregada do caminho: {image_path}")

    # Cores definidas em BGR e intervalo 0-255.
    unique_colors = [
        (1, 0, 0, 1),  # Vermelho
        (0, 1, 0, 1),  # Verde
        (0, 0, 1, 1),  # Azul
        (1, 1, 0, 1),  # Amarelo
        (1, 0, 1, 1),  # Magenta
        (0, 1, 1, 1),  # Ciano
        (1, 0.5, 0, 1), # Laranja
        (0.5, 0, 0.5, 1), # Roxo
        (0, 0.5, 0, 1), # Verde Escuro
        (0.5, 0.5, 0.5, 1), # Cinza
        (0.5, 0, 0, 1), # Marrom
        (1, 0.5, 0.5, 1), # Rosa
        (0.5, 1, 0.5, 1), # Verde Claro
        (0.5, 0.5, 1, 1), # Azul Claro
        (1, 1, 0.5, 1), # Amarelo Claro
    ]

    # Segmentação por cor.
    segmentation_data = []

    for color in unique_colors:
        # Cria uma máscara para a cor atual.
        lower = np.array(color, dtype=np.uint8)
        upper = np.array(color, dtype=np.uint8)
        mask = cv2.inRange(image, lower, upper)
        
        # Verifica se há alguma máscara válida.
        if np.any(mask):
            print(f"Cor detectada: {color}")
            # Encontra contornos.
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Salva dados de segmentação.
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                segmentation_data.append({
                    'color': color,
                    'bbox': [x, y, x+w, y+h]
                })

                # Desenha o contorno na imagem (opcional).
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            print(f"Cor {color} não detectada.")

    # Salva a imagem com as segmentações desenhadas (opcional).
    cv2.imwrite(output_path, image)
    
    # Salva os dados de segmentação em um arquivo JSON.
    if segmentation_data:
        with open(f"{output_path}.json", 'w') as f:
            json.dump(segmentation_data, f, indent=4)
    else:
        print("Nenhum dado de segmentação para salvar.")

# Substitua com os caminhos corretos para a sua imagem e localização de saída.
segment_letters('/home/vicrrs/CILIA/placas/placa_antiga/images_plates/FKW1069.png', '/home/vicrrs/CILIA/placas/placa_antiga/images_plates/FKW1069_segmented_image.png')
