---
title: Unitree Go1
---

# Unitree Go1

## Quadruped Startup

<iframe width="560" height="315" src="https://www.youtube.com/embed/Iqmoot6-QBY?si=c1hXt8UjScOSQu9Z" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Dog ROS2 Startup Instructions

Coming soon

## Static Transforms
For the old dog hardware, use the following static transforms in `minimal_startup_ground/launch/transforms.launch.py`
```python
("unitree", "go1"): {
    "gps": {
        "xyz": (
            0.0643814362384293,
            0.0592539620078344,
            0.152324955289927,
        ),
        "rpy": (0.0, 0.0, 0.0),
    },
    "imu": {
        "xyz": (
            0.246544261742116,
            0.000833506556606053,
            0.160178601155877,
        ),
        "rpy": (
            0.0,
            3.141592653589793,
            0.0,
        ),
    },
    "lidar": {
        "xyz": (
            0.212636626493108,
            0.00104806745515145,
            0.116780107191393,
        ),
        "rpy": (0.0, 0.0, 0.0),
    },
    "zed": {
        "xyz": (
            0.204953137519962,
            0.0010480674551517,
            0.173346896330377,
        ),
        "rpy": (
            0.0,
            0.2617993877991494,
            0.0,
        ),
    },
},
```

## Manual

[Go1 Manual](../../unitree/go1-manual.pdf)

## Harness/Frame

[Harness Manual](../../unitree/harness-manual.pdf)
