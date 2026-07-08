# weapon_detect.py
import cv2
from ultralytics import YOLO
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="0", help="0 for webcam or path to video/image")
parser.add_argument("--weights", type=str, default="yolov8n.pt", help="path to model weights (.pt). Use 'yolov8n.pt' for a small pretrained model or your custom best.pt")
parser.add_argument("--conf", type=float, default=0.35, help="confidence threshold")
parser.add_argument("--save", action="store_true", help="save annotated output to out.mp4")
args = parser.parse_args()

# Load model
model = YOLO(args.weights)  # can be "yolov8n.pt" or "runs/detect/exp/weights/best.pt"

# If using webcam
src = int(args.source) if args.source.isdigit() else args.source
cap = cv2.VideoCapture(src)
if not cap.isOpened():
    raise RuntimeError(f"Unable to open source {args.source}")

# output video writer (optional)
writer = None
if args.save:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    writer = cv2.VideoWriter("out.mp4", fourcc, fps, (w, h))

print("Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # run detection (returns list of Results)
    results = model.predict(source=frame, conf=args.conf, half=False, verbose=False)  # passing frame directly
    # results is a list; take first result
    r = results[0]

    # r.boxes.xyxy, r.boxes.conf, r.boxes.cls
    boxes = r.boxes
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int)  # [x1,y1,x2,y2]
            conf = float(box.conf[0].cpu().numpy())
            cls_id = int(box.cls[0].cpu().numpy())
            label = model.names.get(cls_id, str(cls_id))
            x1, y1, x2, y2 = xyxy
            # draw
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            text = f"{label} {conf:.2f}"
            cv2.putText(frame, text, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("weapon-detect", frame)
    if writer:
        writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
if writer:
    writer.release()
cv2.destroyAllWindows()