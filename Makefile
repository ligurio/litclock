# This way everything works as expected ever for
# `make -C /path/to/project` or
# `make -f /path/to/project/Makefile`.
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

PREFIX ?= /usr
PREFIX_MAN = ${PREFIX}/share/man

ANNOTATED := $(PROJECT_DIR)/quotes/quotes_ru.csv
TARGET_DIR ?= static/times/
JSON_DATA = ${TARGET_DIR}/*.json

LITCLOCK_SCRIPT = litclock
LITCLOCK_MAN = litclock.1

all: build

build: ${ANNOTATED}
	@python build.py --filename $< --path ${TARGET_DIR}

check: check-data check-man

check-data: ${ANNOTATED}
	@python build.py --filename $< --path ${TARGET_DIR} --dry-run --verbose

check-man: ${LITCLOCK_MAN}
	@mandoc -Tlint $< -W style

www:
	@python -m http.server 8000 --bind 127.0.0.1

install: ${LITCLOCK_SCRIPT} ${LITCLOCK_MAN}
	@install ${LITCLOCK_SCRIPT} ${PREFIX}/local/bin/${LITCLOCK_SCRIPT}
	@install ${LITCLOCK_MAN} ${PREFIX_MAN}/man1/${LITCLOCK_MAN}

clean:
	@rm -f ${JSON_DATA}

.PHONY: build check check-data check-man install www clean
