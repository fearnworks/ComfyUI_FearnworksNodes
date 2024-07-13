import fnmatch
import os
import random
import torch
import numpy as np
from PIL import Image, ImageOps

class FileCountInDirectory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ('STRING', {"forceInput": True, "default": ""}),
                "file_types": ('STRING', {"forceInput": True, "default":"*"})
            }
        }

    RETURN_TYPES = ('INT',)
    FUNCTION = "count_files_in_directory"
    CATEGORY = "Fearnworks/File Operations"

    def count_files_in_directory(self, directory_path, file_types):
        print(f"Counting files in directory: {directory_path} with file types: {file_types}")

        file_types_list = file_types.split(',')
        try:
            file_count = sum(
                len(fnmatch.filter(os.listdir(directory_path), pattern.strip()))
                for pattern in file_types_list
            )
        except Exception as e:
            print(f"Error occurred: {e}")
            return (0,)

        print(f"Number of files matching types {file_types}: {file_count}")
        return (file_count,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

# Keep this function for backwards compatibility if needed
def file_count_in_directory(directory_path, file_types):
    count = 0
    for file_type in file_types.split(','):
        count += len(fnmatch.filter(os.listdir(directory_path), file_type.strip()))
    return (count,)


class LoadRandomImageFromDirectory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ('STRING', {"forceInput": True})
            }
        }

    RETURN_TYPES = ('IMAGE', 'MASK')
    FUNCTION = "load_random_image"
    CATEGORY = "Fearnworks/Image"

    def load_random_image(self, directory_path):
        print(f"Loading random image from directory: {directory_path}")

        try:
            # List all files in the directory
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            
            if not files:
                print(f"No files found in {directory_path}")
                return (None, None)

            # Select a random image file
            random_image = random.choice(files)
            image_path = os.path.join(directory_path, random_image)

            # Open and process the image
            with Image.open(image_path) as i:
                i = ImageOps.exif_transpose(i)
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]

                if 'A' in i.getbands():
                    mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                    mask = 1. - torch.from_numpy(mask)
                else:
                    mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            print(f"Loaded random image: {random_image}")
            return (image, mask.unsqueeze(0))

        except Exception as e:
            print(f"Error loading random image: {e}")
            return (None, None)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")