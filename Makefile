# This way everything works as expected ever for
# `make -C /path/to/project` or
# `make -f /path/to/project/Makefile`.
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

ANNOTATED := $(PROJECT_DIR)/litclock_annotated.csv
TARGET_DIR ?= static/times/
JSON_DATA = ${TARGET_DIR}/*.json

all: gen

gen: ${ANNOTATED}
	@python csv_to_json.py --filename ${ANNOTATED} --path ${TARGET_DIR}

check: ${ANNOTATED}
	@python csv_to_json.py --filename ${ANNOTATED} --path ${TARGET_DIR} --dry-run --verbose

www:
	@python -m http.server 8000 --bind 127.0.0.1

clean:
	@rm -f ${JSON_DATA}

.PHONY: gen check www clean
