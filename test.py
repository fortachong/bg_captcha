# Perform test with labeled image set
import os
import sys
import numpy as np
import cv2
import senescyt as se


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
DIR_SYMBOLS = None
DIR_TEST = None

if __name__ == "__main__":
    # Test Images Directory
    if "-t" in opts:
        if len(args) > 0:
            DIR_TEST = args[0]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-t) (directory) (-s) (directory)")

    # Symbols Directory
    if "-s" in opts:
        if len(args) > 1:
            DIR_SYMBOLS = args[1]
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-t) (directory) (-s) (directory)")

    if (DIR_TEST is None) or (DIR_SYMBOLS is None):
        raise SystemExit(f"Usage: {sys.argv[0]} (-t) (directory) (-s) (directory)")

    # Read Symbols
    st = se.symbols(DIR_SYMBOLS)
    
    # Read and decode all images from DIR_TEST
    n_files = 0
    n_true = 0
    errors = []
    for ifile in os.listdir(DIR_TEST):
        if ifile.endswith(".png"):
            n_files += 1
            # Process image file
            path = os.path.join(DIR_TEST, ifile)
            print(f"Reading file {path}")

            # Read image 
            img = cv2.imread(path)

            # Extract label
            label, _ = os.path.splitext(ifile)

            # Process and decode Image
            img_bw = se.img2bw(img, threshold=se.THR)
            detections = se.decode(img_bw, st)
            string_decoded = se.get_string(detections)
            print(f"Label = {label}, Detected = {string_decoded}")
            if label == string_decoded:
                n_true += 1
            else:
                errors.append((ifile, string_decoded))

    n_errors = n_files - n_true
    error_rate = n_errors / n_files
    print(f"Error Rate = {error_rate}")
    print("-"*20)
    if len(errors) > 0:
        print("Files with errors")
        for fname, dec in errors:
            print(f"Filename: {fname}, Decoded: {dec}")

