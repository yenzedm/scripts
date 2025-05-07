import sys

def add_quotes_to_words(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # We divide the text into words, add quotes and combine them back
        words = content.split()
        quoted_words = ['`{}`'.format(word) for word in words]
        new_content = " ".join(quoted_words)

        # Overwriting a file with changed contents
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"File {file_path} processed!")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python add_quotes.py <path/to/file>")
        sys.exit(1)

    file_path = sys.argv[1]
    add_quotes_to_words(file_path)