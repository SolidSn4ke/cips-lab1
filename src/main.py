from PIL import Image, ImageFilter
from datetime import datetime
from pathlib import Path
import sys

OUT_DIR = "./target"


def load_img(path: str):
    with Image.open(path) as img:
        return img.copy()


def med_filter_native(img: Image.Image, kernel_size: int) -> Image.Image:
    source = img.load()
    if source is None:
        raise RuntimeError("Не удалось получить доступ к пикселям изображения")

    result = Image.new(img.mode, img.size)
    destination = result.load()
    if destination is None:
        raise RuntimeError("Не удалось создать изображение результата")

    radius = kernel_size // 2
    for y in range(img.height):
        for x in range(img.width):
            window = [
                source[
                    min(max(x + dx, 0), img.width - 1),
                    min(max(y + dy, 0), img.height - 1),
                ]
                for dy in range(-radius, radius + 1)
                for dx in range(-radius, radius + 1)
            ]

            first_pixel = window[0]
            if isinstance(first_pixel, tuple):
                destination[x, y] = tuple(
                    sorted(pixel[channel] for pixel in window)[len(window) // 2]  # type: ignore
                    for channel in range(len(first_pixel))
                )
            else:
                destination[x, y] = sorted(window)[len(window) // 2]

    return result


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
        med_filter_native(img.copy(), kernel_size),
        Path(OUT_DIR) / f"img-native-{timestamp}{extension}",
    )
    save_img(
        med_filter_lib(img.copy(), kernel_size),
        Path(OUT_DIR) / f"img-lib-{timestamp}{extension}",
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Использование: python main.py <путь_к_изображению> <размер_ядра>"
        )

    try:
        kernel_size = int(sys.argv[2])
    except ValueError:
        raise SystemExit("Размер ядра должен быть целым нечётным числом не меньше 3")

    if kernel_size < 3 or kernel_size % 2 == 0:
        raise SystemExit("Размер ядра должен быть нечётным числом не меньше 3")

    main(sys.argv[1], kernel_size)
