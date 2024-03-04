import json
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def load_annotations(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    annotations_for_image = []
    for annotation in data['annotations']:
        obj_name = annotation['name']
        bbox = annotation['bbox']
        annotations_for_image.append((obj_name, bbox))
            
    return annotations_for_image

def visualize_bbox(image_path, annotations):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for ann in annotations:
        obj_name, bbox = ann
        x, y, w, h = map(int, bbox)
        h = abs(h)  # Use the absolute value for height
        y = y - h   # Adjust the y origin
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='g', facecolor='none')
        ax.add_patch(rect)
        plt.text(x, y, obj_name, bbox=dict(facecolor='green', alpha=0.5), color='white')

    plt.show()



# Example of usage:
json_file_path = r"E:\CILIA\placas\Placa_antigas\images_plates\ann\LUF8794_coco.json"
annotations = load_annotations(json_file_path)
image_path = r"E:\CILIA\placas\Placa_antigas\images_plates\LUF8794.png"  # Change this to the path of your actual image
visualize_bbox(image_path, annotations)
