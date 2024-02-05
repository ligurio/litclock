import argparse
import csv
import json
import os
import random
import sys

DEFAULT_QUOTE_RU = {
    "quote_first": "Счастливые часов не наблюдают.",
    "quote_time_case": "",
    "quote_last": "",
    "title": "Горе от ума",
    "author": "А. Грибоедов",
    "sfw": "yes"
}

DEFAULT_QUOTE_EN = {
    "quote_first": "Who knows, in happiness, how time is flying?",
    "quote_time_case": "",
    "quote_last": "",
    "title": "Woe From Wit",
    "author": "Alexander Griboyedov",
    "sfw": "yes"
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


def complement_placeholders(times):
    times_with_placeholders = times.copy()
    for hours, minutes in iter_daytime():
        time_str = "{}:{}".format(hours, minutes)
        quotes_list = times_with_placeholders.get(time_str)
        if not quotes_list:
            placeholder = DEFAULT_QUOTE_RU.copy()
            placeholder["time"] = time_str
            placeholder["quote_first"] = "{}: {}".format(
                time_str, placeholder["quote_first"])
            times_with_placeholders[time_str] = [placeholder]

    return times_with_placeholders


def write_files(quotes_dict, path):
    for time_str, quotes_list in quotes_dict.items():
        json_obj = json.dumps(quotes_list, indent=4)
        time_wo_colon = time_str.replace(":", "_", 1)
        file_name = os.path.join(path, "{}.json".format(time_wo_colon))
        with open(file_name, "w") as outfile:
            outfile.write(json_obj)


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
                        type=str,
                        required=True)
    parser.add_argument("-p", "--path",
                        type=str)
    parser.add_argument("-d", "--dry-run",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    args = parser.parse_args()
    return args


def main():
    inputs = parse_args()
    times = build_dict(inputs.filename, inputs.verbose)
    times_with_placeholders = complement_placeholders(times)
    # Write files.
    if not inputs.dry_run:
        write_files(times_with_placeholders, inputs.path)

    perc_covered = round(len(times)/(60 * 24) * 100)
    print("File with quotes: {}".format(inputs.filename))
    msg_fmt = "Number of quotes with unique time: {} ({}%)"
    print(msg_fmt.format(len(times), perc_covered))


if __name__ == '__main__':
    main()
