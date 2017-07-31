#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from optparse import OptionParser
from conntrack import NFConntrack


class Utils(object):
    @staticmethod
    def parse_args(parser, cmd_options):
        for optkey, optlist in cmd_options.iteritems():
            if isinstance(optlist[1], dict):
                parms = optlist[1]

            elif isinstance(optlist[1], list):
                parms = {
                    "action": optlist[1][0],
                    "default": optlist[1][1],
                    "help": optlist[1][2],
                    "dest": optkey
                }

                if len(optlist) > 5:
                    parms["type"] = optlist[5]
            else:
                parms = {}

            parser.add_argument(*optlist[0], **parms)

        return parser

    @classmethod
    def multi_commands_args(cls, options):
        parser = argparse.ArgumentParser(prog=options["name"])
        cls.parse_args(parser, options.get("default", {}))
        subparsers = parser.add_subparsers(dest="subparsers")

        for subparsers_name, subparsers_opts in options.get("subparsers", {}).iteritems():
            the_subparsers = subparsers.add_parser(subparsers_name, help=subparsers_opts[0])
            cls.parse_args(the_subparsers, subparsers_opts[1])

        args = parser.parse_args()
        return vars(args)

    @staticmethod
    def commands_args(version, cmd_options):
        """
        @set 'cmd_options' to add command options.
        @example:
            {
            "key": [
                "short-argument", "argument",
                {"type": "int", "action": "store", "default": 0, "help": "xxx"}
            ],
            "old_key": [
                "short-argument", "argument", "store/store_true/store_false",
                "default-value", "help", "string/int"
            ]
            }
        """
        if not isinstance(cmd_options, dict):
            return None

        usage = "usage: %prog [option1] arg1 [option2] arg2"
        parser = OptionParser(usage=usage, version=version)

        for optkey, optlist in cmd_options.iteritems():
            if isinstance(optlist[2], dict):
                parms = optlist[2]
            else:
                parms = {
                    "action": optlist[2],
                    "default": optlist[3],
                    "help": optlist[4],
                }

                if len(optlist) > 5:
                    parms["type"] = optlist[5]

            parser.add_option(optlist[0], optlist[1], dest=optkey, **parms)

        options = parser.parse_args()[0]

        return options


def main():
    args = {
        "name": "conntrack info api",
        "default": {
            "indent": [
                ["-n", "--indent"],
                {
                    "action": "store",
                    "default": -1,
                    "help": "specify print indent",
                    "dest": "indent",
                    "type": int
                }
            ]
        },
        "subparsers": {
            "list": [
                "list all conntrack info",
                {}
            ],
            "forward": [
                "list nat connect conntrack",
                {
                    "ipaddr": [
                        ["-i", "--ipaddr"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify real-server ip addr",
                            "dest": "ipaddr"
                        }
                    ],
                    "port": [
                        ["-p", "--port"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify real-server port",
                            "dest": "port"
                        }
                    ]
                }
            ],
            "server": [
                "list nat connect conntrack",
                {
                    "ipaddr": [
                        ["-i", "--ipaddr"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify nat-server ip addr",
                            "dest": "ipaddr"
                        }
                    ],
                    "port": [
                        ["-p", "--port"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify nat-server port",
                            "dest": "port"
                        }
                    ]
                }
            ],
            "client": [
                "list nat connect conntrack",
                {
                    "ipaddr": [
                        ["-i", "--ipaddr"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify client ip addr",
                            "dest": "ipaddr"
                        }
                    ],
                    "port": [
                        ["-p", "--port"],
                        {
                            "action": "store",
                            "default": "",
                            "help": "specify client port",
                            "dest": "port"
                        }
                    ]
                }
            ],
        }
    }

    cmd_handle = Utils.multi_commands_args(args)

    if cmd_handle.get("indent", -1) < 0:
        cmd_handle["indent"] = None

    nft_conntrack = NFConntrack()
    cmd_method = getattr(nft_conntrack, cmd_handle["subparsers"], None)

    if cmd_method:
        cmd_method(**cmd_handle)
    else:
        print "not support method"


if __name__ == '__main__':
    main()
