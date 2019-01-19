def header_hook(header, data):
    """Called for each header"""

    for e in header.enums:
        e["x_namespace"] = e["namespace"]


def class_hook(cls, data):
    # fix enum paths
    for e in cls["enums"]["public"]:
        e["x_namespace"] = e["namespace"] + "::" + cls["name"] + "::"
