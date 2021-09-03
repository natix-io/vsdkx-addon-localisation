import cv2
import numpy as np


def visualize(frame: np.ndarray, detections: dict):
    """
    Function which visualizes depth estimation results.

    Args:
        frame (np.ndarray): 3D image
        detections (dict): Dictionary of predictions

    Returns:
         (np.ndarray): 3D resulting image
    """
    input_image = frame.copy()
    for i, box in enumerate(detections['boxes']):
        x1, y1, x2, y2 = box
        input_image = cv2.rectangle(input_image,
                                    (x1, y1),
                                    (x2, y2),
                                    (0, 255, 0),
                                    1)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        font_size = 1 / (i + 1) ** 0.4
        dist_id = detections['extra']['distance_ids'][i]
        text = f'#{i + 1} - dist: {dist_id}'
        input_image = cv2.putText(input_image,
                                  text,
                                  (center_x - 60, center_y),
                                  cv2.FONT_HERSHEY_SIMPLEX,
                                  font_size,
                                  (0, 255, 0),
                                  1)
    cv2.imshow('Sorted by Distance objects', input_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return input_image
