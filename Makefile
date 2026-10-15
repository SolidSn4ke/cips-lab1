PYTHON ?= python3
IMAGE ?= ./res/Beauclair (Maciej Łaszkiewicz).png
KERNEL_SIZE ?= 3

.PHONY: run

run:
	$(PYTHON) ./src/main.py "$(IMAGE)" "$(KERNEL_SIZE)"
