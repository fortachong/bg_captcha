# Convert to BW

import sys
import os
import cv2

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

DIR_INPUT = None
DIR_OUTPUT = None
THR = 160

if __name__ == "__main__":
    if "-i" in opts:
        if len(args) > 0:
            DIR_INPUT = args[0]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-i) (directory) -o (directory)")

    if "-o" in opts:
        if len(args) > 1:
            DIR_OUTPUT = args[1]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-i) (directory) -o (directory)")

    if (DIR_INPUT is None) or (DIR_OUTPUT is None):
        raise SystemExit(f"Usage: {sys.argv[0]} (-i) (directory) -o (directory)")

    if not os.path.isdir(DIR_OUTPUT):
        os.mkdir(DIR_OUTPUT)

    for ifile in os.listdir(DIR_INPUT):
        if ifile.endswith(".png"):
            # Process image file
            path = os.path.join(DIR_INPUT, ifile)
            print(f"Reading file {path}")

            # Read image file -> gray scale -> inversion -> threshold
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_inv = cv2.bitwise_not(gray)
            _, img_thr = cv2.threshold(gray_inv, THR, 255, cv2.THRESH_BINARY)

            # Save to DIR_OUTPUT
            filename, extension = os.path.splitext(ifile)
            opath = os.path.join(DIR_OUTPUT, filename + '_bw' + extension)
            print(f"Writing file {opath}")
            cv2.imwrite(opath, img_thr)



            

    