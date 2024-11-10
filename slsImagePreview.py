
'''
2021IMT015
Apoorv Jain
'''

import rawpy
import numpy as np
import matplotlib.pyplot as plt
import time
import psutil
from PIL import Image, ImageFilter
from skimage.metrics import peak_signal_noise_ratio as psnr

file_path = "slsForImageLoading/RAW_SONY_ILCE-7RM2 (1).ARW"


'''for default high quality display:   convert the arw to rgb by default domsaic method'''

'''
for low quality,low size image preview follwing transformations:
1. arw to rgb : using low quality Linear domsaic method
2. Downscale Resolution
3. bit depth reduction
4. light sharpening
'''

def load_and_process_image(file_path, preview=False):
    with rawpy.imread(file_path) as raw:
        rgb_image = raw.postprocess(demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR) if preview else raw.postprocess()

        if preview:
            img = Image.fromarray(rgb_image)
            img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
            img = img.convert("RGB")
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=50, threshold=2))
            rgb_image = np.array(img)
            
    return rgb_image

def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)  

def calculate_psnr(image1, image2):
    img2_resized = Image.fromarray(image2).resize((image1.shape[1], image1.shape[0]), Image.LANCZOS)
    img2_resized = np.array(img2_resized)
    return psnr(image1, img2_resized)

choice = input("Choose display option: 'full', 'preview', or 'both': ").strip().lower()

if choice in ('preview', 'both'):
    start_time = time.time()
    initial_memory = get_memory_usage()
    rgb_image_preview = load_and_process_image(file_path, preview=True)
    preview_load_time = time.time() - start_time
    preview_memory_used = get_memory_usage() - initial_memory

if choice in ('full', 'both'):
    start_time = time.time()
    initial_memory2 = get_memory_usage()
    rgb_image_full = load_and_process_image(file_path, preview=False)
    full_load_time = time.time() - start_time
    full_memory_used = get_memory_usage() - initial_memory2

if choice == 'both':
    image_quality_psnr = calculate_psnr(rgb_image_preview, rgb_image_full)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].imshow(rgb_image_preview)
    axs[0].set_title("Preview Image (Optimized)")
    axs[0].axis("off")
    axs[1].imshow(rgb_image_full)
    axs[1].set_title("Full-Quality Image (Without Optimization)")
    axs[1].axis("off")
    plt.show()
    print(f"Image Quality (PSNR between Preview and Full Image): {image_quality_psnr:.2f} dB")
elif choice == 'preview':
    plt.imshow(rgb_image_preview)
    plt.title("Preview Image (Optimized)")
    plt.axis("off")
    plt.show()
elif choice == 'full':
    plt.imshow(rgb_image_full)
    plt.title("Full-Quality Image (Without Optimization)")
    plt.axis("off")
    plt.show()

if choice in ('preview', 'both'):
    print(f"Preview Load Time (Optimized): {preview_load_time:.2f} seconds")
    print(f"Memory Used for Preview (Optimized): {preview_memory_used:.2f} MB")
if choice in ('full', 'both'):
    print(f"Full Load Time (Without Optimization): {full_load_time:.2f} seconds")
    print(f"Memory Used for Full Image (Without Optimization): {full_memory_used:.2f} MB")
