import cv2
from ultralytics import YOLO
import argparse
import time
import threading

# For cross-platform sound
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except:
    PLAYSOUND_AVAILABLE = False

# Optional: Windows only
try:
    import winsound
    WINSOUND_AVAILABLE = True
except:
    WINSOUND_AVAILABLE = False


# Play alert sound (threaded so it won't block)
def play_alert():
    if WINSOUND_AVAILABLE:
        winsound.Beep(2000, 400)   # frequency, ms
    elif PLAYSOUND_AVAILABLE:
        # Provide your own sound file (mp3 or wav)
        playsound("alert.mp3")     # <-- ADD alert.mp3 in same folder
    else:
        print("[!] No sound library available.")


parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="0")
parser.add_argument("--weights", type=str, default="yolov8n.pt")
parser.add_argument("--conf", type=float, default=0.35)
args = parser.parse_args()

model = YOLO(args.weights)
src = int(args.source) if args.source.isdigit() else args.source

cap = cv2.VideoCapture(src)
if not cap.isOpened():
    raise RuntimeError("Unable to open camera/video source")

last_alert_time = 0
cooldown = 3          # seconds before next alarm

print("Press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, conf=args.conf, verbose=False)
    r = results[0]

    box_found = False

    if r.boxes is not None and len(r.boxes) > 0:
        for box in r.boxes:
            # Box
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names.get(cls_id, str(cls_id))

            # Draw on screen
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            box_found = True

    # Trigger alarm if weapon found
    if box_found:
        now = time.time()
        if now - last_alert_time > cooldown:
            print("⚠️ ALERT! Weapon detected!")
            threading.Thread(target=play_alert).start()
            last_alert_time = now

    cv2.imshow("Weapon Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()