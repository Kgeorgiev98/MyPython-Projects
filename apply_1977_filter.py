from PIL import Image
import pilgram
from tkinter import Tk, filedialog

def apply_filter(image):
    filtered_image = pilgram._1977(image)
    return filtered_image

def open_image(file_path):
    image = Image.open(file_path)
    image.show()

def save_image(image, save_path):
    image.save(save_path)

def process_image(filter_name):
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    if not file_path:
        print("No image selected.")
        return

    image = Image.open(file_path)
    filtered_image = apply_filter(image)

    save_path = filedialog.asksaveasfilename(defaultextension='.jpg')
    if not save_path:
        print("No save location specified.")
        return

    save_image(filtered_image, save_path)
    open_image(save_path)

if __name__ == '__main__':
    filter_name = '_1977'

    process_image(filter_name)
