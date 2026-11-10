---
title: Go1
author: "Wyatt Cross, Max Gardenswartz"
updated: 2026-11-10
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  The Unitree Go1, the smaller of our two robot dogs: startup video, static transforms for the old dog hardware, and the manual.
---

![The Unitree Go1 quadruped robot in white and gray, with a carrying handle on top.](../../../images/ground-robots/unitree-go1.jpg){ width="40%" }

*The Go1, the smaller of the two Unitree robots (Unitree product image).*

!!! note "Brandon, This Page Needs Your Help"
    Brandon Fallin, please review this page. The Dog ROS2 Startup Instructions section is empty, and two of the three Go1s have no name or location yet. Please also tell us which Go1 is Dog 166 (if it exists), and mark which Go1s are ready to use.

--8<-- "rtk-first.md"

[RTK Setup](../../../hardware/rtk-setup.md){ .md-button }

The Go1 is the smaller of our two sizes of robot dog.

--8<-- "ground-docker.md"

## Our Go1s

We have three Go1s.

| Go1 | Ready to Use | Location | Last Updated |
|---|---|---|---|
| Scooby | *Unknown*{ .unknown } | Autonomy Park | 2026-11-06 |
| Name: *Unknown*{ .unknown } | *Unknown*{ .unknown } | Indoor Lab | 2026-11-06 |
| Name: *Unknown*{ .unknown } | *Unknown*{ .unknown } | *Unknown*{ .unknown } | 2026-11-06 |

## Quadruped Startup

<iframe width="560" height="315" src="https://www.youtube.com/embed/Iqmoot6-QBY?si=c1hXt8UjScOSQu9Z" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Dog ROS2 Startup Instructions

Coming soon

## Static Transforms

!!! note "Brandon, Please Check This Section"
    Brandon Fallin, please confirm that these static transforms are still relevant.

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

[Go1 Manual](go1-manual.pdf){ .md-button }
