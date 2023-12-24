from roboflow import Roboflow
import cv2
rf = Roboflow(api_key="EXyCYUSm9O95EO0vkjRj")
project = rf.workspace().project("id-card-detection-v1")
model = project.version(1).model

# infer on a local image
print(model.predict("OIP.jpg", confidence=40, overlap=30).json())

#visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")
def detect_and_crop_ID_card(image_path):
    data = model.predict(image_path, confidence=40, overlap=30).json()

    x = int(data['predictions'][0]['x'])
    y = int(data['predictions'][0]['y'])
    width = data['predictions'][0]['width']
    height = data['predictions'][0]['height']

    # Đọc ảnh từ đường dẫn
    image_path2 = data['predictions'][0]['image_path']
    image = cv2.imread(image_path2)

    # Xác định tâm của ảnh
    left_x = int(x - width / 2)
    top_y = int(y - height / 2)

    # Lấy phần ảnh của căn cước công dân
    id_card_image = image[top_y:top_y+height, left_x:left_x+width]

    # Hiển thị ảnh xoay
    cv2.imwrite(f'Rotated_{image_path}.jpg', id_card_image)
