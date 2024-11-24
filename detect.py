import torch

def detect_objects(image_path):
    """
    Uses YOLOv5 for object detection on the given image.
    :param image_path: Path to the image file
    :return: List of detected objects
    """
    # Load YOLOv5 model (pre-trained on COCO dataset)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    # Perform inference on the image
    results = model(image_path)

    # Extract detected objects
    detected_objects = results.pandas().xyxy[0]['name'].tolist()

    return detected_objects
