# This way everything works as expected ever for
# `make -C /path/to/project` or
# `make -f /path/to/project/Makefile`.
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

PREFIX ?= /usr
PREFIX_MAN = ${PREFIX}/share/man
PREFIX_DATA = ${PREFIX}/local/share

TARGET_DIR ?= static
JSON_DIR = $(TARGET_DIR)/times
VIDEO_DIR = $(TARGET_DIR)/video

QUOTES_PT = $(PROJECT_DIR)/quotes/quotes_pt.csv
QUOTES_RU = $(PROJECT_DIR)/quotes/quotes_ru.csv
QUOTES_EN = $(PROJECT_DIR)/quotes/quotes_en.csv
QUOTES = ${QUOTES_RU} ${QUOTES_EN} ${QUOTES_PT}

LITCLOCK_SCRIPT = litclock
LITCLOCK_MAN = litclock.1

all: build

build: build_json build_video

build_json: build_json_ru build_json_en

build_json_ru: ${QUOTES_RU}
	@python build.py --filename $< --language ru --create-json --path ${JSON_DIR}/ru

build_json_en: ${QUOTES_EN}
	@python build.py --filename $< --language en --create-json --path ${JSON_DIR}/en

build_video: build_video_ru build_video_en

build_video_ru: ${QUOTES_RU}
	@python build.py --filename $< --language ru --create-video --path ${VIDEO_DIR}/ru

build_video_en: ${QUOTES_EN}
	@python build.py --filename $< --language en --create-video --path ${VIDEO_DIR}/en

check: check-data check-man check-pep8

check-data: check_data_ru check_data_en

check_data_ru: ${QUOTES_RU}
	@python build.py --filename $< --language ru --dry-run --create-json

check_data_en: ${QUOTES_EN}
	@python build.py --filename $< --language en --dry-run --create-json

check-man: ${LITCLOCK_MAN}
	@mandoc -Tlint $< -W style

check-pep8: build.py
	@autopep8 --diff --exit-code $<

www: build_json
	@python -m http.server 8000 --bind 127.0.0.1 -d ${TARGET_DIR}

install: ${LITCLOCK_SCRIPT} ${LITCLOCK_MAN} ${QUOTES}
	install ${LITCLOCK_SCRIPT} ${PREFIX}/local/bin/${LITCLOCK_SCRIPT}
	install ${LITCLOCK_MAN} ${PREFIX_MAN}/man1/${LITCLOCK_MAN}
	install -d -m 755 ${PREFIX_DATA}/litclock
	install -m 644 ${QUOTES} ${PREFIX_DATA}/litclock

clean:
	@rm -rf ${VIDEO_DIR}/* ${JSON_DIR}/*

.PHONY: build build_json build_json_ru build_json_en
.PHONY: build_video build_video_ru build_video_en
.PHONY: check check-data check_data_ru check_data_en check-man check-pep8
.PHONY: install www clean
