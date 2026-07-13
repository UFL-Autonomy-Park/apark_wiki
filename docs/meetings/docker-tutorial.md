---
title: Docker Tutorial (02/24/2026)
---

Docker is a tool for making containerized software. Puts all your dependencies in one box:

"It works on my computer." 

"Just ship the computer!"

Great for replicating software stacks on large fleets of devices. Virtual machine simulates entire computer (kernel, hardware, everything). You have to "boot" a virtual machine. Docker does none of that.

## Creating Images
All you need is a Dockerfile. The only required command is `FROM`. Docker Hub is where you can get images, which are OSs packaged up nicely. A minimal Ubuntu Dockerfile is given as
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

CMD["tail", "-f", "/dev/null"]
```
The `CMD` is what runs after the Docker container is built. Run `docker build .` in the same directory as your Dockerfile to build the image. Run `docker image list` to see all containers. You want to name them so you can differentiate between them. To do so, use tags. For instance,
```
docker build --tag demo:latest .
```

Will build the image, and let us run `docker run demo:latest` to run it. To check which containers are running, use `docker container ls`. We can stop the container using `docker stop demo:latest`, or use the container ID. If you want to work in the shell inside of the container, change your Dockerfile as
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

CMD["bash"]
```

## File Management
We need volumes to ensure persistence of files in the image. New files inside of the image disappear when the container restarts. To specify a volume, use the `-v` flag. The volume allows for connection between the filesystems on local and within the image. Any files changed or deleted on host/container are reflected (on both ends!). 

Volumes are extremely helpful when editing ROS2 nodes on Mac or Windows, because you can connect a dir on your host machine that is routed into your ROS2 development container. 

Alternatively, you can use `COPY` command in your Dockerfile. We can do  
```
FROM ubuntu:22.04

WORKDIR /home

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

COPY file.txt .

CMD["bash"]
```
inside of our Dockerfile. This will set the working directory to `/home` inside of the container, and then copy `file.txt` from our folder on the host PC to the container.

## apark-ros2 Repository
This is the development environment for the Autonomy Park on non-Ubuntu machines. Everything you could need in a package is specified in the Dockerfile. Building a fresh container for ROS2 takes about 6 minutes. You only have to build it once though! Note that builds do take up space on your machine. They can take up a ton of room, so it is important to check what you have sitting in your docker images. 

You can run `docker image prune` to remove all images that have been built but never used. To remove the `demo:latest` image, use `docker rmi -f demo:latest`. To remove all images, use `docker system prune`. Git is installed inside of the `apark-ros2` Docker container, so you can pull and push from inside of the container (just need to authenticate).

## VSCode and Docker
VSCode has an extension that allows you to run Docker containers inside of a terminal. It is the Dev Containers extension. 
