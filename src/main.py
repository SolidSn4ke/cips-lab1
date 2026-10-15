from PIL import Image, ImageFilter
from datetime import datetime
from pathlib import Path
import sys

OUT_DIR = "./target"


def load_img(path: str):
    with Image.open(path) as img:
        img.load()
        return img.copy()


def med_filter_native(img, kernel_size: int) -> Image.Image:
    # work
    return img


def med_filter_lib(img, kernel_size: int) -> Image.Image:
    return img.filter(ImageFilter.MedianFilter(size=kernel_size))


def save_img(img, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main(img_path: str, kernel_size: int):
    img = load_img(img_path)
    timestamp = datetime.now().strftime("%H-%M-%S-%f")
    extension = Path(img_path).suffix or ".png"
    save_img(
        med_filter_native(img, kernel_size),
        Path(OUT_DIR) / f"img-native-{timestamp}{extension}",
    )
    save_img(
        med_filter_lib(img, kernel_size),
        Path(OUT_DIR) / f"img-lib-{timestamp}{extension}",
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Использование: python main.py <путь_к_изображению> <размер_ядра>")

    try:
        kernel_size = int(sys.argv[2])
    except ValueError:
        raise SystemExit("Размер ядра должен быть целым нечётным числом не меньше 3")

    if kernel_size < 3 or kernel_size % 2 == 0:
        raise SystemExit("Размер ядра должен быть нечётным числом не меньше 3")

    main(sys.argv[1], kernel_size)
