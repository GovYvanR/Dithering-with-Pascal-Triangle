"""
Functions for Pascal's Triangle Operations

This Python file contains functions to generate Pascal's triangle, normalize its rows,
calculate the cumulative sum for each row, and print the triangle.

Functions:
- generate_pascals_triangle(N): Generates Pascal's triangle up to level N.
- normalize_triangle(triangle): Normalizes each row of the triangle.
- cumulative_sum(triangle): Calculates the cumulative sum for each normalized row of the triangle.
- print_pascals_triangle(triangle): Prints the Pascal's triangle with formatted output.
- get_cumulative_sum(N): Generates Pascal's triangle, normalizes its rows, calculates the
  cumulative sum for each row, and returns the resulting triangle.

Author: [Yvan Richard]
Date: [1st April 2024]
"""

def generate_pascals_triangle(N):
    triangle = []
    for i in range(N):
        row = [1]  # First element of each row is always 1
        if i > 0:
            prev_row = triangle[-1]  # Get the previous row
            for j in range(len(prev_row) - 1):  
                row.append(prev_row[j] + prev_row[j + 1])  # Calculate each element in the row
            row.append(1)  # Last element of each row is always 1
        triangle.append(row)  # Add the row to the triangle
    return triangle

def normalize_triangle(triangle):
    normalized_triangle = []
    for idx, row in enumerate(triangle):
        normalized_row = [element / (2 ** idx) for element in row]  # Normalize each element
        normalized_triangle.append(normalized_row)
    return normalized_triangle

def cumulative_sum(triangle):
    cumulative_triangle = []
    for row in triangle:
        cumulative_row = [sum(row[:i+1]) for i in range(len(row))]  # Calculate cumulative sum for each row
        cumulative_triangle.append(cumulative_row)
    return cumulative_triangle

def print_pascals_triangle(triangle):
    max_width = len(' '.join(map(str, triangle[-1])))  # Calculate maximum width for formatting
    for row in triangle:
        print(' '.join(map(lambda x: f'{x:.5f}', row)).center(max_width))  # Center-align and print each row

def get_cumulative_sum(N):
    triangle = generate_pascals_triangle(N)
    normalized_row_triangle = normalize_triangle(triangle)
    cumulative_row_triangle = cumulative_sum(normalized_row_triangle)
    return cumulative_row_triangle
