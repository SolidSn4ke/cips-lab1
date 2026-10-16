PYTHON ?= python3
IMAGE ?= ./res/Beauclair (Maciej Łaszkiewicz).png
KERNEL_SIZE ?= 3
ITERS ?= 10

.PHONY: run

run:
	$(PYTHON) ./src/main.py "$(IMAGE)" "$(KERNEL_SIZE)"

run_benchmark:
	$(PYTHON) ./src/benchmark.py "$(ITERS)" "$(KERNEL_SIZE)"
