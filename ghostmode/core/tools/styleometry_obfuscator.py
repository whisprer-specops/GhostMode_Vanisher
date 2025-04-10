#!/usr/bin/env python3
import os
import random
import re
import argparse
from textblob import TextBlob
from pathlib import Path

# Optional chaos symbols
UNICODE_OBFUSCATION = ['\u200B', '\u200C', '\u200D', '\u2060', '\uFEFF', '​']

# Very basic synonym replacer using TextBlob
def synonym_swap(sentence):
    words = sentence.split()
    new_words = []
    for word in words:
        if len(word) > 4 and word.isalpha():
            blob = TextBlob(word)
            syns = blob.synsets
            if syns:
                lemmas = syns[0].lemma_names()
                alt = random.choice(lemmas)
                if alt.lower() != word.lower():
                    word = alt.replace("_", " ")
        new_words.append(word)
    return " ".join(new_words)

def shuffle_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    random.shuffle(sentences)
    return " ".join(sentences)

def add_unicode_noise(text):
    return ''.join(
        ch + (random.choice(UNICODE_OBFUSCATION) if random.random() < 0.1 else '')
        for ch in text
    )

def stylometry_obfuscate(text, chaos=False):
    obfuscated = []
    for sentence in re.split(r'(?<=[.!?]) +', text):
        if random.random() < 0.8:
            sentence = synonym_swap(sentence)
        if chaos and random.random() < 0.3:
            sentence = add_unicode_noise(sentence)
        obfuscated.append(sentence)
    random.shuffle(obfuscated)
    result = " ".join(obfuscated)
    return add_unicode_noise(result) if chaos else result

def main():
    parser = argparse.ArgumentParser(description="Stylometry Obfuscation Tool")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("-o", "--output", help="Output file (default: *_obf.txt)", default=None)
    parser.add_argument("--chaos", action="store_true", help="Enable high-entropy obfuscation")

    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print("[!] Input file does not exist.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        original = f.read()

    print("🧠 Obfuscating stylometry fingerprint...")
    altered = stylometry_obfuscate(original, chaos=args.chaos)

    output_path = args.output or f"{Path(args.input).stem}_obf.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(altered)

    print(f"✅ Obfuscated text saved to: {output_path}")

if __name__ == "__main__":
    main()
