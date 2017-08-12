#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

#iterate through a set, each item will be a new line in the file
def set_to_file(links, file_name):
   with open(file_name, "w") as f:
    for link in sorted(links):
        f.write(link + "\n")


def file_to_set(file_name):
    results = set()
    with open(file_name, "rt") as f:
        for line in f:
            results.add(line.replace("\n", ""))
    return results

def list_to_set(list):
    results = set(list)
    return results


def set_to_list(set):
    results = list(set)
    return results