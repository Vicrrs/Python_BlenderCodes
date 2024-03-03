import cv2
import numpy as np

# Carregue a imagem
imagem = cv2.imread('IMG_20230413_142656651_HDR2-1160x679.jpg')

# Defina os quatro pontos da placa manualmente (x, y)
pontos_placa = [(100, 100), (200, 100), (200, 200), (100, 200)]

# Crie uma máscara vazia
mascara = np.zeros(imagem.shape[:2], dtype=np.uint8)

# Converta os pontos da placa em um formato compatível com o polígono OpenCV
pontos_placa = np.array(pontos_placa, dtype=np.int32)

# Preencha a máscara com os pontos da placa
cv2.fillPoly(mascara, [pontos_placa], 255)

# Aplique a máscara à imagem original
imagem_segmentada = cv2.bitwise_and(imagem, imagem, mask=mascara)

# Desenhe os pontos da placa na imagem segmentada
for ponto in pontos_placa:
    cv2.circle(imagem_segmentada, ponto, 5, (0, 0, 255), -1)

# Mostre a imagem segmentada com os pontos da placa
cv2.imshow('Imagem Segmentada', imagem_segmentada)
cv2.waitKey(0)
cv2.destroyAllWindows()
