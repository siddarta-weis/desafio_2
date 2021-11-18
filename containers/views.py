from warnings import filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework import status

import docker


@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_list(request):
    try:
        if request.GET.get('status', None):
            #posible values are restarting, running, paused, exited
            filter_status = request.GET.get('status', None)
            containers = docker.from_env().containers.list(all=True, filters={'status': filter_status})
        else:
            containers = docker.from_env().containers.list(all=True)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    content = {}
    for container in containers:
        content[container.id] = container.attrs

    return Response(content, status=status.HTTP_200_OK)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_create(request):
    if isinstance(request.data, dict) and "Image" in request.data:
        try:
            cmd = request.data["Cmd"] if "Cmd" in request.data else ""
            container = docker.from_env().containers.run(
                request.data["Image"], cmd, detach=True
            )
            return Response(
                {"message": "Container created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"message": f"No such image {request.data['Image']}, or bad parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response({"message": "wrong format."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_start(request):
    if isinstance(request.data, dict) and "id" in request.data:
        try:
            container = docker.from_env().containers.get(request.data["id"])
            container.start()
            return Response({"message": "Container started"})
        except:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "wrong format"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_stop(request):
    if isinstance(request.data, dict) and "id" in request.data:
        try:
            container = docker.from_env().containers.get(request.data["id"])
            container.stop()
            return Response({"message": "Container stoped"})
        except:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "wrong format"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_remove(request, id):
    try:
        container = docker.from_env().containers.get(id)
        if container.status == "running":
            return Response({"message":"You cannot remove a running container"}, status=status.HTTP_400_BAD_REQUEST)
        container.remove()
    except Exception as e:
        print(e)
        return Response({"message": "didn't find image or wrong format"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "removed"})

@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def containers_stats(request, id):
    container = docker.from_env().containers.get(id).stats(stream=False)

    return Response(container)

@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def images_list(request):
    images = docker.from_env().images.list()

    content = {}
    for image in images:
        content[image.tags[0]] = image.attrs

    return Response(content, status=status.HTTP_200_OK)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def images_create(request):
    if isinstance(request.data, dict) and "fromImage" in request.data:
        try:
            image = docker.from_env().images.pull(request.data["fromImage"])
        except:
            return Response(
                {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": f"{image.tags[0]} pulled successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response({"message": "wrong format."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def images_remove(request, name):
    try:
        image = docker.from_env().images.remove(image=name)
    except:
        return Response(
            {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"Deleted": name}, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def networks_list(request):
    try:
        if request.GET.get('driver', None):
            #possible values are bridge, host, overlay, ipvlan, macvlan, none
            filter_driver = request.GET.get('driver', None)
            networks = docker.from_env().networks.list(filters={'driver': filter_driver})
        else:
            networks = docker.from_env().networks.list()

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    content = {}

    for network in networks:
        content[network.id] = network.attrs

    return Response(content)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def networks_create(request):
    if isinstance(request.data, dict) and "Name" in request.data:
        network_name = request.data["Name"]
        try:
            docker.from_env().networks.create(network_name)
            return Response(
                {"message": f"Network {network_name} was created successfuly"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
            )
    return Response({"message": "wrong format."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def networks_remove(request, id):
    try:
        network = docker.from_env().networks.get(id)
        network.remove()
    except:
        return Response(
            {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"Deleted": id})


@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def volumes_list(request):
    volumes = docker.from_env().volumes.list()

    content = {}

    for volume in volumes:
        content[volume.name] = volume.attrs

    return Response(content)


@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def volumes_create(request):
    if isinstance(request.data, dict) and "Name" in request.data:
        volume_name = request.data["Name"]
        try:
            docker.from_env().volumes.create(volume_name)
            return Response(
                {"message": f"Volume {volume_name} was created successfuly"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
            )
    return Response({"message": "wrong format."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def volumes_remove(request, name):
    try:
        volume = docker.from_env().volumes.get(name)
        volume.remove()
    except:
        return Response(
            {"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"Deleted": name})
