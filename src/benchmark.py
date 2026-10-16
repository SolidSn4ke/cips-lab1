import main
import time
import sys

IMG_SRC = "./res/Beauclair (Maciej Łaszkiewicz).png"


def measure(func, iters, kernel_size) -> float:
    img = main.load_img(IMG_SRC)
    start_time = time.perf_counter()
    for _ in range(iters):
        func(img, kernel_size)
    end_time = time.perf_counter()
    return end_time - start_time


def run_benchmark(iters: int, kernel_size: int):
    for name, func in {
        "native": main.med_filter_native,
        "lib": main.med_filter_lib,
    }.items():
        print(f"{name}:")
        exec_time = measure(func, iters, kernel_size)
        print(f"exec_time: {exec_time:.6f} seconds\n")


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        raise SystemExit(
            "Использование: python benchmark.py <кол-во итераций> <размер_ядра>"
        )

    try:
        iters = int(sys.argv[1])
    except ValueError:
        raise SystemExit("Кол-во итераций должно быть натуральным числом")

    if iters < 1:
        raise SystemExit("Кол-во итераций должно быть натуральным числом")

    try:
        kernel_size = int(sys.argv[2])
    except ValueError:
        raise SystemExit("Размер ядра должен быть целым нечётным числом не меньше 3")

    if kernel_size < 3 or kernel_size % 2 == 0:
        raise SystemExit("Размер ядра должен быть нечётным числом не меньше 3")

    run_benchmark(iters, kernel_size)
