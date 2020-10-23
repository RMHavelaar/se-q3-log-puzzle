#!/usr/bin/env python2
"""
Log Puzzle exercise
Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
Given an Apache logfile, find the puzzle URLs and download the images.
Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
'Author: ROBERT HAVELAAR'
import os
import re
import sys
import urllib.request
import argparse
import requests

puzzle_pattern = re.compile(r'[\S]*puzzle\/[\S]*')


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # +++your code here+++
    filename_base = filename.split("_")[1]
    with open(filename) as f:
        urls = f.read()
    puzzle_pieces = re.findall(puzzle_pattern, urls)
    puzzle_pieces = sorted(list(set(puzzle_pieces)),
                           key=lambda url: url[url.rfind('-') + 1:])
    puzzle_urls = [f'http://{filename_base}{piece}' for piece in puzzle_pieces]
    return puzzle_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    print(img_urls)
    try:
        os.makedirs(dest_dir)
    except FileExistsError:
        pass
    os.chdir(dest_dir)
    img_str = "<html><body>"
    for i, url in enumerate(img_urls):
        src = f'img{i}'
        img_str += f'<img src="./{src}">'
        print(f'Downloading img{i} from url: {url}')
        with open(src, 'wb') as f:
            f.write(requests.get(url).content)
    img_str += "</body></html>"
    with open('index.html', 'w') as f:
        f.write(img_str)
    print('downloading complete')

    pass


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])