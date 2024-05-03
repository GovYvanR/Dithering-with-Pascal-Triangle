from PIL import Image
import numpy as np
import random, sys
import PascalTriangle

#Work in uint8 or int16 mode  
#Configure Threshold (255 default uint8)
#Entry to theshold modulation control (here fixed)
Threshold = 255

# Generates Pascal's triangle, normalizes its rows, calculates the
# cumulative sum for each row, and returns the resulting triangle.
cumulative_row_triangle = PascalTriangle.get_cumulative_sum(max(Threshold + 1, 512 - (Threshold + 1)))

# Convert cumulative_row_triangle to a NumPy array
cumulative_row_triangle_array = np.array(cumulative_row_triangle, dtype=object)

def is_gray_scale(image):
    #Check if the image is grayscale.
    return image.mode == 'L'

def convert_to_gray_scale(image):
    #Convert the image to grayscale.
    return image.convert('L')

def process_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Check if the image is grayscale
        if is_gray_scale(img):
            print("Image is already grayscale.")
        else:
            # Convert the image to grayscale
            img = convert_to_gray_scale(img)
            print("Image converted to grayscale.")

        # Convert the image to a NumPy array
        img_array = np.array(img)

        # Get the size of the img_array
        height, width = img_array.shape

        # Generate empty memory array with the same size as the image
        halftone = np.zeros((height, width), dtype=np.uint8)

        # Copying the array with a new type (int16)
        # Thresholding type change
        new_array = img_array.astype(np.int16)

        # Generate a random number array of the same size as the image
        random_numbers = np.random.rand(height, width)    

        # Perform a serpentine scan of the image
        for y in range(1, height):
            direction = 1 if y % 2 == 0 else -1  # Set direction based on even or odd rows
            start_pixel = 1 if direction == 1 else width - 2  # Start pixel index
            end_pixel = width - 1 if direction == 1 else 0  # End pixel index
            for x in range(start_pixel, end_pixel, direction):
                pixel_x = new_array[y, x]   # Current pixel
                pixel_a = new_array[y - 1, x] # Top neighbor Pixel
                pixel_b = new_array[y, x - direction] # Left or Right serpentine neighbor Pixel
                
                # Diff of Neighbor Pixels
                #       B
                #   A   X          
                pixel_diff = max(pixel_a, pixel_b) - min(pixel_a, pixel_b)

                # Retrieve Corresponding Cumulative Row Sum
                cum_row_sum = cumulative_row_triangle_array[abs(pixel_diff)]

                # Find the index where the cumulative distribution first exceeds random number
                index = np.argmax(cum_row_sum > random_numbers[y, x])

                # Add Min from Neighboor Pixels
                index = index + min(pixel_a, pixel_b)

                # Sum Current Pixel and Index
                pixel_x = pixel_x + index

                # Perform Thresholding
                if pixel_x > Threshold:
                    halftone[y, x] = 255
                    new_array[y, x] = pixel_x - 255
                else:
                    new_array[y, x] = pixel_x
    

    except FileNotFoundError:
        print("Error: Image file not found.")
    except Exception as e:
        print(f"Error: {e}")

    return halftone

if __name__ == "__main__":
    if len(sys.argv) != 1:  #2
        print("Usage: python PCADithering.py <image_path>")
        sys.exit(1)

    image_path = 'IMAGE_PNG/Lion.png'
    #image_path = sys.argv[1]
    halftone = process_image(image_path)
    
    # Convert the halftone NumPy array to an image
    halftone = Image.fromarray(halftone)

    # Save the image as a PNG file
    filename_with_extension = image_path.split('/')[-1]
    filename_without_extension = filename_with_extension.split('.')[0]  
    halftone.save(filename_without_extension + '_HT3.png')
