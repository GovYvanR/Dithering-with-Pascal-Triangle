from PIL import Image
import numpy as np
import random, sys
import PascalTriangle



# Generates Pascal's triangle, normalizes its rows, calculates the
# cumulative sum for each row, and returns the resulting triangle.
# Estimate Overflow if Threshold different from 255
# Given Threshold Modulation (or jsut set at 127) the number of possibilities
# grow and the size of Pascal's Triangle as well
def gen_pascal_cdf(threshold):
    cumulative_row_triangle = PascalTriangle.get_cumulative_sum(max(threshold + 1, 512 - (threshold + 1)))

    # Convert cumulative_row_triangle to a NumPy array
    cumulative_row_triangle_array = np.array(cumulative_row_triangle, dtype=object)
    return cumulative_row_triangle_array

def is_gray_scale(image):
    #Check if the image is grayscale.
    return image.mode == 'L'

def convert_to_gray_scale(image):
    #Convert the image to grayscale.
    return image.convert('L')

def process_image(PCDF, image_path, mode, thr):
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

        # Generate empty memory array
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

                if (pixel_a == pixel_b):
                    index = pixel_a
                else:    
                    pixel_diff = abs(max(pixel_a, pixel_b) - min(pixel_a, pixel_b))

                    # Retrieve Corresponding Cumulative Row Sum
                    cum_row_sum = PCDF[abs(pixel_diff)]

                    # Find the index where the cumulative distribution first exceeds random number
                    index = np.argmax(cum_row_sum > random_numbers[y, x])

                    # Add Min from Neighboor Pixels
                    index = index + min(pixel_a, pixel_b)

                if mode == 1: #Dithering
                    # Sum Current Pixel and Index
                    pixel_x = pixel_x + index
                    # Perform Thresholding
                    if pixel_x > thr:
                        halftone[y, x] = 255
                        new_array[y, x] = pixel_x - 255
                    else:
                        new_array[y, x] = pixel_x
                elif mode == 2: #Smoothing with temporal dependencies  
                    if index < 0:
                       index = 0 
                    halftone[y, x] = index
                    new_array[y, x] = pixel_x - index
                elif mode == 3: #Smoothing without temporal dependencies
                    halftone[y, x] = index

    except FileNotFoundError:
        print("Error: Image file not found.")
    except Exception as e:
        print(f"Error: {e}")

    return halftone

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python PCADithering.py <image_path> <mode> <thr>")
        print("Using default options...")
        # Set default values for arguments
        image_path = "IMAGE_PNG/Lion.png"
        mode = 1
        threshold = 255 
    else:
        # Extract command-line arguments
        image_path = sys.argv[1]
        mode = int(sys.argv[2])
        if mode == 1:
            threshold = int(sys.argv[3])
        else:
            #For mode 1 & 2 threshold alsways iqual 255
            threshold = 255

    # Generate Pascal CDF
    PCDF = gen_pascal_cdf(threshold)

    # Process Image
    halftone = process_image(PCDF, image_path, mode, threshold)
    
    # Convert the halftone NumPy array to an image
    halftone = Image.fromarray(halftone)

    # Save the image as a PNG file
    filename_with_extension = image_path.split('/')[-1]
    filename_without_extension = filename_with_extension.split('.')[0]  
    halftone.save(filename_without_extension + '_IPCA.png')
