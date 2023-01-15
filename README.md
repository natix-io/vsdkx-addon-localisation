## Dependency requirements

This project requires the following dependencies: 

- Python 3.8
- opencv-contrib-python==4.4.0.46
- timm
- torch==1.9.0
- torchvision==0.10.0
- pandas
- requests
- tqdm
- matplotlib
- seaborn

To install the dependencies via pip:

```
pip install -r requirements.txt
```

## DepthEstimation

This project uses the [MiDaS](https://github.com/isl-org/MiDaS) Depth Estimation 
model, trained on 10 datasets (ReDWeb, DIML, Movies, MegaDepth, WSVD, TartanAir,
HRWSI, ApolloScape, BlendedMVS, IRS), which predicts the depth of each pixel in 
the image. We employ the `DPT_Hybrid` model weights.

### Initialization
Initialization example:

```python
from DepthEstimation.core.models.depth_model import DepthEstimator

model_settings = {
   'device': 'cpu' # Device string used for pytorch (options: 'cpu'| 'gpu')
}
system_config = {'debug':
                    {
                    'debug_mode': True  # Bool Flag
                    },
                 'depth_estimation':
                    {'stages': 3, # Number of distance levels
                     'grid_size': 5, # Square size of objects center used for depth estimation
                     'model_type': 'DPT_Hybrid' # Depth estimation model's name
                     }
                 }

depth_estimator = DepthEstimator(
                model_settings=model_settings,
                system_config=system_config['depth_estimation'],
                debug_mode=system_config['debug']['debug_mode']
            )
```

### Input/ Output

This addon needs to be executed after inference as it relies on the information of the detected bounding boxes: 

- Input:

   ```python
   coords = addon_object.inference.boxes
   scores = addon_object.inference.scores
   classes = addon_object.inference.classes

   # estimate depth of every pixel of an inout image
   depth_img = self._estimate_depth(addon_object.frame)
   ```
   
- Output

   ```python
   # Ordered bounding boxes, scores and classes 
   addon_object.inference.boxes = sorted_coords
   addon_object.inference.scores = sorted_scores
   addon_object.inference.classes = sorted_classes
   # Distance IDs for each corresponding bounding box, the IDs correspond to the configured number of stages and grib size
   addon_object.inference.extra['distance_ids'] = stage_distance_ids
   ```
