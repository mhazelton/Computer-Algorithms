
"""
CISC-4080-R01, Lab 1

Purpose:
    - Read integers from a file into a list
    - Implement linear search 
    - Implement selection sort
    - Implement binary search
    - Compare running times

Author: Max Hazelton
Last Modified: 09/08/25
Known Bugs:
    - None known

Notes:
    - Indices in functions are 0-based. For display we print 1-based positions.
    - Input file should contain one integer per line.
"""

import time

# File reading
def read_integers(filename):
    """
    Read integers from a text file.

    Params:
        filename (str): path to a text file, one integer per line.
    Pre-conditions:
        - File exists and lines are valid integers.
    Post-conditions:
        - Returns a list of ints in file order.
    """
    nums = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line != "":
                nums.append(int(line))
    return nums


# Linear search
def linear_search(a, target):
    """
    Linear search for all occurrences.

    Params:
        a (list[int]): unsorted list
        target (int): value to find
    Pre-conditions:
        - a is a list of ints
    Post-conditions:
        - Returns list of 0-based indices where a[i] == target
    """
    indices = []
    for i in range(len(a)):
        if a[i] == target:
            indices.append(i)
    return indices


# Selection sort (in-place)
def selection_sort(a):
    """
    Sort the list in non-decreasing order using selection sort (in-place).

    Params:
        a (list[int]): list to sort
    Pre-conditions:
        - a is a list of ints
    Post-conditions:
        - a is sorted in-place; function returns None
    """
    n = len(a)
    for i in range(n - 1):
        min_pos = i
        for j in range(i + 1, n):
            if a[j] < a[min_pos]:
                min_pos = j
        if min_pos != i:
            a[i], a[min_pos] = a[min_pos], a[i]


# Binary search (on sorted list)
def binary_search(a, target):
    """
    Standard binary search for one occurrence.

    Params:
        a (list[int]): sorted list (non-decreasing)
        target (int): value to find
    Pre-conditions:
        - a is sorted
    Post-conditions:
        - Returns a 0-based index where target occurs, or -1 if not found
    """
    low = 0
    high = len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        if a[mid] == target:
            return mid
        elif a[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# (Extra credit) Return the full range of duplicate indices [first, last]
def binary_search_range(a, target):
    """
    Return [first_index, last_index] where target appears in sorted list a,
    or None if target not found. Indices are 0-based.

    This extends binary search to find the boundary indices.
    """
    # find first
    low, high = 0, len(a) - 1
    first = -1
    while low <= high:
        mid = (low + high) // 2
        if a[mid] >= target:
            if a[mid] == target:
                first = mid
            high = mid - 1
        else:
            low = mid + 1

    if first == -1:
        return None

    # find last
    low, high = first, len(a) - 1
    last = first
    while low <= high:
        mid = (low + high) // 2
        if a[mid] <= target:
            if a[mid] == target:
                last = mid
            low = mid + 1
        else:
            high = mid - 1

    return [first, last]


# Main script
def main():
    filename = "random_numbers.txt"
    print(f"Read input from {filename} ...")
    try:
        data = read_integers(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found in the current directory.")
        return
    except ValueError:
        print("Error: file contains a non-integer line.")
        return

    try:
        target = int(input("Enter a number to search for: ").strip())
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    # Linear search on unsorted data
    start = time.perf_counter()
    lin_indices = linear_search(data, target)
    lin_time = time.perf_counter() - start

    if len(lin_indices) > 0:
        # display as 1-based “positions”
        positions = [i + 1 for i in lin_indices]
        print(f"{target} appears in positions " + ", ".join(str(p) for p in positions))
    else:
        print(f"{target} does not appear in the file (unsorted list).")

    # Selection sort
    print("Sorting the data with selection sort ...")
    sel_data = list(data)  # work on a copy
    start = time.perf_counter()
    selection_sort(sel_data)
    sel_time = time.perf_counter() - start

    # Binary search on sorted data
    print(f"Binary search for {target} in sorted list...")
    start = time.perf_counter()
    idx = binary_search(sel_data, target)
    bin_time = time.perf_counter() - start

    if idx != -1:
        print(f"{target} appears in position {idx + 1}")
        # Extra credit (optional): show full duplicate range
        rng = binary_search_range(sel_data, target)
        if rng is not None and rng[0] != rng[1]:
            first_pos = rng[0] + 1
            last_pos = rng[1] + 1
            print(f"(extra) {target} appears from positions {first_pos} to {last_pos}")
    else:
        print(f"{target} does not appear in the sorted list.")

    # Built-in sort on a fresh copy (per requirement)
    print("Sorting the data using Python's built-in sort function....")
    built_data = list(data)
    start = time.perf_counter()
    built_data.sort()
    built_time = time.perf_counter() - start

    # Timing summary
    print("Running time comparison result:")
    print(f"  linear search:   {lin_time:.6f} seconds")
    print(f"  binary search:   {bin_time:.6f} seconds")
    print(f"  selection sort:  {sel_time:.6f} seconds")
    print(f"  built in sort:   {built_time:.6f} seconds")


if __name__ == "__main__":
    main()
