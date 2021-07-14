import argparse

import cv2
from ai_connector.server import Server

from main import EventDetector


def run_on_video(image_path,
                 detector: EventDetector,
                 system_config: dict):
    """
    Runs the inference on a video on a scheduled interval (e.g. every x seconds)

    Args:
        image_path (str): Path to the video
        detector (object): Instantiated detector object
        system_config (dict): system config file
    """

    # Video capture with the provided input source
    input_image = cv2.VideoCapture(image_path)
    ### Do stuff
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Camera Tampering Detection")
    parser.add_argument('--no-server', default=False, action='store_true',
                        help='set True to run car detection without gRPC')
    parser.add_argument('--image-path', type=str,
                        default='bin/assets/input.jpg',
                        help='path to a image')

    args = parser.parse_args()
    # Run Tampering detection as a gRPC server
    if not args.no_server:
        Server.run(EventDetector)

    system_config = {
        'event_detector_details':
            {'model_type': 'DPT_Hybrid'},
        'debug':
            {
                'debug_mode': True,
                'output_video_path': './bin/inference/test.jpg',
            },
        'model_settings':
            {
                'image_type': 'BGR',
                'device': 'cpu'
            }
    }

    detector = EventDetector(system_config=system_config)
    try:
        video_path = int(args.video_path)
    except ValueError:
        video_path = args.video_path

    run_on_video(video_path, detector, system_config)
