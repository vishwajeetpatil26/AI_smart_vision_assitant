
def generate_alert(detections):
    """
    Prioritize detected objects using approximate distance.
    Expected fields:
    object, position, confidence, distance
    """

    if not detections:
        return None

    priority = {
        "car": 1,
        "truck": 1,
        "bus": 1,
        "motorcycle": 1,
        "person": 2,
        "bicycle": 2,
        "chair": 3,
    }

    def risk_score(item):
        distance = item.get("distance")

        if distance is None:
            return priority.get(item.get("object"), 99) * 10

        if distance < 1.0:
            return 0
        elif distance < 2.0:
            return 10
        elif distance < 4.0:
            return 20

        return 30 + priority.get(item.get("object"), 99)

    selected = min(detections, key=risk_score)

    obj = selected.get("object", "obstacle")
    position = selected.get("position", "ahead")
    distance = selected.get("distance")

    if distance is not None:
        return f"{obj} detected {distance:.1f} meters away, {position}"

    return f"{obj} detected {position}"
