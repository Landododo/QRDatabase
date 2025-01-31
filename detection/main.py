import cv2, os

from classes import Detection

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







