#!/usr/bin/env python3


def get_title(txt):
    txt = txt.replace("-", " ")
    txt = txt.title()
    return txt


def get_slug(txt):
    txt = txt.lower()
    txt = txt.replace(" ", "-")
    return txt
