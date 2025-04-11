import cv2
import numpy as np
import tkinter as tk

# Constants
capture_x, capture_y, capture_w, capture_h = 300, 300, 300, 700
box_size = 60

# Measurement box values
x_spacing = 92
y_spacing = 52
x_offset = 20
y_offset = 79
tilt_h = 0
tilt_v = 0

# Display variables
no_background = False
closed_tk = False

# Result array
color_res = [[""] * 2 for _ in range(4)]
color_val = [[""] * 2 for _ in range(4)]

BGR_color_limits = {
    "Red": [((0, 0, 200), (150, 150, 255))],
    "Blue": [((160, 0, 0), (255, 150, 150))],
    "Grey": [((100, 100, 100), (200, 200, 200))]
}

# Callback function for updating scale values
def update_scale(val):
    global x_spacing, y_spacing, x_offset, y_offset, tilt_h, tilt_v
    x_spacing = slider_spacing_x.get()
    y_spacing = slider_spacing_y.get()
    x_offset = slider_offset_x.get()
    y_offset = slider_offset_y.get()
    tilt_h = slider_tilt_h.get()
    tilt_v = slider_tilt_v.get()

# Toggle background visibility
def update_btn():
    global no_background
    no_background = not no_background

# Detect Tkinter close event
def closed(event):
    global closed_tk
    closed_tk = True

# Print function for debugging detected color level
def print_debug(array):
    for row in array:
        for element in row:
            for i in element:
                print(f"{int(i):>3} ", end='')
            print(";", end='')
        print(" | ", end='')
    print()
    
def tilt_image(image: np.ndarray, tilt_h: float, tilt_v: float) -> np.ndarray:    #! Virker ikke helt endnu

    h, w = image.shape[:2]

    # Define source points (original corners)
    src_pts = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    # Define destination points (simulate both horizontal & vertical tilt)
    dst_pts = np.float32([
        [tilt_h, tilt_v],         # Top-left moves
        [w + tilt_h, tilt_v],    # Top-right moves
        [-tilt_h, h - tilt_v],     # Bottom-left moves
        [w-tilt_h, h - tilt_v]  # Bottom-right moves
    ])

    # Compute perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # Apply transformation
    tilted_image = cv2.warpPerspective(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    return tilted_image

# Create Tkinter UI

win = tk.Tk()
win.title("Color Detection Settings")
win.protocol("WM_DELETE_WINDOW", lambda: closed(None))  # Catch window close event

# UI Elements
tk.Button(win, text="Toggle background", command=update_btn).pack(padx=50, pady=20)

slider_spacing_x = tk.Scale(win, from_=0, to=100, label="Spacing X", command=update_scale, orient="horizontal", length=200)
slider_spacing_x.pack()

slider_spacing_y = tk.Scale(win, from_=0, to=100, label="Spacing Y", command=update_scale, orient="horizontal", length=200)
slider_spacing_y.pack()

slider_offset_x = tk.Scale(win, from_=0, to=100, label="Offset X", command=update_scale, orient="horizontal", length=200)
slider_offset_x.pack()

slider_offset_y = tk.Scale(win, from_=0, to=100, label="Offset Y", command=update_scale, orient="horizontal", length=200)
slider_offset_y.pack()

slider_tilt_h = tk.Scale(win, from_=0, to=100, label="Tilt horisontal", command=update_scale, orient="horizontal", length=200)
slider_tilt_h.pack()

slider_tilt_v = tk.Scale(win, from_=0, to=100, label="Tilt vertical", command=update_scale, orient="horizontal", length=200)
slider_tilt_v.pack()
    
# Main loop
def update_frame(debug=False):
    if closed_tk and debug:
        win.quit()
        return

    # Frames
    screen = pyautogui.screenshot(region=(capture_x, capture_y, capture_w, capture_h))
    frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    frame = tilt_image(frame, tilt_h, tilt_v)
    blank_frame = np.zeros_like(frame)

    # Color reckgonition
    for row in range(4):
        for col in range(2):
            x = x_offset + col * (box_size + x_spacing)
            y = y_offset + row * (box_size + y_spacing)
            roi = frame[y:y+box_size, x:x+box_size]

            if roi.shape[0] == box_size and roi.shape[1] == box_size:
                roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mean_hsv = cv2.mean(roi_hsv)[:3]                
                mean_color = cv2.mean(roi)[:3]
                
                detected_color = "N/A"
                for color, ranges in BGR_color_limits.items():
                    for lower, upper in ranges:
                        if all(lower[i] <= mean_color[i] <= upper[i] for i in range(3)):
                            detected_color = color
                            break  # Stop at first match
                    if detected_color != "N/A":
                        break
                color_res[row][col] = detected_color
                color_val[row][col] = mean_color

                frame[y:y+box_size, x:x+box_size] = np.full((box_size, box_size, 3), mean_color, dtype=np.uint8)
                blank_frame[y:y+box_size, x:x+box_size] = np.full((box_size, box_size, 3), mean_color, dtype=np.uint8)
                cv2.rectangle(frame, (x, y), (x + box_size, y + box_size), (0, 255, 0), 1)
                cv2.rectangle(blank_frame, (x, y), (x + box_size, y + box_size), (0, 255, 0), 1)
                cv2.putText(frame, detected_color, (x, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0))
                cv2.putText(blank_frame, detected_color, (x, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0))
                
    if debug:
        cv2.imshow("Frame", blank_frame if no_background else frame)
        win.after(10, update_frame, True)  # Schedule next frame update
        #print_debug(color_val)
        print(color_res)
    else:
        return color_res

def debug():
    update_frame(True)
    win.mainloop()
    cv2.destroyAllWindows()
    
def get_colors(): 
    colors = update_frame()
    return colors
