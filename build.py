#!/usr/bin/env python

import argparse
import csv
import json
import os
import random
import sys

import textwrap
from PIL import Image, ImageDraw, ImageFont
import cv2

DEFAULT_QUOTE = {
    "ru":  [
        {
            "quote_first": "Счастливые часов не наблюдают.",
            "quote_time_case": "",
            "quote_last": "",
            "title": "Горе от ума",
            "author": "А. Грибоедов",
            "sfw": "yes"
        }
    ],
    "en": [
        {
            "quote_first": "Who knows, in happiness, how time is flying?",
            "quote_time_case": "",
            "quote_last": "",
            "title": "Woe From Wit",
            "author": "Alexander Griboyedov",
            "sfw": "yes"
        }
    ]
}


def complement_number(num):
    if num < 10:
        return "0{}".format(num)
    return "{}".format(num)


def iter_daytime():
    for hours in range(24):
        for minutes in range(60):
            yield (complement_number(hours),
                   complement_number(minutes))


def split_string(quote, quote_time_case):
    quote_lc = quote.lower()
    quote_time_case_lc = quote_time_case.lower()
    start_pos = quote_lc.find(quote_time_case_lc)
    if start_pos == -1:
        print("substr '{}' is not found".format(quote_time_case))
        sys.exit(1)
    end_pos = start_pos + len(quote_time_case)
    quote_first = quote[0:start_pos]
    quote_last = quote[end_pos:len(quote)]
    return quote_first, quote_last


def build_record(row):
    record = {}
    record["time"] = row["time"]
    record["quote_time_case"] = row["quote_time_case"]
    record["quote_first"], record["quote_last"] = \
        split_string(row["quote"], row["quote_time_case"])
    record["title"] = row["title"]
    record["author"] = row["author"]
    record["sfw"] = "no"
    if row["sfw"] != "nsfw":
        record["sfw"] = "yes"
    return record


def generate_image(txt_quote, txt_title, txt_author, image_name):
    bg_color = 'black'
    text_color = 'white'
    width = 1024
    height = 512
    font_size = 30

    font_path = "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf"
    font = ImageFont.truetype(
        font_path, size=font_size, index=0, encoding='unic')

    img = Image.new('RGB', (width, height), color=bg_color)
    imgDraw = ImageDraw.Draw(img)

    start_w = 50
    start_h = 100
    interligne = 40
    for line in textwrap.wrap(txt_quote, width=50):
        imgDraw.text((start_w, start_h), line, font=font, fill=text_color)
        start_h = start_h + interligne
    txt = "—  '{}', {}".format(txt_title, txt_author)
    imgDraw.text((start_w, start_h + 10), txt, font=font, fill=text_color)
    img.save(image_name)


def random_default_quote(lang):
    quotes_list = DEFAULT_QUOTE.get(lang)
    return random.choice(quotes_list)


def complement_placeholders(times, lang):
    times_with_placeholders = times.copy()
    for hours, minutes in iter_daytime():
        time_str = "{}:{}".format(hours, minutes)
        quotes_list = times_with_placeholders.get(time_str)
        if not quotes_list:
            default_quote = random_default_quote(lang)
            placeholder = default_quote.copy()
            placeholder["time"] = time_str
            placeholder["quote_first"] = "{}: {}".format(
                time_str, placeholder["quote_first"])
            times_with_placeholders[time_str] = [placeholder]

    return times_with_placeholders


def write_files(quotes_dict, path, image=False):
    for time_str, quotes_list in quotes_dict.items():
        json_obj = json.dumps(quotes_list, indent=4)
        time_wo_colon = time_str.replace(":", "_", 1)
        if not image:
            file_name = os.path.join(path, "{}.json".format(time_wo_colon))
            json_obj = json.dumps(quotes_list, indent=4)
            with open(file_name, "w") as outfile:
                outfile.write(json_obj)
        else:
            file_name = os.path.join(path, "{}.png".format(time_wo_colon))
            quote = random.choice(quotes_list)
            quote_str = quote["quote_first"] + \
                quote["quote_time_case"] + \
                quote["quote_last"]
            generate_image(quote_str, quote["title"],
                           quote["author"], file_name)


"""
The dictionary format is the following:

[
  "00:09": [
    ...
  ],
  "00:10": [
  {
    "time": "00:10",
    "quote_first": "",
    "quote_time_case": "",
    "quote_last": "",
    "title": "",
    "author": "",
    "sfw": ""
  },
  {
    "time": "00:10",
    "quote_first": "",
    "quote_time_case": "",
    "quote_last": "",
    "title": "",
    "author": "",
    "sfw": ""
  }]
  "00:11": [
    ...
  ],
]
"""


def build_dict(quote_filename, verbose=False):
    times = {}
    csv_fields = ["time", "quote_time_case", "quote", "title", "author", "sfw"]
    with open(quote_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=csv_fields,
                                    delimiter="|", quoting=csv.QUOTE_NONE)
        for row in list(csv_reader):
            # Build a dictionary.
            time = row["time"]
            if times.get(time) is None:
                times[time] = []
            record = build_record(row)
            if verbose:
                print(record)
            times[time].append(record)
    return times


def parse_args():
    parser = argparse.ArgumentParser(prog="build_data")
    parser.add_argument("--filename",
                        type=str)
    parser.add_argument("-l", "--language",
                        choices=["ru", "en"],
                        required=True,
                        type=str)
    parser.add_argument("-p", "--path",
                        type=str)
    parser.add_argument("-d", "--dry-run",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create-video', action="store_true")
    group.add_argument('--create-json', action="store_true")
    args = parser.parse_args()
    return args


def build_video(image_dir, video_name):
    fps = 1 / 60  # 1 minute
    images = [img for img in sorted(
        os.listdir(image_dir)) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_dir, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    result_file = os.path.join(image_dir, video_name)
    video = cv2.VideoWriter(filename=result_file, fourcc=fourcc,
                            fps=fps, frameSize=(width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_dir, image)))

    cv2.destroyAllWindows()
    video.release()
    print("File {}".format(result_file))


def main():
    inputs = parse_args()
    filename = inputs.filename
    if not filename and inputs.language:
        filename = "quotes/quotes_{}.csv".format(inputs.language)

    if not os.path.isfile(filename):
        print("File {} is not found".format(filename))
        sys.exit(1)

    if not inputs.dry_run and not os.path.isdir(inputs.path):
        os.makedirs(inputs.path)

    times = build_dict(filename, inputs.verbose)
    times_with_placeholders = complement_placeholders(times, inputs.language)
    # Write JSON files.
    if not inputs.dry_run and inputs.create_json:
        write_files(times_with_placeholders, inputs.path)

    # Write a video file.
    if not inputs.dry_run and inputs.create_video:
        write_files(times_with_placeholders, inputs.path, image=True)
        build_video(inputs.path, "litclock.avi")

    perc_covered = round(len(times)/(60 * 24) * 100)
    print("File with quotes: {}".format(filename))
    msg_fmt = "Number of quotes with unique time: {} ({}%)"
    print(msg_fmt.format(len(times), perc_covered))


if __name__ == '__main__':
    main()
