## ASCII Art Converter with Color Support
This is a Python script that converts images into ASCII art, with optional ANSI 24-bit color support, enhanced grayscale conversion, and dark/light mode rendering. It supports resizing and produces output suitable for viewing in terminals that support ANSI colors (like VS Code Terminal or Windows Terminal).

## Features

- Adjustable output height

- Optional true-color ANSI escape codes (great for terminal rainbow mode)

- Light and dark mode for ASCII contrast

- Improved grayscale conversion with luminance weighting

- Auto contrast and image enhancement before ASCII conversion

- Outputs to a .txt file

## Usage
1. Install dependencies
```bash
pip install pillow numpy
```
2. Run the script
```bash
python .\ascii_art.py test.png -o art.txt -d
```
3. Additional options
```bash
python ascii_art.py image.jpg --output art.txt --height 80 --dark --colour
```
### Option	Description
--output, -o	Output .txt file (default: ascii_art.txt)
--height, -H	Output height in characters (default: 100)
--dark, -d	Use dark characters on light background (inverted ramp)
--colour, -c	Enable colorized ASCII output using ANSI escape codes

## Example

python ascii_art.py lena.png --output lena_art.txt --colour --height 60
Then view it in a terminal that supports ANSI colors:

```bash
cat lena_art.txt
```

or alternatively

```bash
type lena_art.txt
```

## Works best in:

VS Code Terminal

Windows Terminal

iTerm2 (macOS)

less -R or bat for viewing with color support

##Output
By default, the ASCII art is written to ascii_art.txt. It uses a set of ASCII characters based on brightness:

```text
['@@', '$$', '##', '**', '!!', '==', ';;', '::', '~~', '--', ',,', '..','  ']
And in color mode, each character is printed with the original pixel color using 24-bit ANSI escape codes.
```

## ⚠️ Notes
Make sure your output terminal supports ANSI escape codes and truecolor (RGB) rendering.

File output is meant for terminal display; standard text editors won't render the colors.

## 🧪 Tips
View colored output with cat ascii_art.txt in a supported terminal.

For longer viewing: less -R ascii_art.txt

To create rainbow effects, use colorful input images and --colour flag.

## 📄 License
MIT – use and modify freely. Credit is appreciated.