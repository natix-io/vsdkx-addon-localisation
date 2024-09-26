import numpy as np
import unittest

from vsdkx.core.structs import AddonObject, Inference
from vsdkx.addon.depth.processor import DepthEstimator


class MyTestCase(unittest.TestCase):
    addon_config = {
        'stages': 3,
        'grid_size': 5,
        'model_type': 'DPT_Hybrid'
    }

    model_settings = {
        'device': 'cpu'
    }

    def test_center(self):
        frame = (np.random.rand(640, 640, 3) * 100).astype('uint8')
        bb_1 = [10, 20, 100, 200]
        center_1 = [[110, 55]]

        center_points = DepthEstimator._get_center_points([bb_1])

        self.assertEqual(center_points, center_1)

        square_size = 10
        center_area = DepthEstimator._get_center_area(frame, center_points, square_size)

        self.assertEqual(len(center_area), 1)
        self.assertEqual(center_area[0].shape[0], center_area[0].shape[1])
        self.assertEqual(center_area[0].shape[0], 2 * square_size)

    def test_estimate_depth(self):
        frame = (np.random.rand(640, 640, 3) * 100).astype('uint8')

        addon_processor = DepthEstimator(self.addon_config, self.model_settings, {}, {})
        res = addon_processor._estimate_depth(frame)

        self.assertEqual(res.shape, (640, 640))

        curr_config = self.addon_config.copy()
        curr_config['model_type'] = 'MiDaS_small'
        addon_processor = DepthEstimator(curr_config, self.model_settings, {}, {})
        res = addon_processor._estimate_depth(frame)

        self.assertEqual(res.shape, (640, 640))

    def test_post_process(self):
        addon_processor = DepthEstimator(self.addon_config, self.model_settings, {}, {})

        frame = (np.random.rand(640, 640, 3) * 100).astype('uint8')
        inference = Inference()

        test_object = AddonObject(frame=frame, inference=inference, shared={})
        result = addon_processor.post_process(test_object)

        self.assertEqual(len(result.inference.boxes), 0)

        # should be last after post process
        bb_1 = np.array([120, 150, 170, 200])
        class_1 = 1
        score_1 = 0.8

        # should be second after post process
        bb_2 = np.array([50, 60, 250, 380])
        class_2 = 0
        score_2 = 0.72

        # should be first after post process
        bb_3 = np.array([10, 10, 640, 640])
        class_3 = 1
        score_3 = 0.41

        inference.boxes = [bb_1, bb_2, bb_3]
        inference.classes = [class_1, class_2, class_3]
        inference.scores = [score_1, score_2, score_3]

        test_object = AddonObject(frame=frame, inference=inference, shared={})
        result = addon_processor.post_process(test_object)

        self.assertTrue((result.inference.boxes[0] == bb_3).all())
        self.assertTrue((result.inference.boxes[1] == bb_2).all())
        self.assertTrue((result.inference.boxes[2] == bb_1).all())


if __name__ == '__main__':
    unittest.main()
