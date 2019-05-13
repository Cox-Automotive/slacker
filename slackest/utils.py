#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_item_id_by_name(list_dict, key_name):
    for d in list_dict:
        if d['name'] == key_name:
            return d['id']

def get_item_id_by_email(list_dict, key_email):
    for d in list_dict:
        if d['profile']['email'] == key_email:
            return d['id']
