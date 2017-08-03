#! /usr/bin/env python


"""

Export textual UniProt records format for PROKKA. Reads from STDIN, writes to
STDOUT

"""

from __future__ import print_function

import itertools
import re
import os

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys


__author__ = "Ilia Korvigo"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Ilia Korvigo"
__email__ = "ilia.korvigo@gmail.com"


map = map if sys.version_info.major >= 3 else itertools.imap
DESCRIPTION_PATERN = re.compile("Full=([A-Za-z0-9\-()/,.:\s]+)")


def sprot_description(description):
    """
    :type description: str
    """
    matches = DESCRIPTION_PATERN.findall(description)
    return ";".join(map(str.strip, matches))


def toprokka(srec):
    """
    :type srec: SeqRecord
    """
    id_ = srec.id
    name = srec.name.split("_")[0]  # drop the species part if present
    descr = sprot_description(srec.description)
    prokka_id = "{} ~~~{}~~~{}".format(id_, name, descr)
    return SeqRecord(seq=srec.seq, id=prokka_id, name="", description="")


def main():
    try:
        sprot_records = SeqIO.parse(sys.stdin, "swiss")
        prokka_records = map(toprokka, sprot_records)
        SeqIO.write(prokka_records, sys.stdout, "fasta")
    except BrokenPipeError:  # pipe closed
        pass

if __name__ == "__main__":
    main()
