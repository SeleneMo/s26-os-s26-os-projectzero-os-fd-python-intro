#!/usr/bin/env python3

import os
import re
from sys import argv

def main():
    if len(argv) != 3:
        os.write(2, f"Usage: {argv[0]} <input_file> <output_file>\n".encode())
        return 1
    
    inputFileName = argv[1]
    outputFileName = argv[2]
    
    # Open input file for reading
    fd_in = os.open(inputFileName, os.O_RDONLY)
    if fd_in < 0:
        os.write(2, f"Error: Could not open input file {inputFileName}\n".encode())
        return 1
    
    # Read entire file content
    file_content = b""
    while True:
        chunk = os.read(fd_in, 4096)  # Read in chunks
        if not chunk:
            break
        file_content += chunk
    
    os.close(fd_in)
    
    # Decode bytes to string
    text = file_content.decode('utf-8', errors='ignore')
    
    # Extract words: case-insensitive, exclude whitespace and punctuation
    # Using regex to find all words (alphanumeric sequences)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Count word occurrences
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by count (descending), then alphabetically for ties
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Open output file for writing (create/truncate)
    fd_out = os.open(outputFileName, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    if fd_out < 0:
        os.write(2, f"Error: Could not open output file {outputFileName}\n".encode())
        return 1
    
    # Write results: one word per line, format "word count"
    total_bytes_written = 0
    for word, count in sorted_words:
        line = f"{word} {count}\n"
        line_bytes = line.encode('utf-8')
        bytes_written = os.write(fd_out, line_bytes)
        total_bytes_written += bytes_written
    
    # Sync and close
    os.fsync(fd_out)
    os.close(fd_out)
    
    os.write(2, f"Wrote {total_bytes_written} bytes to {outputFileName}\n".encode())
    return 0

if __name__ == "__main__":
    exit(main())
