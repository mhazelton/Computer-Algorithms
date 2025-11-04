# Note: You need to run the following command to install necesary libraries:
# pip install pillow numpy matplotlib

# Max Hazelton
# CISC4080 Lab 3
# MergeSort, QuickSort, QuickSelect + image I/O
#   New photos will be saved in the same folder
#   fordham.png and gray_image.png need to be in this folder


from PIL import Image, ImageDraw
import numpy as np
import random

# -------------------------------
# MergeSort (returns a NEW list)
# -------------------------------
def MergeSort(arr, ascend=True):
    # Accept numpy arrays or lists
    a = list(arr)

    def merge(left, right, ascend):
        out = []
        i = j = 0
        if ascend:
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    out.append(left[i]); i += 1
                else:
                    out.append(right[j]); j += 1
        else:
            while i < len(left) and j < len(right):
                if left[i] >= right[j]:
                    out.append(left[i]); i += 1
                else:
                    out.append(right[j]); j += 1
        # append remainder
        if i < len(left):  out.extend(left[i:])
        if j < len(right): out.extend(right[j:])
        return out

    def mergesort(a, ascend):
        n = len(a)
        if n <= 1:
            return a[:]
        mid = n // 2
        L = mergesort(a[:mid], ascend)
        R = mergesort(a[mid:], ascend)
        return merge(L, R, ascend)

    return mergesort(a, ascend)


# -----------------------------------------
# QuickSort (in-place) with partition helper
# -----------------------------------------
def partition(arr, l, r, ascend=True):
    # Random pivot; swap it to end
    p_idx = random.randint(l, r)
    arr[p_idx], arr[r] = arr[r], arr[p_idx]
    pivot = arr[r]

    i = l  # place for next element that satisfies comparison

    if ascend:
        for j in range(l, r):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
    else:
        for j in range(l, r):
            if arr[j] >= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

    # put pivot in its final place
    arr[i], arr[r] = arr[r], arr[i]
    return i  # final pivot index


def QuickSort(arr, l, r, ascend=True):
    # In-place QuickSort
    if l >= r:
        return
    pi = partition(arr, l, r, ascend=ascend)
    QuickSort(arr, l, pi - 1, ascend=ascend)
    QuickSort(arr, pi + 1, r, ascend=ascend)


# ----------------------------
# QuickSelect (k-th smallest)
# ----------------------------
def QuickSelect(arr, k, ascend=True):
    a = list(arr)  # work on a copy

    l, r = 0, len(a) - 1
    while l <= r:
        pi = partition(a, l, r, ascend=ascend)
        if pi == k:
            return a[pi]
        elif pi < k:
            l = pi + 1
        else:
            r = pi - 1

    # Shouldn't reach here if k is valid
    raise IndexError("k out of bounds in QuickSelect")


# Part 1: Sort grayscale image with MergeSort and QuickSort

# --- Load grayscale image ---
img_path = "gray_image.png"     # ensure this file is present next to the script/notebook
img = Image.open(img_path).convert("L")   # 'L' = grayscale
pixels = np.array(img)
h, w = pixels.shape
flat_pixels = pixels.flatten()  # 1-D array of intensities

print(f"Grayscale image loaded: {h}x{w}, total pixels = {len(flat_pixels)}")

# --- MergeSort (ascending) ---
sorted_pixels_ms_asc = MergeSort(flat_pixels, ascend=True)
sorted_img = np.reshape(sorted_pixels_ms_asc, (h, w)).astype(np.uint8)
Image.fromarray(sorted_img, mode="L").save("MergeSort_ascending_sorted_gray.png")

# --- MergeSort (descending) via reverse ---
sorted_pixels_ms_desc = sorted_pixels_ms_asc[::-1]
sorted_img = np.reshape(sorted_pixels_ms_desc, (h, w)).astype(np.uint8)
Image.fromarray(sorted_img, mode="L").save("MergeSort_descending_sorted_gray.png")

print("Saved: MergeSort_ascending_sorted_gray.png, MergeSort_descending_sorted_gray.png")

# --- QuickSort (ascending) ---
pixels_qs = flat_pixels.copy().tolist()
QuickSort(pixels_qs, l=0, r=len(pixels_qs)-1, ascend=True)
sorted_img = np.reshape(pixels_qs, (h, w)).astype(np.uint8)
Image.fromarray(sorted_img, mode="L").save("QuickSort_ascending_sorted_gray.png")

# --- QuickSort (descending) ---
pixels_qs = flat_pixels.copy().tolist()
QuickSort(pixels_qs, l=0, r=len(pixels_qs)-1, ascend=False)
sorted_img = np.reshape(pixels_qs, (h, w)).astype(np.uint8)
Image.fromarray(sorted_img, mode="L").save("QuickSort_descending_sorted_gray.png")

print("Saved: QuickSort_ascending_sorted_gray.png, QuickSort_descending_sorted_gray.png")


# Part 2: QuickSelect brightest pixel in color image

# --- Load color image ---
campus_path = "fordham.png"     # ensure file present
img_c = Image.open(campus_path).convert("RGB")
pix_c = np.array(img_c)
hc, wc, _ = pix_c.shape

# Perceived brightness Y = 0.299R + 0.587G + 0.114B
R, G, B = pix_c[..., 0], pix_c[..., 1], pix_c[..., 2]
Y = 0.299 * R + 0.587 * G + 0.114 * B
flat_Y = Y.flatten()

# Use QuickSelect to get maximum brightness (k = n-1 for ascending order)
k = len(flat_Y) - 1
brightest_value = QuickSelect(flat_Y, k, ascend=True)

# Get a stable coordinate for that brightness.
# Floating-point equality can be tricky; use isclose to find matches, then pick the first.
mask = np.isclose(Y, brightest_value, rtol=1e-05, atol=1e-08)
flat_idx = np.argmax(mask.ravel())  # first True position
y, x = divmod(flat_idx, wc)

# Draw a red circle and label
draw = ImageDraw.Draw(img_c)
r = 8
draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=3)
draw.text((x + 10, y - 10), f"({x},{y})", fill="red")

# Save with the filename requested in the lab
img_c.save("fordham_01_marked.png")
print("Saved: fordham_01_marked.png")