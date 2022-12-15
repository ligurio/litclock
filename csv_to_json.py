import argparse
import csv
import json
import os
import sys

"""
[
  {
    "time": "00:10",
    "quote_first": "It was at ",
    "quote_time_case": "ten minutes past midnight",
    "quote_last": ". Three police cars, Alsations and a black maria arrive at the farmhouse. The farmer clad only in a jock-strap, refused them entry.",
    "title": "The Queue",
    "author": "Jonathan Barrow",
    "sfw": "yes"
  }
]
"""

def split_string(quote, quote_time_case):
    start_pos = quote.find(quote_time_case)
    if start_pos == -1:
        print("substr {} is not found".format(quote_time_case))
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
            json_obj = json.dumps(times[time], indent = 4)
            outfile.write(json_obj)

DEFAULT_ANNNOTATED_DATA = "litclock_annotated.csv"
DEFAULT_JSON_PATH = "static/times"

csv_fields = ["time", "quote_time_case", "quote", "title", "author", "sfw"]
times = {}

parser = argparse.ArgumentParser(prog = "csv_to_json")
parser.add_argument("--filename",
					default = DEFAULT_ANNNOTATED_DATA,
					type=str)
parser.add_argument("-p", "--path",
					default=DEFAULT_JSON_PATH,
					type=str)
parser.add_argument("-d", "--dry-run",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    action="store_true")
args = parser.parse_args()

with open(args.filename) as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames=csv_fields,
                                delimiter="|", quoting=csv.QUOTE_NONE)
    for row in list(csv_reader):
        # Build a dictionary.
        time = row["time"]
        if times.get(time) == None:
            times[time] = []
        record = build_record(row)
        if args.verbose:
            print(record)
        times[time].append(record)

# Write files.
if not args.dry_run:
	write_files(times, args.path)
