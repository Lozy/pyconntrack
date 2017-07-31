#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 File:        conntrack.py
 Author:      konia Zheng
 Mail:        konia@maxln.com
 Date:        2017/7/26
 Description:   `/proc/net/nf_conntrack` converter

"""

import os
import re
import json


class NFConntrack(object):
    def __init__(self):
        self.conntrack = "/proc/net/nf_conntrack"

    def _load_conntrack(self):
        conntrack_data = []

        if os.path.exists(self.conntrack):
            with open(self.conntrack, "r") as file_handle:
                conntrack_data = file_handle.readlines()

        return conntrack_data

    @staticmethod
    def conntrack_format(conntrack_data):
        if not conntrack_data or not isinstance(conntrack_data, list):
            return []

        protocol_items = ["network", "network_number", "protocol", "protocol_number", "expire", "state"]
        equal_items = ["src", "dst", "sport", "dport", "type", "code", "id", "dstkey", "srckey", "stream_timeout",
                       "timeout"]
        map_names = ["input", "output"]

        protocol_rule = r"^([a-z0-9]+)[\s\t]+([0-9]+)[\s\t]+([a-z]+)[\s\t]+([0-9]+)[\s\t]+([0-9]+)[\s\t]+([^s ]*)"
        equal_rule = r"([a-z]+)=([0-9.]+)"
        assure_rule = r"\[ASSURED\]"

        conntrack_collect = []

        for conntrack in conntrack_data:
            protocol_data = re.findall(protocol_rule, conntrack)
            equal_data = re.findall(equal_rule, conntrack)
            assure_tag = bool(re.search(assure_rule, conntrack))

            data = dict(zip(protocol_items, protocol_data[0]))
            data["assured"] = assure_tag

            for equal_item in equal_data:
                if equal_item[0] in equal_items:
                    for map_item in map_names:
                        if map_item not in data:
                            data[map_item] = {}

                        if equal_item[0] not in data[map_item]:
                            data[map_item][equal_item[0]] = equal_item[1]
                            break
                else:
                    data[equal_item[0]] = equal_item[1]

            conntrack_collect.append(data)

        return conntrack_collect

    def fetch_conntrack(self):
        return self.conntrack_format(self._load_conntrack())

    @staticmethod
    def filiter_network(conntrack_msg, network=""):
        result = []
        for msg in conntrack_msg:
            if not network or msg["protocol"] == network:
                result.append(msg)

        return result

    @staticmethod
    def filiter_src(conntrack_msg, chain, src, sport=""):
        result = []
        for msg in conntrack_msg:
            if msg[chain]["src"] == src:
                if not sport or msg[chain].get("sport", "-") == sport:
                    result.append(msg)

        return result

    @staticmethod
    def filiter_dst(conntrack_msg, chain, dst, dport=""):
        result = []
        for msg in conntrack_msg:
            if msg[chain]["dst"] == dst:
                if not dport or msg[chain].get("dport", "-") == dport:
                    result.append(msg)
        return result

    def list(self, indent=4, **kwargs):
        print json.dumps(self.fetch_conntrack(), indent=indent)

    def forward(self, ipaddr, port, indent=4, **kwargs):
        if not ipaddr:
            return False

        print json.dumps(self.filiter_src(self.fetch_conntrack(), "output", ipaddr, port), indent=indent)

    def server(self, ipaddr, port, indent=4, **kwargs):
        if not ipaddr:
            return False
        print json.dumps(self.filiter_dst(self.fetch_conntrack(), "input", ipaddr, port), indent=indent)

    def client(self, ipaddr, port="", indent=4, **kwargs):
        if not ipaddr:
            return False

        print json.dumps(self.filiter_dst(self.fetch_conntrack(), "input", ipaddr, port), indent=indent)
