import argparse
import csv
import json
import os
import sys


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


def write_files(times, path):
    for time in times.keys():
        time_wo_colon = time.replace(":", "_", 1)
        file_name = "{}.json".format(time_wo_colon)
        if path:
            file_name = os.path.join(path, file_name)
        print(file_name)
        with open(file_name, "w") as outfile:
            json_obj = json.dumps(times[time], indent=4)
            outfile.write(json_obj)


DEFAULT_ANNNOTATED_DATA = "quotes/quotes_ru.csv"
DEFAULT_JSON_PATH = "static/times"

parser = argparse.ArgumentParser(prog="csv_to_json")
parser.add_argument("--filename",
                    default=DEFAULT_ANNNOTATED_DATA,
                    type=str)
parser.add_argument("-p", "--path",
                    default=DEFAULT_JSON_PATH,
                    type=str)
parser.add_argument("-d", "--dry-run",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    action="store_true")
args = parser.parse_args()

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


times = build_dict(args.filename)
# Write files.
if not args.dry_run:
    write_files(times, args.path)

perc_covered = round(len(times)/(60 * 24) * 100)
print("File with quotes: {}".format(args.filename))
msg_fmt = "Number of quotes with unique time: {} ({}%)"
print(msg_fmt.format(len(times), perc_covered))
