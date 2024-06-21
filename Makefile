# This way everything works as expected ever for
# `make -C /path/to/project` or
# `make -f /path/to/project/Makefile`.
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

PREFIX ?= /usr
PREFIX_MAN = ${PREFIX}/share/man
PREFIX_DATA = ${PREFIX}/local/share

QUOTES ?= $(PROJECT_DIR)/quotes/quotes_en.csv
TARGET_DIR ?= static/times/
JSON_DATA = ${TARGET_DIR}/*.json

LITCLOCK_SCRIPT = litclock
LITCLOCK_MAN = litclock.1

all: build

build: ${QUOTES}
	@python build.py --filename $< --path ${TARGET_DIR}

check: check-data check-man check-pep8

check-data:
	@python build.py --filename $(PROJECT_DIR)/quotes/quotes_ru.csv --dry-run --create-json --path ${TARGET_DIR}/times
	@python build.py --filename $(PROJECT_DIR)/quotes/quotes_en.csv --dry-run --create-json --path ${TARGET_DIR}/times

check-man: ${LITCLOCK_MAN}
	@mandoc -Tlint $< -W style

check-pep8: build.py
	@autopep8 --diff $<

www: build
	@python -m http.server 8000 --bind 127.0.0.1 -d static

install: ${LITCLOCK_SCRIPT} ${LITCLOCK_MAN} ${QUOTES}
	install ${LITCLOCK_SCRIPT} ${PREFIX}/local/bin/${LITCLOCK_SCRIPT}
	install ${LITCLOCK_MAN} ${PREFIX_MAN}/man1/${LITCLOCK_MAN}
	install -d -m 755 ${PREFIX_DATA}/litclock
	install -m 644 ${QUOTES} ${PREFIX_DATA}/litclock

clean:
	@rm -f ${JSON_DATA}

.PHONY: build check check-data check-man check-pep8 install www clean
