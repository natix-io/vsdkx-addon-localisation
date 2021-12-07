## Configuration

```yaml
addons:
  depth: 
    class: vsdkx.addon.depth.processor.DepthEstimator
    stages: 3 # Number of distance levels
    grid_size: 5 # Square size of objects center used for depth estimation 
    model_type: 'DPT_Hybrid' # Depth estimation model's name
```
