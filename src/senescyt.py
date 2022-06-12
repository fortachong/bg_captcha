# Decode captcha image with template matching

import sys
import os
import numpy as np
import cv2

# Default parameters
THR = 160
DEFAULT_TEMPLATE_MATCHING_THRESHOLD = 0.8
OFFSET_PIXELS = 2

# Template Class
class Template:
    def __init__(
        self,
        image_path,
        label,
        color,
        matching_threshold=DEFAULT_TEMPLATE_MATCHING_THRESHOLD
    ):
        self.image_path = image_path
        self.label = label
        self.color = color
        self.template = cv2.imread(image_path)
        self.template_height, self.template_width = self.template.shape[:2]
        self.matching_threshold = matching_threshold

# Return image in b&w
def img2bw(img, threshold=THR):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_inv = cv2.bitwise_not(gray)
    _, img_thr = cv2.threshold(gray_inv, threshold, 255, cv2.THRESH_BINARY)
    img_bw = cv2.cvtColor(img_thr, cv2.COLOR_GRAY2BGR)
    return img_bw

# Read Symbols
def symbols(path):
    symbols_templates = []
    for ifile in os.listdir(path):
        if ifile.endswith(".png"):
            p_ = os.path.join(path, ifile)
            l_, _ = os.path.splitext(ifile)
            label = l_[0]
            t_ = Template(
                image_path=p_,
                label=label,
                color=(0,0,255)
            )
            symbols_templates.append(t_)
    return symbols_templates


# Decode a B&W image using a symbols table
def decode(img_bw, symbols_templates):
    detections = []
    img_patch = img_bw
    width = img_patch.shape[1]
    offset = 0
    max_attempts = 20
    attempts = 0

    while offset < width:
        detections_ = []
        # Search template for all symbols
        for template in symbols_templates:
            template_matching = cv2.matchTemplate(
                template.template,
                img_patch,
                cv2.TM_CCOEFF_NORMED
            )
            match_locations = np.where(template_matching >= template.matching_threshold)
            for (x, y) in zip(match_locations[1], match_locations[0]):
                match = {
                    "TOP_LEFT_X": x,
                    "TOP_LEFT_Y": y,
                    "BOTTOM_RIGHT_X": x + template.template_width,
                    "BOTTOM_RIGHT_Y": y + template.template_height,
                    "MATCH_VALUE": template_matching[y, x],
                    "LABEL": template.label,
                    "COLOR": template.color
                }
                # Append to detections
                detections_.append(match)
        
        # If no detections, finish
        if len(detections_) > 0:
            # Find the first ones
            d_ = sorted(detections_, key=lambda obj: obj["TOP_LEFT_X"], reverse=False)
            fst_ = []
            fst_.append(d_[0])
            xmin = d_[0]["TOP_LEFT_X"]
            xmax = (xmin + d_[0]["BOTTOM_RIGHT_X"])//2
            filtered = list(filter(lambda obj: obj["TOP_LEFT_X"] <= xmax, d_[1:]))
            fst_ = fst_ + filtered
            # Sort and select the one with highest MATCH_VALUE
            fst_sorted = sorted(fst_, key=lambda obj["MATCH_VALUE"], reverse=True)
            detected = fst_sorted[0]
            # Reduce the image to search in
            old_x = detected["BOTTOM_RIGHT_X"]
            img_patch = img_patch[:,old_x+1-OFFSET_PIXELS:,:]
            # Update
            detected["TOP_LEFT_X"] = detected["TOP_LEFT_X"] + offset
            detected["BOTTOM_RIGHT_X"] = detected["BOTTOM_RIGHT_X"] + offset
            # Update offset
            offset += old_x + 1 - OFFSET_PIXELS
            detections.append(detected)
        else:
            break
        if attempts > max_attempts:
            break
        attempts += 1
        
    return detections

def get_string(detections):
    d_ = [d['LABEL'] for d in detections]
    return "".join(d_)


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
DIR_SYMBOLS = None

if __name__ == "__main__":
    # Read file
    if "-f" in opts:
        if len(args) > 0:
            PATH = args[0]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-i) (filepath) (-s) (directory)")

    # Symbols directory
    if "-s" in opts:
        if len(args) > 1:
            DIR_SYMBOLS = args[1]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-i) (filepath) (-s) (directory)")



    # Read Symbols
    st = symbols(DIR_SYMBOLS)

    # Read Image
    img = cv2.imread(PATH)
    img_bw = img2bw(img)

    # Detections
    detections = decode(img_bw, st)
    st = get_string(detections)
    print(st)
    print()