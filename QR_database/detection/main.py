import cv2, os, numpy as np
from pyzbar.pyzbar import decode
#from classes import Detection
from django.conf import settings
from pathlib import Path


detector = cv2.QRCodeDetector()
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
            
DEBUG_DIRECTORY = os.path.join(settings.MEDIA_ROOT, "debug", "scanner")
if not os.path.exists(DEBUG_DIRECTORY):
    os.makedirs(DEBUG_DIRECTORY)

def to_media_url_fragment(abs_path: str | Path) -> str:
    """
    Convert '/…/project/media/debug/scanner/foo.png' -> 'debug/scanner/foo.png'
    """
    rel = Path(abs_path).resolve().relative_to(Path(settings.MEDIA_ROOT).resolve())
    # Force forward slashes so the browser doesn’t get back‑slashes on Windows
    return rel.as_posix()

def get_detections(path: str, debug=False):
    """
`   Tuple of all QR code Detections

    If debug is set to true, then polylines will be drawn around the QR code and an
    annotated image will be outputted to debug/scanner/{image_name}_detections
    :return: Empty tuple if no qr codes are successfully detected in the image
    """
    img = cv2.imread(path)
    #cv2.imshow('Image Window Title', img)
    # cv2.waitKey(0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    codes = decode(gray)
    # print(f'{result=}')

    # found_code, payloads, points, _ = detector.detectAndDecodeMulti(img)
    #print(f'{payloads=}')
    # print(f'{points=}')
    result = []

    for code in codes:
        payload = code.data.decode("utf-8")
        points = np.array(code.polygon, dtype=np.float32)

        result.append(Detection(payload, points))

    if not codes:
        print("NOTHING")
        return (), None
    else:
        if debug:
            for det in result:
                pts = det.vertices.reshape((-1, 1, 2)).astype(int)
                img = cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
                if img is None:
                    print(f"[ERROR] Could not read image from {path}")
            fname = os.path.join(DEBUG_DIRECTORY,f"{path.split("/")[-1].split(".")[0]}_detections.png")
            print(f"Writing to {fname}")
            success = cv2.imwrite(fname, img)
            if success:
                print("Debug image saved!")
                debug_image_path = to_media_url_fragment(fname)
            else:
                print("failed")
        

        return result, debug_image_path

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    get_detections(path, True)


# class Detection:
#     def __init__(self, payload, vertices, anchor = False):
#         self.payload = payload
#         self.vertices = vertices

#         if anchor:
#             i_basis: np.ndarray = vertices[2] - vertices[1]
#             j_basis: np.ndarray = vertices[4] - vertices[1]
#             flipped: bool = np.cross(i_basis, j_basis) < 0

#             x, y = i_basis
#             if x == 0:
#                 # Check if x is vertical
#                 rot = (90 if vertices[2][1] > 0 else -90)
#             else:
#                 rot = np.atan(y/x)

#             if x < 0:
#                 if y >= 0:
#                     rot += 180
#                 else:
#                     rot -= 180
#             self.flipped = flipped
#             self.rot = rot
#             self.translate = vertices[1]
#             self.scale: float = np.linalg.norm(i_basis) / 100.0















