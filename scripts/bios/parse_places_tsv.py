# -*- coding: utf-8 -*-
from sefaria.model import *
import unicodecsv as csv


"""
0 English Name
1 Hebrew Name
2 GeoCode
"""

PlaceSet().delete()

def _(p, attr, field):
    if field:
        setattr(p, attr, field)

with open("Torah Commentators - Bios - Places.tsv") as tsv:
    next(tsv)
    next(tsv)
    for l in csv.reader(tsv, dialect="excel-tab"):

        #todo: handle polygons?
        latlon = []
        try:
            latlon = [float(_) for _ in l[2].split(",")]
        except Exception as e:
            if l[2] != "#ERROR!":
                print "Failed to parse geo: {}. \n{}".format(l[2], e)
            continue
        if len(latlon) != 2:
            continue

        key = l[0]
        p = Place().load({"key": key}) or Place()

        p.key = key
        p.name_group.add_title(l[0], "en", primary=True, replace_primary=True)
        if l[1]:
            p.name_group.add_title(l[1], "he", primary=True, replace_primary=True)

        p.set_location(latlon[0], latlon[1])

        p.save()