#!/usr/bin/env python3

import argparse
import fitz
import os

def crop_pdf(input_pdf_path, output_pdf_path, left=0, bottom=0, right=0, top=0):
    doc = fitz.open(input_pdf_path)

    for page in doc:
        rect = page.rect
        new_rect = fitz.Rect(
            rect.x0 + left,
            rect.y0 + top,
            rect.x1 - right,
            rect.y1 - bottom
        )
        page.set_cropbox(new_rect)

    doc.save(output_pdf_path)

def main():
    parser = argparse.ArgumentParser(description="Crop margins from a PDF file.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_pdf", help="Path to save the cropped PDF file.")
    parser.add_argument("--cropleft", type=float, default=0, help="Crop margin from the left in points.")
    parser.add_argument("--cropbottom", type=float, default=0, help="Crop margin from the bottom in points.")
    parser.add_argument("--cropright", type=float, default=0, help="Crop margin from the right in points.")
    parser.add_argument("--croptop", type=float, default=0, help="Crop margin from the top in points.")
    
    args = parser.parse_args()

    crop_pdf(args.input_pdf, args.output_pdf,
             left=args.cropleft, bottom=args.cropbottom,
             right=args.cropright, top=args.croptop)

if __name__ == "__main__":
    main()
