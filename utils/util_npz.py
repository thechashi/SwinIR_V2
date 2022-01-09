import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
def transform(image, resize_size):
        resize_image = cv2.resize(image, resize_size, interpolation=cv2.INTER_CUBIC)
        return np.array(resize_image) 

def get_npz(file_name):
    image = np.load(file_name)
    image = image.f.arr_0
    return image

def view_npz(file_name):
    image = np.load(file_name)
    image = image.f.arr_0
    plt.ion()
    plt.figure()
    plt.imshow(image)
    
def summary_2D_npz(file_name):
    image = np.load(file_name)
    image = image.f.arr_0
    shape, dtype, min_, max_, mean, std = image.shape, image.dtype, image.min(), image.max(), np.mean(image), np.std(image)
    print('Img shape: ',shape)    # shape of an image
    print('Dtype: ', dtype)
    print('Min: ', min_)
    print('Max: ', max_)
    print('Std: ', std)
    print('Mean: ', mean)  
    
def npz_to_png(input_path, output_path):
    image = np.load(input_path)
    image = image.f.arr_0
    cv2.imwrite(output_path, image.reshape((image.shape[0], image.shape[1], 1)))
    
def resize_all(input_path, output_path):
    folders = ['/HR', '/LR_bicubic/X2', '/LR_bicubic/X3', '/LR_bicubic/X4', '/LR_bicubic/X8']
    for folder in folders:
        if not os.path.exists(output_path + folder):
            os.makedirs(output_path + folder)
    print('Processing HR images...')
    # making HR images
    for filename in os.listdir(input_path):
        if '.npz' in filename:
            file_path = os.path.join(input_path, filename)
            img = get_npz(file_path)
            shape = img.shape
            new_shape = ((shape[1]//24)*24, (shape[0]//24)*24)
            img = transform(img, new_shape)
            np.savez(os.path.join(output_path + folders[0], filename), img)
    sizes = [2, 3, 4, 8]
    # making LR 2, 3, 4, 8 images
    print('Processing LR images...')
    for filename in os.listdir(output_path + folders[0]):
        file_path = os.path.join(output_path + folders[0], filename)
        img = get_npz(file_path)
        shape = img.shape
        idx = 1
        for size in sizes:
            new_shape = ((shape[1]//size), (shape[0]//size))
            img = transform(img, new_shape)
            np.savez(os.path.join(output_path + folders[idx], filename.split('.')[0]+'x{}.npz'.format(size)), img)
            idx += 1
            
def get_abs_max(input_path, verbose=False):
    dataset_max = -math.inf
    for filename in os.listdir(input_path):
        if '.npz' in filename:
            file_path = os.path.join(input_path, filename)
            image = get_npz(file_path)
            min_ = image.min()
            max_ = image.max()
            current_max = max(abs(max_), abs(min_))
            if verbose:
                print('Filename: {}, min: {}, max: {}, absolute max: {}'.format(filename, min_, max_, current_max))
            dataset_max = max(dataset_max, current_max)
    if verbose:
        print('Datset max: ', dataset_max)
    return dataset_max
        
        
if __name__ == "__main__":
    pass
    #resize_all('../testsets/slices/raw',  '../testsets/slices')