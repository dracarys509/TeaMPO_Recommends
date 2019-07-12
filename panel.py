#!/usr/bin/env python

import sys
import subprocess


if len(sys.argv) < 2:
    print("please call with file to edit")
    sys.exit(1)
filename = sys.argv[1]

def from_string(s):
    items = []
    keys = None
    for line in s.split('\n'):
        if keys is None:
            keys = [ k.strip() for k in line.split('|') ]
        elif "|" in line:
            items.append({key: value.strip() for (key, value) in zip(keys, line.split('|'))})
    return (keys, items)

def center_pad(s, l):
    total_pad_ammount = l - len(s)
    left_pad_ammount = total_pad_ammount / 2
    right_pad_ammount = (total_pad_ammount + 1) / 2
    return (" "*left_pad_ammount) + s + (" "*right_pad_ammount)
def right_pad(s, l):
    return s+" "*((l - len(s)))
def to_string(keys, items, with_nums):
    if with_nums:
        keys = ["Number"] + keys
        for i in range(len(items)):
            items[i] = items[i].copy()
            items[i]["Number"] = str(i)
    key_to_max_len = {}
    for key in keys:
        key_to_max_len[key] = max(len(key), max( len(item[key]) for item in items ) )
    joiner = "   |   "
    output = joiner.join( center_pad(key, key_to_max_len[key]) for key in keys)
    output += "\n" + ("=" * (len(output) + 2))
    for item in items:
        output += "\n" + (joiner.join(right_pad(item[key], key_to_max_len[key]) for key in keys)).strip()
    output += "\n\n\n(s) indicates a song"
    return output

filestring = None
with open(filename) as f:
    filestring = f.read()

(keys, data) = from_string(filestring)

while True:
    print(to_string(keys, data, True))
    i = raw_input("What would you like to do? (q quit, a add Album (or song), l[number] to like, p[number] to play, w to write_out): ")
    n = None
    if len(i) > 1:
        n = int(i[1:])
        i = i[0]
    if i == "q":
        break;
    elif i == "a":
        item = {}
        for key in keys:
            item[key] = raw_input("value for " + key + ": ")
        data.append(item)
    elif i == "l":
        if n is None:
            n = int(raw_input("number to like: ").strip())
        current_count = int(data[n]["Likes"])
        data[n]["Likes"] = str(current_count + 1)
    elif i == "p":
        if n is None:
            n = int(raw_input("number to play: ").strip())
        args = ["tizonia"]
        if "(s)" in data[n]["Album"]:
            args.append("--gmusic-unlimited-tracks")
            args.append("".join(data[n]["Album"].split("(s)")) + " (" + data[n]["Artist"] + ")")
        else:
            args.append("--gmusic-unlimited-album")
            args.append(data[n]["Album"] + " (" + data[n]["Artist"] + ")")
        print("running " + " ".join(args) + "")
        subprocess.call(args)
    elif i == "w":
        new_name = raw_input("filename to write (leave empty for previous filename " + filename + "): ")
        if new_name.strip() == "":
            new_name = filename
        with open(new_name, "w") as f:
            f.write(to_string(keys, data, False))
        break;

