import cv2
import numpy as np

def add_license_plate_segmentation_mask(image, points):
  """
  Adiciona uma máscara de segmentação denotando os quatro pontos de uma placa de carro, para uma imagem.

  Args:
    image: Imagem a ser processada.
    points: Lista de quatro pontos que definem a placa de carro.

  Returns:
    Imagem com a máscara de segmentação adicionada.
  """

  # Verifica se os tamanhos dos argumentos de entrada são iguais.
  if image.shape[:2] != points.shape:
    # Redimensiona os pontos para que tenham o mesmo tamanho da imagem.
    points = cv2.resize(points, image.shape[:2])

  # Verifica se os argumentos de entrada têm o mesmo número de canais.
  if image.shape[2] != 1:
    # Converte a imagem para um canal.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Cria uma máscara vazia.
  mask = np.zeros(image.shape[:2], dtype=np.uint8)

  # Desenha um retângulo na máscara, usando os pontos fornecidos.
  cv2.fillPoly(mask, np.array([points], dtype=np.int32), 255)

  # Adiciona a máscara à imagem.
  return cv2.addWeighted(image, 1.0, mask, 0.5, 0.0)


# Exemplo de uso

image = cv2.imread("PLACA.jpg")
points = [(100, 100), (200, 100), (200, 200), (100, 200)]

mask = add_license_plate_segmentation_mask(image, points)

cv2.imshow("Imagem com máscara de segmentação", mask)
cv2.waitKey(0)