#!/usr/bin/env python3
import os
import sys
import shutil
import mimetypes
from PIL import Image
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pikepdf import Pdf

def nuke_image_metadata(filepath):
    try:
        image = Image.open(filepath)
        data = list(image.getdata())
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(data)
        new_image.save(filepath)
        print(f"[✓] Metadata removed from image: {filepath}")
    except Exception as e:
        print(f"[!] Error stripping image metadata: {e}")

def nuke_audio_metadata(filepath):
    try:
        audio = MP3(filepath, ID3=EasyID3)
        audio.delete()
        audio.save()
        print(f"[✓] Metadata removed from audio: {filepath}")
    except Exception as e:
        print(f"[!] Error stripping audio metadata: {e}")

def nuke_pdf_metadata(filepath):
    try:
        with Pdf.open(filepath) as pdf:
            pdf.save(filepath, preserve_pdfa=True, linearize=True)
        print(f"[✓] Metadata removed from PDF: {filepath}")
    except Exception as e:
        print(f"[!] Error stripping PDF metadata: {e}")

def nuke_metadata(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type:
        if mime_type.startswith("image"):
            nuke_image_metadata(filepath)
        elif mime_type == "application/pdf":
            nuke_pdf_metadata(filepath)
        elif mime_type.startswith("audio") or mime_type.startswith("video"):
            nuke_audio_metadata(filepath)
        else:
            print(f"[!] Unsupported file type: {mime_type}")
    else:
        print("[!] Could not determine file type.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 metadata_nuker.py <file1> [file2 file3 ...]")
        return
    for file in sys.argv[1:]:
        if os.path.isfile(file):
            backup = file + ".bak"
            shutil.copy2(file, backup)
            nuke_metadata(file)
        else:
            print(f"[!] File not found: {file}")

if __name__ == "__main__":
    main()
