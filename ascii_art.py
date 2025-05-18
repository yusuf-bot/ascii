import argparse
import os
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def resize_image(image, new_height=100):
    """Resize the image to have a specified height while maintaining aspect ratio."""
    width, height = image.size
    print(f"Original image dimensions: {width}x{height}")
    new_width = int(width * (new_height / height))
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def enhance_for_grayscale(image):
    """Enhance image for better grayscale conversion results."""
    # Increase contrast slightly
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1.15)  # Increase contrast by 15%
    
    # Sharpen the image to preserve details
    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(1.2)  # Increase sharpness by 20%
    
    return image

def custom_grayscale(image):
    """Convert to grayscale using proper luminance weights for better results."""
    # Convert image to numpy array for faster processing
    img_array = np.array(image)
    
    # If image is already grayscale, return it
    if len(img_array.shape) == 2:
        return Image.fromarray(img_array)
    
    # Apply luminance formula: 0.21R + 0.72G + 0.07B with NumPy for speed
    if image.mode != "RGB":
        image = image.convert("RGB")
        img_array = np.array(image)
    
    r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    grayscale = (0.21 * r + 0.72 * g + 0.07 * b).astype(np.uint8)
    
    # Convert back to PIL Image
    result = Image.fromarray(grayscale)
    
    # Adjust black and white points for better dynamic range
    min_val = 5  # Avoid pure black
    max_val = 250  # Avoid pure white
    result = ImageOps.autocontrast(result, cutoff=(min_val/255*100, (255-max_val)/255*100))
    
    return result

def rgb_to_ansi(r, g, b):
    """Convert RGB values to ANSI 24-bit color escape sequence."""
    return f"\033[38;2;{r};{g};{b}m"

def convert_to_ascii(image_path, output_path, colour, dark_mode=False, new_height=100):
    """
    Convert an image to ASCII art with the following steps:
    1. Resize to specified height
    2. Enhance image for grayscale conversion
    3. Convert to grayscale using proper luminance weights
    4. Map grayscale values to ASCII characters
    5. If color mode is on, apply the original pixel color to each character
    6. Save the ASCII art to a text file
    """
    # ASCII characters from darkest to lightest
    ascii_chars = ["  ",'..', ',,', '--', '~~', '::', ';;', '==', '!!', '**', '##', '$$', '@@'] if dark_mode else ['@@', '$$', '##', '**', '!!', '==', ';;', '::', '~~', '--', ',,', '..','  ']
    if colour:
        ascii_chars = ["<3"]
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Resize image
            img = resize_image(img, new_height)
            
            # Store original colored image if color mode is enabled
            original_img = img.copy() if colour else None
            
            # Enhance image for better grayscale conversion
            img = enhance_for_grayscale(img)
            
            # Convert to grayscale with improved method
            grayscale_img = custom_grayscale(img)
            
            # Calculate width of ASCII art
            width, height = grayscale_img.size
            
            # Convert grayscale image to numpy array for faster processing
            gray_array = np.array(grayscale_img)
            
            # Create a list to store ASCII art
            ascii_art = []
            
            # Convert image to ASCII
            for y in range(height):
                line = ""
                for x in range(width):
                    # Get pixel grayscale value (0-255)
                    pixel_value = gray_array[y, x]
                    
                    # Map the pixel value to one of the character ranges
                    range_index = int(pixel_value / (255/len(ascii_chars)))
                    if range_index >= len(ascii_chars):  # Ensure index is within bounds
                        range_index = len(ascii_chars) - 1
                    
                    # Get the corresponding character
                    char = ascii_chars[range_index]
                    
                    # Apply color if color mode is enabled
                    if colour and original_img:
                        # Get RGB values from original image
                        r, g, b = original_img.getpixel((x, y))[:3]
                        # Add ANSI color to character
                        char = f"{rgb_to_ansi(r, g, b)}{char}\033[0m"
                    
                    line += char
                ascii_art.append(line)
            
            # Save ASCII art to file
            with open(output_path, 'w') as f:
                f.write('\n'.join(ascii_art))
            
            print(f"ASCII art saved to {output_path}")
            print(f"Image dimensions: {grayscale_img.size}")
            print(f"ASCII dimensions: {width}x{height}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    parser.add_argument('image_path', help='Path to the input image')
    parser.add_argument('--output', '-o', help='Path to the output text file', default='ascii_art.txt')
    parser.add_argument('--dark', '-d', action='store_true', help='Use dark mode (dark characters on light background)')
    parser.add_argument('--height', '-H', type=int, default=100, help='Height of the output in characters (default: 100)')
    parser.add_argument('--colour', '-c', action='store_true', help='Enable colored ASCII art output')
    args = parser.parse_args()
    
    # Ensure output path has a .txt extension
    if not args.output.endswith('.txt'):
        args.output += '.txt'
    
    convert_to_ascii(args.image_path, args.output, args.colour, args.dark, args.height)