#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from os import makedirs, path

from . import RAWCORPUS_DIR
from .textio import lsfile, pdf_to_text


class CustomCorpus(object):

    def __init__(self, corpus, path_to_dir, input_type="pdf"):

        self.corpus = corpus
        self.corpus_path = path.join(RAWCORPUS_DIR, self.corpus)
        self.path_to_dir = path_to_dir
        self.input_type = input_type

        if not path.exists(self.corpus_path):
            makedirs(self.corpus_path)
            print(path.exists(self.corpus_path), "yayyyy")

    def build(self):

        print("Building custom corpus \'%s\'..." % self.corpus)
        input_file_paths = lsfile(self.path_to_dir, "*." + self.input_type)

        if self.input_type == "pdf":
            for input_file_path in input_file_paths:
                pdf_to_text(
                    file_path=input_file_path,
                    parsed_path=path.join(
                        self.corpus_path,
                        "txt".join(
                            path.basename(input_file_path).rsplit("pdf")
                        )
                    )
                )

        print("'%s' corpus built\n" % self.corpus)
