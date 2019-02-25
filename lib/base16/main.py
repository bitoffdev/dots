#!/usr/bin/env python3
import argparse
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
        for name in filter(lambda x: x[-5:] == '.yaml', names):
            yield name[:-5]

def get_scheme(name):
    scheme_dir = os.path.join(BASE_DIR, "schemes")
    path = None
    for parent, _, names in os.walk(scheme_dir):
        if name + '.yaml' in names:
            path = os.path.join(parent, name + '.yaml')
    if path:
        with open(path) as fh:
            return Base16Dict(yaml.load(fh))

class Base16Dict(dict):

    """
    Implements github.com/chriskempson/base16/blob/master/builder.md#template-variables
    """

    def __getitem__(self, key):
        m = re.match('(base0[0-9A-F])(?:-(hex|rgb|dec))(?:-([rgb]))?', key)
        for _ in range(1 if m else 0):
            base, encoding, channel = m.groups()
            if not base or not encoding: break
            # TODO allow other encodings
            assert encoding == 'hex'

            # exit early if we no channel was specified
            if not channel:
                return dict.__getitem__(self, base)

            # get the correct channel
            index = 'rgb'.index(channel) * 2
            return dict.__getitem__(self, base)[index:index+2]

        # no match found
        key = 'scheme' if key == 'scheme-name' else key
        key = 'author' if key == 'scheme-author' else key
        return dict.__getitem__(self, key)

    def __contains__(self, value):
        return dict.__contains__(self, value) or \
                isinstance(self.__getitem__(value), str)

def download_schemes(args):
    LIST_URL = "https://raw.githubusercontent.com/chriskempson/base16-schemes-source/master/list.yaml"
    with urlopen(LIST_URL) as fh:
        scheme_list = yaml.load(fh)
        for name in scheme_list:
            url = scheme_list[name]
            cmd = ['git', 'clone', url, os.path.join(BASE_DIR, "schemes", name)]
            print(" ".join(cmd))
            subprocess.run(cmd)

def list_schemes(args):
    print(sorted(list(get_scheme_list())))


def render(args):
    with open(args.template) as fh:
        template = fh.read()

    scheme = get_scheme(args.scheme)

    print(pystache.render(template, scheme))

def main():
    parser = argparse.ArgumentParser(prog=__file__)
    subparsers = parser.add_subparsers(help='sub-command help')
    subparsers.add_parser('download', help='download all the schemes').set_defaults(func=download_schemes)
    subparsers.add_parser('list', help='list downloaded schemes').set_defaults(func=list_schemes)
    render_parser = subparsers.add_parser('render', help='render a mustache template to standard output')
    render_parser.set_defaults(func=render)
    render_parser.add_argument('scheme', type=str, help='name of the base16 theme')
    render_parser.add_argument('template', type=str, help='path to the mustache template')

    args = parser.parse_args(sys.argv[1:])

    if not 'func' in args:
        parser.print_help()
        raise SystemExit
    args.func(args)

if __name__ == "__main__":
    main()
