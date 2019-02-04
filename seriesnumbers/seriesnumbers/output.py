import os
import json
import csv


def generate_output(full_path, result):
    f = open(full_path, "w+")
    path, this_format = os.path.splitext(full_path)
    if this_format == ".txt":
        generate_txt(result, path)
    elif this_format == ".json":
        generate_json(result, path)
    elif this_format == ".cvs":
        generate_cvs(result, path)


def generate_json(seq, path):
    data = {}
    data['numbers'] = []
    for x in range(len(seq)):
        data['numbers'].append({str(x): str(seq[x])})
    with open(path + ".json", "w+") as outfile:
        json.dump(data, outfile)


def generate_txt(seq, path):
    outfile = open(path + ".txt", "w+")
    for x in range(len(seq)):
        outfile.write(str(x) + ": " + str(seq[x]) + "\n")
    outfile.close()


def generate_csv(seq, path):
    data = []
    for x in range(len(seq)):
        data.append([str(x), str(seq[x])])
    outfile = open(path + ".csv", "w+")
    with outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)
