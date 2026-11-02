
import cv2
import numpy as np
import os
from datetime import datetime
from cvzone.HandTrackingModule import HandDetector

# =============== CONFIGURATION ===============
WIDTH, HEIGHT = 1280, 720
HEADER = 105
BRUSH_SIZE = 8
ERASER_SIZE = 40

# OpenCV colors use BGR format
COLORS = [
    ("BLUE", (255, 100, 30)),
    ("GREEN", (40, 210, 70)),
    ("RED", (50, 50, 240)),
    ("YELLOW", (0, 220, 255)),
    ("WHITE", (255, 255, 255)),
]

BACKGROUND = (24, 27, 35)
PANEL = (37, 42, 53)
TEXT = (240, 243, 248)
MUTED = (165, 175, 190)
ACCENT = (255, 180, 50)

# =============== INITIALIZATION ===============
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
current_color_name = "BLUE"
current_color = COLORS[0][1]
current_tool = "BRUSH"
previous_point = None

brush_size = BRUSH_SIZE
eraser_size = ERASER_SIZE
message = "Ready to paint"
message_until = 0

detector = HandDetector(maxHands=1, detectionCon=0.7)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

if not cap.isOpened():
    print("Could not open webcam.")
    raise SystemExit

os.makedirs("drawings", exist_ok=True)


def show_message(text):
    global message, message_until
    message = text
    message_until = datetime.now().timestamp() + 2


# =============== DRAW INTERFACE ===============
def draw_interface(frame):
    # Modern dark toolbar
    cv2.rectangle(frame, (0, 0), (WIDTH, HEADER), BACKGROUND, -1)

    cv2.putText(
        frame, "AIR PAINT", (20, 32),
        cv2.FONT_HERSHEY_DUPLEX, 0.9, TEXT, 2
    )
    cv2.putText(
        frame, "GESTURE DRAWING STUDIO", (20, 56),
        cv2.FONT_HERSHEY_SIMPLEX, 0.43, MUTED, 1
    )

    buttons = []
    start_x = 275
    button_w = 105
    gap = 9

    # Color palette
    for i, (name, color) in enumerate(COLORS):
        x1 = start_x + i * (button_w + gap)
        x2 = x1 + button_w

        cv2.rectangle(
            frame, (x1, 13), (x2, 60), PANEL, -1
        )
        cv2.circle(
            frame, (x1 + 17, 36), 8, color, -1
        )
        cv2.putText(
            frame, name, (x1 + 30, 41),
            cv2.FONT_HERSHEY_SIMPLEX, 0.43, TEXT, 1
        )

        if current_color_name == name and current_tool == "BRUSH":
            cv2.rectangle(
                frame, (x1, 13), (x2, 60), ACCENT, 2
            )
        else:
            cv2.rectangle(
                frame, (x1, 13), (x2, 60), (75, 82, 96), 1
            )

        buttons.append((name, x1, 13, x2, 60))

    # Eraser and clear controls
    controls = [
        ("ERASER", 845, 13, 965, 60),
        ("CLEAR", 975, 13, 1095, 60),
        ("SAVE", 1105, 13, 1215, 60),
    ]

    for name, x1, y1, x2, y2 in controls:
        selected = (
            (name == "ERASER" and current_tool == "ERASER")
        )
        fill = (95, 75, 55) if selected else PANEL

        cv2.rectangle(frame, (x1, y1), (x2, y2), fill, -1)
        cv2.rectangle(
            frame, (x1, y1), (x2, y2),
            ACCENT if selected else (75, 82, 96), 2 if selected else 1
        )
        cv2.putText(
            frame, name, (x1 + 12, 41),
            cv2.FONT_HERSHEY_SIMPLEX, 0.52, TEXT, 1
        )
        buttons.append((name, x1, y1, x2, y2))

    # Instructions
    cv2.putText(
        frame,
        "1 FINGER: DRAW     2 FINGERS: SELECT TOOL",
        (20, 87), cv2.FONT_HERSHEY_SIMPLEX,
        0.48, MUTED, 1
    )

    cv2.putText(
        frame,
        f"Tool: {current_tool}  |  Brush: {brush_size}  |  Eraser: {eraser_size}",
        (770, 87), cv2.FONT_HERSHEY_SIMPLEX,
        0.48, TEXT, 1
    )

    return buttons


# =============== MAIN APPLICATION ===============
try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read webcam.")
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        hands, frame = detector.findHands(frame, draw=True)
        buttons = draw_interface(frame)

        if hands:
            hand = hands[0]
            landmarks = hand["lmList"]

            x, y = landmarks[8][0], landmarks[8][1]
            fingers = detector.fingersUp(hand)

            index_up = fingers[1] == 1
            middle_up = fingers[2] == 1

            # Two fingers: choose a toolbar option
            if index_up and middle_up:
                previous_point = None
                cv2.circle(frame, (x, y), 12, ACCENT, 2)

                if y < HEADER:
                    for name, x1, y1, x2, y2 in buttons:
                        if x1 <= x <= x2 and y1 <= y <= y2:
                            if name == "CLEAR":
                                canvas[:] = 0
                                show_message("Canvas cleared")

                            elif name == "ERASER":
                                current_tool = "ERASER"
                                show_message("Eraser selected")

                            elif name == "SAVE":
                                filename = datetime.now().strftime(
                                    "drawings/painting_%Y%m%d_%H%M%S.png"
                                )
                                if cv2.imwrite(filename, canvas):
                                    show_message("Artwork saved")
                                else:
                                    show_message("Could not save artwork")

                            else:
                                current_color_name = name
                                current_color = dict(COLORS)[name]
                                current_tool = "BRUSH"
                                show_message(name + " selected")

                            break

            # One index finger: draw
            elif index_up and not middle_up:
                if y > HEADER:
                    point = (x, y)

                    if previous_point is not None:
                        if current_tool == "ERASER":
                            cv2.line(
                                canvas, previous_point, point,
                                (0, 0, 0), eraser_size
                            )
                        else:
                            cv2.line(
                                canvas, previous_point, point,
                                current_color, brush_size
                            )

                    previous_point = point
                    cv2.circle(frame, point, 5, ACCENT, -1)
                else:
                    previous_point = None

            else:
                previous_point = None

        else:
            previous_point = None

        # Merge artwork with webcam view
        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        inverse_mask = cv2.bitwise_not(mask)

        background = cv2.bitwise_and(frame, frame, mask=inverse_mask)
        drawing = cv2.bitwise_and(canvas, canvas, mask=mask)
        output = cv2.add(background, drawing)

        # Bottom status panel
        cv2.rectangle(
            output, (0, HEIGHT - 38), (WIDTH, HEIGHT),
            BACKGROUND, -1
        )

        cv2.putText(
            output, message, (20, HEIGHT - 13),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, TEXT, 1
        )

        cv2.putText(
            output, "[+/-] Brush   [E] Eraser   [C] Clear   [S] Save   [Q] Quit",
            (620, HEIGHT - 13),
            cv2.FONT_HERSHEY_SIMPLEX, 0.43, MUTED, 1
        )

        cv2.imshow("Air Paint - Gesture Drawing Studio", output)

        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):
            break
        elif key == ord("c"):
            canvas[:] = 0
            show_message("Canvas cleared")
        elif key == ord("e"):
            current_tool = "ERASER"
            show_message("Eraser selected")
        elif key == ord("b"):
            current_tool = "BRUSH"
            show_message("Brush selected")
        elif key in (ord("+"), ord("=")):
            brush_size = min(brush_size + 2, 40)
            show_message("Brush size increased")
        elif key in (ord("-"), ord("_")):
            brush_size = max(brush_size - 2, 2)
            show_message("Brush size decreased")
        elif key == ord("s"):
            filename = datetime.now().strftime(
                "drawings/painting_%Y%m%d_%H%M%S.png"
            )
            if cv2.imwrite(filename, canvas):
                show_message("Artwork saved: " + filename)
            else:
                show_message("Could not save artwork")

finally:
    cap.release()
    cv2.destroyAllWindows()
