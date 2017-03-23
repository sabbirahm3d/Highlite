#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from context import resquest
from parse import pdf_to_text
from resquest import buildcorpus


class RateResume:

    def __init__(self, path, area, pages=[], anon=True, build=False):

        self.path = path
        self.area = area
        self.pages = pages
        self.anon = anon
        self.build = build
        self.resume_corpus = buildcorpus.ResumeCorpus(
            area=self.area,
            pages=self.pages,
            anon=self.anon
        )

        self.glob_bow = self.resume_corpus.get_data(data="bow")
        self.bow = pdf_to_text(self.path)
        self.intersection = (set(self.bow.keys()) & set(self.glob_bow.keys()))

        self.ratios = {}
        self.local_total = 0
        self.global_total = 0

    def build(self):

        if self.build:
            self.resume_corpus.build()

    def get_glob_bow(self):

        return self.glob_bow

    def get_bow(self):

        return self.bow

    def get_intersection(self):

        return self.intersection

    def get_stats(self, data=False):

        stats = {
            "area": self.area,
            "total_local": self.local_total,
            "global_local": self.global_total,
            "len_intersect": len(self.intersection),
            "data": self.ratios
        }

        if not data:
            return {
                key: value for key, value in stats.items() if key != "data"
            }

        return stats

    def rate(self):

        for word in self.intersection:

            self.ratios[word] = {
                "local": self.bow[word],
                "global": self.glob_bow[word]
            }
            self.local_total += self.bow[word]
            self.global_total += self.glob_bow[word]


if __name__ == '__main__':

    from pprint import pprint

    obj = RateResume(path="../sample/resume.pdf", area="Anthropology")
    obj.rate()
    pprint(obj.get_stats())

    obj = RateResume(path="../sample/resume.pdf", area="Computer Science")
    obj.rate()
    pprint(obj.get_stats())

    obj = RateResume(path="../sample/resume.pdf", area="Data Science")
    obj.rate()
    pprint(obj.get_stats())
