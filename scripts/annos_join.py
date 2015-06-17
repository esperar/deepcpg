#!/usr/bin/env python

import argparse
import sys
import logging
import os.path as pt
import pandas as pd

from predict import annos


class App(object):

    def run(self, args):
        name = pt.basename(args[0])
        parser = self.create_parser(name)
        opts = parser.parse_args(args[1:])
        return self.main(name, opts)

    def create_parser(self, name):
        p = argparse.ArgumentParser(
            prog=name,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Combines multiple bed files and joins overlapping annotations ')
        p.add_argument(
            'in_files',
            help='Annotation tracks in bed format',
            nargs='+')
        p.add_argument(
            '-o', '--out_file',
            help='Output file')
        p.add_argument(
            '--verbose',
            help='More detailed log messages',
            action='store_true')
        p.add_argument(
            '--log_file',
            help='Write log messages to file')
        return p

    def main(self, name, opts):
        logging.basicConfig(filename=opts.log_file,
                            format='%(levelname)s (%(asctime)s): %(message)s')
        log = logging.getLogger(name)
        if opts.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        log.debug(opts)

        log.info('Read annotations ...')
        d = []
        for in_file in opts.in_files:
            d.append(annos.read_bed(in_file), usecols=[0, 1, 2])
        d = pd.concat(d)

        log.info('Join annotations ...')
        d = annos.join_overlapping_frame(d)

        log.info('Write annotations ...')
        s = d.to_csv(opts.out_file, sep='\t', header=None, index=False)
        if s is not None:
            print(s, end='')

        return 0


if __name__ == '__main__':
    app = App()
    app.run(sys.argv)