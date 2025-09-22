from ultralytics import YOLO
import os, cv2

def blur_photo(imagePath, file_name):
    model = YOLO(r"model/best.pt")

    results = model.predict(source=imagePath, conf=0.5, save=False, show=False)

    # Load original image
    img = cv2.imread(imagePath)

    h_orig, w_orig = img.shape[:2]

    for r in results:
        h_pred, w_pred = r.orig_shape  # YOLO's original detected image shape
        scale_w, scale_h = w_orig / w_pred, h_orig / h_pred

        for box in r.boxes.xyxy:  # xyxy format
            x1, y1, x2, y2 = map(int, box.tolist())

            # Scale boxes back to original resolution
            x1 = int(x1 * scale_w)
            x2 = int(x2 * scale_w)
            y1 = int(y1 * scale_h)
            y2 = int(y2 * scale_h)

            # Extract ROI and apply Gaussian blur
            roi = img[y1:y2, x1:x2]
            if roi.size > 0:
                roi = cv2.GaussianBlur(roi, (51, 51), 30)
                img[y1:y2, x1:x2] = roi

    cv2.imwrite(os.path.join("final_data", file_name), img)
    return os.path.join("final_data", file_name)

