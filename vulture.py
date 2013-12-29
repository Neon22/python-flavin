#! /usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# vulture - Find dead code.
#
# Copyright (C) 2012  Jendrik Seipp (jendrikseipp@web.de)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import optparse
import os.path
import shutil

from wake import Vulture


def parse_args():
    def csv(option, opt, value, parser):
        setattr(parser.values, option.dest, value.split(','))
    usage = "usage: %prog [options] PATH [PATH ...]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--exclude', action='callback', callback=csv,
                      type="string", default=[],
                      help='Comma-separated list of filename patterns to '
                           'exclude (e.g. svn,external).')
    parser.add_option('-v', '--verbose', action='store_true')
    parser.add_option('--halt_on_main', action='store_true')
    parser.add_option('--minimise', action='store_true')
    options, args = parser.parse_args()
    return options, args

### minimse functions

def copy_modules_as_ref(files):
    """ copy the paths to local ./ dir
        rename with '_ref.py' at end
    """
    for f in files:
        parts = os.path.split(f)
        print parts
        path = './'
        fname = os.path.splitext(parts[-1])
        path += fname[0]+'_ref'+fname[1]
        # copy filen
        shutil.copyfile(f, path)

def copy_primary_to_minimal(filename):
    " copy the filename to filename_minimal "
    parts = os.path.splitext(filename)
    newname = parts[0]+'_minimal'+parts[1]
    # copy file
    shutil.copyfile(filename, newname)
    return newname

def minimise_primary(prim_filename):
    " replace imports in prim_file with '_minimal' names "
    pass
def minimise_modules(files):
    """ for each '_ref' file create an '_minimal' file
        with the unused refs omitted
    """
    pass

if __name__ == '__main__':
    options, args = parse_args()
    if args:
        minimise = options.minimise
        vulture = Vulture(exclude=options.exclude, verbose=options.verbose, halt_on_main=options.halt_on_main)
    else:
        vulture = Vulture(exclude=[], verbose=False, halt_on_main=True)
        args = ['test.py']
        minimise = True
    vulture.scavenge(args)
    vulture.report()
    #
    if minimise:
        print("\nCleaning up import files")
        files = vulture.get_import_files()
        unused = vulture.get_unused_references()
        print("Primary = {}".format(args[0]))
        print(files)
        print(unused)
        modules_assoc = copy_modules_as_ref(files)
        primary = copy_primary_to_minimal(args[0])
        minimise_modules(modules_assoc)
        minimise_primary(primary)
        print("Minimal master is: {}".format(primary))
