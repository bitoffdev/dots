#!/usr/bin/env python3
import argparse
import math
import os
import pystache
import re
import subprocess
import sys
from urllib.request import urlopen
import yaml

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_scheme_list():
    scheme_dir = os.path.join(BASE_DIR, "schemes")
    for parent, _, names in os.walk(scheme_dir):
        for name in filter(lambda x: x[-5:] == ".yaml", names):
            yield name[:-5]


def get_scheme(name):
    scheme_dir = os.path.join(BASE_DIR, "schemes")
    path = None
    for parent, _, names in os.walk(scheme_dir):
        if name + ".yaml" in names:
            path = os.path.join(parent, name + ".yaml")
    if path:
        with open(path) as fh:
            return Base16Dict(yaml.load(fh))


class Base16Dict(dict):
    """
    Implements github.com/chriskempson/base16/blob/master/builder.md#template-variables

    Subclass of dict, where each entry is a 6-character hex encoding
    """

    @staticmethod
    def _hex_to_rgb(hex):
        # type: (str) -> int
        """Convert a single color channel from hex to integer in the range
        [0,255]"""
        return int(hex, base=16)

    def __getitem__(self, key):
        m = re.match("(base0[0-9A-F])(?:-(hex|rgb|dec))(?:-([rgb]))?", key)
        for _ in range(1 if m else 0):
            base, encoding, channel = m.groups()
            if not base or not encoding:
                break

            # exit early if we no channel was specified
            if encoding == "hex" and not channel:
                return dict.__getitem__(self, base)

            # get the correct channel
            index = "rgb".index(channel) * 2
            channel_hex = dict.__getitem__(self, base)[index : index + 2]
            if encoding == "rgb":
                return self._hex_to_rgb(channel_hex)
            elif encoding == "hex":
                return channel_hex
            raise ValueError

        # no match found
        key = "scheme" if key == "scheme-name" else key
        key = "author" if key == "scheme-author" else key
        return dict.__getitem__(self, key)

    def __contains__(self, value):
        return dict.__contains__(self, value) or isinstance(
            self.__getitem__(value), str
        )


def download_schemes(args):
    LIST_URL = "https://raw.githubusercontent.com/chriskempson/base16-schemes-source/master/list.yaml"
    with urlopen(LIST_URL) as fh:
        scheme_list = yaml.load(fh)
        for name in scheme_list:
            url = scheme_list[name]
            cmd = ["git", "clone", url, os.path.join(BASE_DIR, "schemes", name)]
            print(" ".join(cmd))
            subprocess.run(cmd)


def list_schemes(args):
    schemes = sorted(list(get_scheme_list()))
    if args.json:
        print(schemes)
    else:
        print("\n".join(schemes))


def rgb_to_ansi256(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232

    return (
        16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    )


def get_fg_escape(r, g, b):
    return "\033[38;5;{}m".format(rgb_to_ansi256(r, g, b))


def get_bg_escape(r, g, b):
    return "\033[48;5;{}m".format(rgb_to_ansi256(r, g, b))


def preview_schemes(args):
    for scheme_name in get_scheme_list():
        try:
            scheme = get_scheme(scheme_name)
            for j in range(16):
                i = hex(j)[2:].upper().zfill(2)
                print(
                    get_bg_escape(
                        scheme["base{}-rgb-r".format(i)],
                        scheme["base{}-rgb-g".format(i)],
                        scheme["base{}-rgb-b".format(i)],
                    )
                    + " ",
                    end="",
                )
            print("\033[0;00m " + scheme_name)
        except Exception as e:
            print("\033[0;00m")
            # print(scheme)
            # raise e
            pass


def render(args):
    with open(args.template) as fh:
        template = fh.read()

    scheme = get_scheme(args.scheme)

    print(pystache.render(template, scheme))


def main():
    parser = argparse.ArgumentParser(prog=__file__)
    subparsers = parser.add_subparsers(help="sub-command help")
    subparsers.add_parser("download", help="download all the schemes").set_defaults(
        func=download_schemes
    )
    list_parser = subparsers.add_parser("list", help="list downloaded schemes")
    list_parser.add_argument("--json", action="store_true", help="output as JSON")
    list_parser.set_defaults(func=list_schemes)
    subparsers.add_parser(
        "preview", help="preview theme colors in terminal"
    ).set_defaults(func=preview_schemes)
    render_parser = subparsers.add_parser(
        "render", help="render a mustache template to standard output"
    )
    render_parser.set_defaults(func=render)
    render_parser.add_argument("scheme", type=str, help="name of the base16 theme")
    render_parser.add_argument(
        "template", type=str, help="path to the mustache template"
    )

    args = parser.parse_args(sys.argv[1:])

    if not "func" in args:
        parser.print_help()
        raise SystemExit
    args.func(args)


if __name__ == "__main__":
    main()
