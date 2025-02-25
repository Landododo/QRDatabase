import cv2, os, numpy as np

#from classes import Detection

detector = cv2.QRCodeDetector()

DEBUG_DIRECTORY = "./debug/scanner/"
if not os.path.exists(DEBUG_DIRECTORY):
    os.makedirs(DEBUG_DIRECTORY)

def get_detections(path: str, debug=False):
    """
`   Tuple of all QR code Detections

    If debug is set to true, then polylines will be drawn around the QR code and an
    annotated image will be outputted to debug/scanner/{image_name}_detections
    :return: Empty tuple if no qr codes are successfully detected in the image
    """
    img = cv2.imread(path)
    found_code, payloads, points, _ = detector.detectAndDecodeMulti(img)
    if not found_code:
        return ()
    else:
        result =  tuple(
            Detection(payload, point_set)
            for payload, point_set
            in zip(payloads, points)
            if payload
        )
        if debug:
            img = cv2.polylines(img, points.astype(int), True, (255, 0, 0), 2)
            for point_set in points:
                img = cv2.circle(img, point_set[0].astype(int), 3, (0, 255, 0), 2, cv2.FILLED,0)

            fname = DEBUG_DIRECTORY + f"{path.split("/")[-1].split(".")[0]}_detections.png"
            print(f"Writing to {fname}")
            print("Debug image saved!"
                  if cv2.imwrite(fname, img)
                  else "Failed to write debug image")
        return result

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    get_detections(path, True)


class Detection:
    def __init__(self, payload, vertices, anchor = False):
        self.payload = payload
        self.vertices = vertices

        if anchor:
            i_basis: np.ndarray = vertices[2] - vertices[1]
            j_basis: np.ndarray = vertices[4] - vertices[1]
            flipped: bool = np.cross(i_basis, j_basis) < 0

            x, y = i_basis
            if x == 0:
                # Check if x is vertical
                rot = (90 if vertices[2][1] > 0 else -90)
            else:
                rot = np.atan(y/x)

            if x < 0:
                if y >= 0:
                    rot += 180
                else:
                    rot -= 180
            self.flipped = flipped
            self.rot = rot
            self.translate = vertices[1]
            self.scale: float = np.linalg.norm(i_basis) / 100.0















