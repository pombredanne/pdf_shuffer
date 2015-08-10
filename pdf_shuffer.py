#!/usr/bin/env python3
# encoding: utf-8

'''
Other good PDF utils available on Debian/Ubuntu Linux:
pdfshuffler	a gui of PyPDF.
pdfgrep		search pdf files for a regular expression. For example, "pdfgrep -n scare *.pdf" search a word among pdf files under current directory.
cups-pdf	PDF printer for CUPS. It does what SmartPrint does on Windows.
ImageMagick	http://www.imagemagick.org/script/index.php. ImageMagick® is a software suite to create, edit, compose, or convert bitmap images.
briss		http://sourceforge.net/projects/briss/. This project aims to offer a simple cross-platform application for cropping PDF files. A simple user interface lets you define exactly the crop-region by fitting a rectangle on the visually overlaid pages. Note: Cropping changes page size.

http://ma.juii.net/blog/scale-page-content-of-pdf-files, How to scale the page content of PDF files?
http://stackoverflow.com/questions/6118635/what-is-the-best-pdf-open-source-library-for-java
http://blog.mashape.com/post/66047403916/list-of-50-pdf-generation-manipulation-and
http://www.cyberciti.biz/faq/removing-password-from-pdf-on-linux/, HowTo: Linux Remove a PDF File Password Using Command Line Options

PDF Clown	http://www.stefanochizzolini.it/common/contents/projects/clown/samples/PageCoordinatesSample.java, ctm.getScaleX()
iText		http://itextpdf.com/product/itext. iText is a Java PDF library that allows you to CREATE, ADAPT, INSPECT and MAINTAIN documents in the Portable Document Format (PDF). It's dual-licensed.
PyPDF2		http://knowah.github.io/PyPDF2/, https://github.com/knowah/PyPDF2. PDF toolkit implemented solely in Python. PyPDF2 does what pdftk does. pdfshuffler is a GUI of PyPDF.
multivalent	http://multivalent.sourceforge.net/Tools/index.html. PDF tools written in Java.


[PDFjam Examples]
1. Resize all pages to A5. Note: The scale ratio is derived from the the first page. The other pages don't scale correctly it their size are different from the first one.
$ pdfjam --paper a5paper --outfile ~/tmp/04.pdf 04.pdf
2. Rotate all pages in counter-clockwise 90 degress.
$ pdfjam --angle 90 --landscape --outfile ~/tmp/04.pdf 04.pdf
3. Remove pages 2-3 and 11-12, and insert a blank page after page 1.
pdfjam --outfile ~/tmp/04.pdf 04.pdf "1,{},4-10,13-"
4. Split a file into three parts.
$ pdfjam --outfile ~/tmp/04_part1.pdf 04.pdf "1-10"
$ pdfjam --outfile ~/tmp/04_part2.pdf 04.pdf "11-30"
$ pdfjam --outfile ~/tmp/04_part3.pdf 04.pdf "31-"
5. Merge multiple files into one.
$ pdfjam --outfile ~/tmp/04.pdf ~/tmp/04_part1.pdf ~/tmp/04_part2.pdf ~/tmp/04_part3.pdf
6. Combine multiple pages onto each sheet.
$ pdfjam --nup 2x1 --landscape --outfile ~/tmp/04.pdf 04.pdf
7. Clip a page into two pages.
Assume 01exp.pdf contains only one physical page, which consists of two logical pages, and "Paper Size: A4, Landscape (11.69 x 8.27 inch)". (01exp.pdf can be generated from "pdfjam --landscape --outfile 01exp.pdf 01a4-book.pdf 1")
Need to clip it into two pages, each "Paper Size: A4, Portrait (8.27 x 11.69 inch)". A DIN A4 page (width×height) = 210x297 mm = 595×842 pps = 8.27x11.69 inch. 1 inch = 72 pps = 25.4 millimeter.
Get the left logical page:
$ pdfjam --trim "0 0 148.5mm 0" --outfile 01expL.pdf 01exp.pdf 
Get the right logical page:
$ pdfjam --trim "148.5mm 0 0 0" --outfile 01expR.pdf 01exp.pdf
8. Scale the page content of PDF files while keeping the physical page size the same. (http://www2.warwick.ac.uk/fac/sci/statistics/staff/academic-research/firth/software/pdfjam/, http://ma.juii.net/blog/scale-page-content-of-pdf-files)
Scale at center and move the given offset relative to the left-bottom.
$ pdfjam --scale 1.06 --offset '2cm 2cm' --outfile tmp2/A1_06.pdf tmp2/A.pdf
9. Arrange pages into a booklet. Note to pass total page number, round up to a multiple of 4, to "--signature".
$ pdfbook --short-edge --signature 56 04.pdf
10.
$ pdfjam --landscape --offset "6mm 0" --outfile 1final.pdf ~/tmp/1nup.pdf (move content 6mm right-forward)

[Advanced PDFjam Examples]
1. Make a A5 booklet for "Disney's World Of English book 01.pdf". 
This file contains 57 pages. The last page is meanless and I decide not to print it. The first page size is much larger the the others. So it's necessary to resize them separately.
1.1 Rename to a shorter name.
$ cp Disney\'s\ World\ Of\ English\ book\ 01.pdf 01.pdf
1.2 Resize the first page.
$ pdfjam --paper a4paper --outfile 01p1.pdf 01.pdf 1
1.3 Resize the other pages except 57.
$ pdfjam --paper a4paper --outfile 01p2.pdf 01.pdf 2-56
1.4 Merge all pages.
$ pdfjam --outfile 01a4.pdf 01p1.pdf 01p2.pdf
1.5 Make a booklet.
$ pdfbook --short-edge --signature 56 01a4.pdf
If left blank of each logical page is desired, use following command:
$ pdfbook --short-edge --signature 56 --delta "2cm 0" 01a4.pdf

The final output is 01a4-book.pdf. Each logical page size is A5. Print it double-side, then bind pages at the middle.

2. Print "truck town" twoside, each side contains 4 A6 pages.
truck.pdf contains 420 pages. There are 35 booklets, each booklet contains 12 pages. There are 4 meanless pages in each booklet: page 2, 3, 11 and 12. So there are 8*35 pages need to print. If they are printed 4 pages on each A4 sheet and twoside, it will only require 35 A4 papers.
2.1 Delete pages 2, 3, 11 and 12 in each booklet. The result pdf contains 280 pages.
$ pdf_shuffer.py -d 12*n+2,12*n+3,12*n+11,12*n+12 truck.pdf tmp
2.2 Combine 4 pages. The result pdf contains 70 physical pages. Paper size is scaled to A4 automatically.
$ pdfjam --nup 2x2 --delta "2mm 2mm" --frame true --outfile truck22.pdf tmp/truck.pdf
2.3 There's no space reserved for binding on each page of the result pdf of above step. Following command reserve 10 mm at each paper's left side. The scale ratio is: 1 - offset * 2 / 210 = 0.95238.
$ pdfjam --scale 0.95238 --offset "5mm 0" --twoside --outfile truck22o.pdf truck22.pdf

The final output is truck22o.pdf. Each logical page size is A6. Print it double-side, then bind pages at the left.

3. Make an A6 booklet for "truck town".
3.1 Resize all pages to A4.
$ pdfjam --paper a4paper --outfile trucka4.pdf truck.pdf
3.2 Make an A5 booklet.
$ pdfbook --short-edge --signature 12 trucka4.pdf
3.3 The total page number 210 (must be even) of trucka4.pdf is not a multiple of 4. To fix that, append two blank pages at the end.
$ pdfjam --landscape --outfile trucka4-book2.pdf trucka4-book.pdf "1-,{},{}"
3.4 Swap 4n+2 and 4n+3.
$ pdf_shuffer.py -m 4*n+3:4*n+2 trucka4-book2.pdf tmp
3.5 Combine every 2 pages into one.
$ pdfjam --nup 1x2 --frame true --outfile trucka4-book3.pdf tmp/trucka4-book2.pdf

The final output is trucka4-book3.pdf. Each logical page size is A6. Print it double-side, cut each A4 paper into two A5, bind every 6 A5 papers into an A6 booklet.

[TODO]
1. How to scale two dimensions separately? gs sometimes work, sometimes broken.
$ pdfjam --no-tidy --scale "1 1.2" trucka4.pdf
$ pdfjam --trim "0 30.375 0 30.375" --clip true --frame true trucka4.pdf
2. pdfjam cannot query the number of pages. pdfinfo can do that. Maybe it's better to replace pdftk with pdfjam & pdfinfo in this script?
'''

import subprocess
import tempfile
import os.path
import argparse
import re
import shutil
import locale
import logging
import sys
import readline
import traceback

tmpd_ = tempfile.TemporaryDirectory()
#tmpd = tmpd_.name
tmpd = '/tmp' #Keep temporary directory when debug

patt_add_exp = '^[\dn+\-*/]+:[\dn+\-*/]+(,[\dn+\-*/]+:[\dn+\-*/]+)*(@\d+(-\d+)?(,\d+(-\d+)?)*)?$'
patt_del_exp = '^[\dn+\-*/]+(,[\dn+\-*/]+)*(@\d+(-\d+)?(,\d+(-\d+)?)*)?$'
patt_mov_exp = patt_add_exp
patt_rotate_exp = patt_del_exp
patt_join_exp = patt_del_exp
patt_split_exp = patt_del_exp
patt_pg_size = 'Page\s+(?P<pn>\d+)\s+size:\s+(?P<width>[\d\.]+)\s+x\s+(?P<height>[\d\.]+)\s+.*'
patt_paper = '^a[1-6]paper$'

encoding = locale.getdefaultlocale()[1]
if(not encoding):
    # None means the portable 'C' locale. However str.decode(encoding) doesn't accept None.
    encoding = 'ASCII'

def getstatusoutput(cmdline, keepStdErr=True, raiseException=True):
    logging.info(str(cmdline))
    if(keepStdErr):
        err = subprocess.STDOUT
    else:
        err = None
    stdout = subprocess.PIPE
    proc = subprocess.Popen(cmdline, stdout=stdout, stderr=err, shell=isinstance(cmdline, str))
    out, _ = proc.communicate()
    if(out):
        out2 = out.decode(encoding, 'ignore')
    else:
        out2 = ''
    logging.info(out2)
    # A None value indicates that the process hasn't terminated yet.
    assert(proc.returncode!=None)
    if(proc.returncode!=0 and raiseException):
        raise Exception('command failure: ' + str(cmdline))
    return(proc.returncode, out2)

def reglob(path, exp, invert=False):
    """glob.glob() style searching which uses regex
    :param exp: Regex expression for filename
    :param invert: Invert match to non matching files
    """
    m = re.compile(exp)
    if invert is False:
        res = [f for f in os.listdir(path) if m.match(f)]
    else:
        res = [f for f in os.listdir(path) if not m.match(f)]
    res = list(map(lambda x: os.path.join(path, x), res))
    return res

class RangeList(object):
    def __init__(self, spec):
        '''1,3-5,6'''
        self.rl = list()
        for subspec in spec.split(','):
            tokens = subspec.split('-')
            begin = int(tokens[0])
            if(len(tokens)>=2):
                end = int(tokens[1])
            else:
                end = begin
            self.rl.append(range(begin, end+1))
    def __iter__(self):
        for r in self.rl:
            for i in r:
                yield i

def eval_del_exp(max_pn, del_exp):
    if(re.match(patt_del_exp, del_exp) == None):
        raise Exception('invalid del_exp: ' + del_exp)
    ops = list()
    tokens = del_exp.split('@')
    if(len(tokens)>=2):
        n_range = RangeList(tokens[1])
    else:
        n_range = range(0, max_pn+1)
    del_exp = tokens[0]
    exps = del_exp.split(',')
    for exp_pn in exps:
        if(exp_pn.find('n') == -1):
            # constant page no
            pn = int(exp_pn)
            if((pn > 0) and (pn <= max_pn)):
                ops.append(pn)
            continue
        for n in n_range:
            try:
                pn = int(eval(exp_pn))
            except (NameError, SyntaxError):
                print('invalid del_exp: '+ del_exp)
                raise
            if((pn >= 1) and (pn <= max_pn)):
                ops.append(pn)
    ops = sorted(set(ops))
    return ops

def eval_add_exp(max_pn, add_exp):
    if(re.match(patt_add_exp, add_exp) == None):
        raise Exception('invalid add_exp: ' + add_exp)
    ops = dict()
    tokens = add_exp.split('@')
    if(len(tokens)>=2):
        n_range = RangeList(tokens[1])
    else:
        n_range = range(0, max_pn+1)
    add_exp = tokens[0]
    exps = add_exp.split(',')
    for exp in exps:
        add_spec = exp.split(':')
        exp_pn = add_spec[0]
        exp_blanks = add_spec[1]
        if(exp.find('n') == -1):
            # constant page no
            pn = int(exp_pn)
            blanks = int(exp_blanks)
            if((pn >= 1) and (pn <= max_pn + 1) and (blanks >= 1) and (pn not in ops)):
                ops[pn] = blanks
            continue
        for n in n_range:
            try:
                pn = int(eval(exp_pn))
                blanks = int(eval(exp_blanks))
            except (NameError, SyntaxError):
                print('invalid add_exp: '+ add_exp)
                raise
            if((pn >= 1) and (pn <= max_pn + 1) and (blanks >= 1) and (pn not in ops)):
                ops[pn] = blanks
    return sorted(ops.items())

def eval_mov_exp(max_pn, mov_exp):
    assert(mov_exp!=None)
    if(re.match(patt_mov_exp, mov_exp) == None):
        raise Exception('invalid mov_exp: ' + mov_exp)
    ops = list()
    tokens = mov_exp.split('@')
    if(len(tokens)>=2):
        n_range = RangeList(tokens[1])
    else:
        n_range = range(0, max_pn+1)
    mov_exp = tokens[0]
    exps = mov_exp.split(',')
    for exp in exps:
        mov_spec = exp.split(':')
        exp_pn1 = mov_spec[0]
        exp_pn2 = mov_spec[1]
        if(exp.find('n') == -1):
            # constant page no
            pn1 = int(exp_pn1)
            pn2 = int(exp_pn2)
            if((pn1 >= 1) and (pn1 <= max_pn) and (pn2 >= 1) and (pn2 <= max_pn + 1)):
                ops.append((pn1, pn2))
            continue
        for n in n_range:
            try:
                pn1 = int(eval(exp_pn1))
                pn2 = int(eval(exp_pn2))
            except (NameError, SyntaxError):
                print('invalid mov_exp: '+ mov_exp)
                raise
            if((pn1 >= 1) and (pn1 <= max_pn) and (pn2 >= 1) and (pn2 <= max_pn + 1)):
                ops.append((pn1, pn2))
    return ops

'''ints is in type of list or set'''
def ints2str(ints):
    ints = list(ints)
    ints.sort()
    l = (str(item) for item in ints)
    res = ' '.join(l)
    return res

def pg_path_patt():
    return os.path.join(tmpd, 'pg_%d.pdf')

def pg_paths():
    return reglob(tmpd, '^pg_\d+.pdf$')

def pg_path(pg_no):
    return os.path.join(tmpd, 'pg_%d.pdf'%pg_no)

def pg_num(pg_fp):
    return int(os.path.splitext(os.path.basename(pg_fp))[0][3:])

def blank_fp(prototype_fp):
    fp = os.path.join(tmpd, 'blank1.pdf')
    if(os.path.isfile(fp)):
        return fp
    assert(os.path.isfile(prototype_fp))
    getstatusoutput(['pdfjam', '--outfile', fp, prototype_fp, '{},1'])
    getstatusoutput(['pdfjam', '--outfile', fp, fp, '1'])
    assert(os.path.isfile(fp))
    return fp

def pglist2str(pglist):
    l = (os.path.basename(item) for item in pglist)
    return ' '.join(l)

'''
There are several ways to get number of pages:

zhichyu@jupiter:~$ pdftk 01.pdf dump_data
InfoKey: Creator
InfoValue: ACDSee
InfoKey: Title
InfoValue: ACDSee PDF Image.
InfoKey: CreationDate
InfoValue: D:20070303102909
NumberOfPages: 57

zhichyu@jupiter:~$ pdftk 01.pdf burst
zhichyu@jupiter:~$ cat doc_data.txt
InfoKey: Creator
InfoValue: ACDSee
InfoKey: Title
InfoValue: ACDSee PDF Image.
InfoKey: CreationDate
InfoValue: D:20070303102909
NumberOfPages: 57

zhichyu@jupiter:~/tmp$ pdfinfo -f 1 -l 100000 /home/zhichyu/tmp/1.pdf
Creator:        TeX
Producer:       iText® 5.2.0 ©2000-2012 1T3XT BVBA
CreationDate:   Mon Jan 20 16:17:38 2014
ModDate:        Mon Jan 20 16:22:03 2014
Tagged:         no
Form:           none
Pages:          34
Encrypted:      no
Page    1 size: 522.24 x 773.81 pts
Page    1 rot:  0
Page    2 size: 520.24 x 769.81 pts
Page    2 rot:  0
Page    3 size: 522.24 x 773.81 pts
Page    3 rot:  0
Page    4 size: 520.24 x 769.81 pts
Page    4 rot:  0
Page    5 size: 522.24 x 773.81 pts
Page    5 rot:  0
Page    6 size: 520.24 x 769.81 pts
Page    6 rot:  0
Page    7 size: 522.24 x 773.81 pts
Page    7 rot:  0
Page    8 size: 520.24 x 769.81 pts
Page    8 rot:  0
Page    9 size: 522.24 x 773.81 pts
Page    9 rot:  0
Page   10 size: 520.24 x 769.81 pts
Page   10 rot:  0
Page   11 size: 522.24 x 773.81 pts
Page   11 rot:  0
Page   12 size: 520.24 x 769.81 pts
Page   12 rot:  0
Page   13 size: 522.24 x 773.81 pts
Page   13 rot:  0
Page   14 size: 520.24 x 769.81 pts
Page   14 rot:  0
Page   15 size: 522.24 x 773.81 pts
Page   15 rot:  0
Page   16 size: 520.24 x 769.81 pts
Page   16 rot:  0
Page   17 size: 522.24 x 773.81 pts
Page   17 rot:  0
Page   18 size: 520.24 x 769.81 pts
Page   18 rot:  0
Page   19 size: 522.24 x 773.81 pts
Page   19 rot:  0
Page   20 size: 520.24 x 769.81 pts
Page   20 rot:  0
Page   21 size: 522.24 x 773.81 pts
Page   21 rot:  0
Page   22 size: 520.24 x 769.81 pts
Page   22 rot:  0
Page   23 size: 522.24 x 773.81 pts
Page   23 rot:  0
Page   24 size: 520.24 x 769.81 pts
Page   24 rot:  0
Page   25 size: 522.24 x 773.81 pts
Page   25 rot:  0
Page   26 size: 520.24 x 769.81 pts
Page   26 rot:  0
Page   27 size: 522.24 x 773.81 pts
Page   27 rot:  0
Page   28 size: 520.24 x 769.81 pts
Page   28 rot:  0
Page   29 size: 522.24 x 773.81 pts
Page   29 rot:  0
Page   30 size: 520.24 x 769.81 pts
Page   30 rot:  0
Page   31 size: 522.24 x 773.81 pts
Page   31 rot:  0
Page   32 size: 520.24 x 769.81 pts
Page   32 rot:  0
Page   33 size: 522.24 x 773.81 pts
Page   33 rot:  0
Page   34 size: 520.24 x 769.81 pts
Page   34 rot:  0
File size:      3808037 bytes
Optimized:      no
PDF version:    1.4

'''
def get_num_pages(fp):
    rc, output = getstatusoutput(['pdftk', fp, 'dump_data'])
    name = 'NumberOfPages:'
    val = 0
    for line in output.splitlines():
        if(line.startswith(name)):
            val = line[len(name):].strip()
            val = int(val)
            break
    return val

def get_pages_size(fp):
    rc, output = getstatusoutput(['pdfinfo', '-f', '1', '-l', '100000', fp])
    i = 0
    sizes = list()
    patt = re.compile(patt_pg_size)
    for line in output.splitlines():
        m = patt.match(line)
        if(m==None):
            continue
        pn = int(m.group('pn'))
        width = float(m.group('width'))
        height = float(m.group('height'))
        assert(pn == i+1)
        sizes.append((width, height))
        i += 1
    return sizes

def is_same_size(pg_sizes):
    assert(len(pg_sizes)>=1)
    same_size = True
    for i in range(1, len(pg_sizes)):
        (width1, height1) = pg_sizes[i-1]
        (width2, height2) = pg_sizes[i]
        if(width1!=width2 or height1!=height2):
            same_size = False
    return same_size

def get_pages_orientation(pg_sizes):
    # All pages could be in the different orientation.
    orientation = list()
    assert(len(pg_sizes)>=1)
    num_portrait = 0
    num_landscape = 0
    for i in range(0, len(pg_sizes)):
        (width, height) = pg_sizes[i]
        if(width >= height):
            num_landscape += 1
        else:
            num_portrait += 1
    if(num_portrait >= num_landscape):
        return True
    else:
        return False

def rotate_inplace(fp):
    #pdfjam --angle 90 --landscape --outfile ~/tmp/04.pdf 04.pdf
    sizes = get_pages_size(fp)
    is_portrait = get_pages_orientation(sizes)
    tmp_fp = os.path.join(tmpd, os.path.basename(fp)+'.rotated')
    if(is_portrait):
        getstatusoutput(['pdfjam', '--landscape', '--angle', '90', '--outfile', tmp_fp, fp])
    else:
        getstatusoutput(['pdfjam', '--angle', '90', '--outfile', tmp_fp, fp])
    shutil.copyfile(tmp_fp, fp)

def split(fp):
    getstatusoutput(['pdftk', fp, 'burst', 'output', pg_path_patt()])
    pages = sorted(pg_paths(), key=pg_num)
    return pages

def merge(pages, dst_fp):
    getstatusoutput(['pdftk'] + pages + ['cat', 'output', dst_fp])

def erase_pg(pglist2, new_pn):
    assert(new_pn<=len(pglist2))
    del pglist2[new_pn - 1]
    for i in range(new_pn-1, len(pglist2)):
        pg = pglist2[i]
        pg[1] -= 1

def insert_pg(pglist2, new_pn, pg):
    pg[1] = new_pn
    pglist2.insert(new_pn-1, pg)
    for i in range(new_pn, len(pglist2)):
        pg = pglist2[i]
        pg[1] += 1

'''Add blank pages per an expression.'''
def op_add(infile, outfile, expression):
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    add_spec = eval_add_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + str(add_spec))
    if(len(add_spec) == 0):
        shutil.copyfile(infile, outfile)
    else:
        pages = split(infile)
        assert(max_pn == len(pages))
        pglist = list()  # pglist1 item structure: pg_path
        for i in range(0, max_pn):
            pglist.append(pg_path(i+1))
        blank1 = blank_fp(pages[0])
        for item in reversed(add_spec):
            orig_pn = item[0]
            blank_pg_num = item[1]
            if(orig_pn > max_pn):
                for i in range(0, blank_pg_num):
                    pglist.append(blank1)
            else:
                for i in range(0, blank_pg_num):
                    pglist.insert(orig_pn-1, blank1)
        merge(pglist, outfile)

'''Delete pages whose number match an expression.'''
def op_delete(infile, outfile, expression):    
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    del_spec = eval_del_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + ints2str(del_spec))
    if(len(del_spec) == 0):
        shutil.copyfile(infile, outfile)
    else:
        pages = split(infile)
        assert(max_pn == len(pages))
        pglist = list()  # pglist item structure: [remained, pg_path]
        for i in range(0, max_pn):
            pglist.append([True, pg_path(i+1)])
        for i in del_spec:
            pglist[i-1][0] = False
        # generator expression is more powerful than built-in filter().
        pglist = list(item[1] for item in pglist if item[0]==True)
        merge(pglist, outfile)

'''Move pages per an expression.'''
def op_move(infile, outfile, expression):
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    mov_spec = eval_mov_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + str(mov_spec))
    if(len(mov_spec) == 0):
        shutil.copyfile(infile, outfile)
    else:
        getstatusoutput(['pdftk', infile, 'burst', 'output', pg_path_patt()])
        pages = sorted(pg_paths(), key=pg_num)
        assert(max_pn == len(pages))
        pglist1 = list()  # pglist1 item structure: [orig_pn, new_pn, pg_path]. pglist1 is indexed by orig_pn-1.
        pglist2 = list()  # pglist2 is a shallow copy of pglist1, and is indexed by new_pn-1.
        for i in range(0, max_pn):
            item = [i+1, i+1, pg_path(i+1)]
            pglist1.append(item)
        pglist2 = pglist1.copy()
        for (orig_pn1, orig_pn2) in mov_spec:
            pg1 = pglist1[orig_pn1 - 1]
            new_pn1 = pg1[1]
            erase_pg(pglist2, new_pn1)

            if(orig_pn2 > max_pn):
                # move pages to the end
                assert(orig_pn2 == max_pn + 1)
                insert_pg(pglist2, max_pn+1, pg1)
            else:
                # normal movement
                pg2 = pglist1[orig_pn2 - 1]
                new_pn2 = pg2[1]
                insert_pg(pglist2, new_pn2, pg1)
        # generator expression is more powerful than built-in filter().
        pglist = list(item[2] for item in pglist2)
        merge(pglist, outfile)

'''Rotate pages whose number match an expression.'''
def op_rotate(infile, outfile, expression):    
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    rotate_spec = eval_del_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + ints2str(rotate_spec))
    if(not rotate_spec):
        return
    if(len(rotate_spec) == 0):
        shutil.copyfile(infile, outfile)
    else:
        pages = split(infile)
        assert(max_pn == len(pages))
        for i in range(0, max_pn):
            if i+1 in rotate_spec:
                rotate_inplace(pages[i])
        merge(pages, outfile)

def op_join(infile, outfile, expression):    
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    join_spec = eval_del_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + ints2str(join_spec))
    if(len(join_spec) == 0):
        if(outfile != infile):
            shutil.copyfile(infile, outfile)
    else:
        sizes = get_pages_size(infile)
        pages = split(infile)
        assert(max_pn == len(pages))
        pglist = list()
        i = 0
        while(i < max_pn):
            if(i+1 in join_spec and i+1 < max_pn):
                # FIXME: pdfjam requires all PDF files' name use '.pdf' suffix.
                tmp_page1 = pages[i] + '.tmp1.pdf'
                tmp_page2 = pages[i] + '.tmp2.pdf'
                merge([pages[i], pages[i+1]], tmp_page1)
                is_portrait = get_pages_orientation(sizes[i:i+2])
                if(is_portrait):
                    cmd = ['pdfjam', '--landscape', '--nup', '2x1', '--outfile', tmp_page2, tmp_page1]
                else:
                    cmd = ['pdfjam', '--nup', '1x2', '--outfile', tmp_page2, tmp_page1]
                getstatusoutput(cmd)
                pglist.append(tmp_page2)
                i += 2
            else:
                pglist.append(pages[i])
                i += 1
        merge(pglist, outfile)

def op_split(infile, outfile, expression):    
    max_pn = get_num_pages(infile)
    logging.info('max_pn: ' + str(max_pn))
    split_spec = eval_del_exp(max_pn, expression)
    logging.info('expression is evaluated to: ' + ints2str(split_spec))
    if(len(split_spec) == 0):
        if(outfile != infile):
            shutil.copyfile(infile, outfile)
    else:
        sizes = get_pages_size(infile)
        pages = split(infile)
        assert(max_pn == len(pages))
        pglist = list()
        i = 0
        while(i < max_pn):
            if(i+1 in split_spec): 
                width, height = sizes[i]
                if(width>=height):
                    is_portrait = False
                    size1 = '0 0 %fpts 0' % (width/2) # left, top, right, bottom
                    size2 = '%fpts 0 0 0' % (width/2)
                else:
                    is_portrait = True
                    size1 = '0 0 0 %fpts' % (height/2)
                    size2 = '0 %fpts 0 0' % (height/2)
                tmp_page1 = pages[i] + '.tmp1.pdf'
                tmp_page2 = pages[i] + '.tmp2.pdf'
                getstatusoutput(['pdfjam', '--trim',  size1, '--outfile', tmp_page1, pages[i]])
                getstatusoutput(['pdfjam', '--trim',  size2, '--outfile', tmp_page2, pages[i]])
                pglist.append(tmp_page1)
                pglist.append(tmp_page2)
            else:
                pglist.append(pages[i])
            i += 1
        merge(pglist, outfile)

'''Resize all pages one by one.'''
def op_resize(infile, outfile, expression):
    assert(expression!=None)
    # WARNNING: pdfjam requires the "paper" suffix in the name. Otherwise treat both "a4" and "a5" as us letter.
    if(re.match(patt_paper, expression) == None):
        raise Exception('unsupported paper size %s.' %expression)
    sizes = get_pages_size(infile)
    same_size = is_same_size(sizes)
    is_portrait = get_pages_orientation(sizes)
    max_pn = len(sizes)
    logging.info('max_pn: ' + str(max_pn))
    if(same_size):
        cmd = ['pdfjam', '--paper', expression, '--outfile', outfile, infile]
        if(not is_portrait):
            cmd.append('--landscape')
        getstatusoutput(cmd)
        return
    for i in range(0, max_pn):
        cmd = ['pdfjam', '--paper', expression, '--outfile', pg_path(i+1), infile, str(i+1)]
        if(not is_portrait):
            cmd.append('--landscape')
        getstatusoutput(cmd)
    cmd = ['pdfjam', '--noautoscale', 'true', '--outfile', outfile]
    if(not is_portrait):
        cmd.append('--landscape')
    for i in range(0, max_pn):
        cmd.append(pg_path(i+1))
    getstatusoutput(cmd)

'''Scale the page content to fullfile page.'''
def op_scale(infile, outfile, expression):
    assert(expression!=None)
    logging.info('scale_exp: ' + expression)
    tokens = expression.split(',')
    ratioX, ratioY = float(tokens[0]), float(tokens[1])
    # Why "-dFIXEDMEDIA -sPAPERSIZE=a4" doesn't work? http://stackoverflow.com/questions/7446552/resizing-a-pdf-using-ghostscript
    #gs -dNOPAUSE -dBATCH -dSAFER -dCompatibilityLevel="1.3" -dPDFSETTINGS="/printer" -dSubsetFonts=true -dEmbedAllFonts=true -sDEVICE=pdfwrite -sOutputFile="out.pdf" -c "<</BeginPage{0.9 0.9 scale 29.75 42.1 translate}>> setpagedevice" -f /home/zhichyu/tmp/A.pdf
    sizes = get_pages_size(infile)
    same_size = is_same_size(sizes)
    if(not same_size):
        raise('The scale operation requires all pages be in the same size!')
    cmd = 'gs -dNOPAUSE -dBATCH -dSAFER -dCompatibilityLevel="1.3" -dPDFSETTINGS="/printer" -dSubsetFonts=true -dEmbedAllFonts=true -sDEVICE=pdfwrite -sOutputFile="%s"' % outfile
    (width, height) = sizes[0]
    # gs scales and moves per the left-bottom. pdfjam scales per the center, and moves per the left-bottom.
    offsetX = (1 - ratioX) * 0.5 * width
    offsetY = (1 - ratioY) * 0.5 * height
    cmd += ' -c "<</BeginPage{%f %f scale %f %f translate}>> setpagedevice" -f "%s"'%(ratioX, ratioY, offsetX, offsetY, infile)
    getstatusoutput(cmd)

def operate(infile, outfile, op, exp):
    # clean up temp directory
    pages = sorted(pg_paths(), key=pg_num)
    for pg_fp in pages:
        os.unlink(pg_fp)
    if(op=='add'):
        op_add(infile, outfile, exp)
    elif(op=='delete'):
        op_delete(infile, outfile, exp)
    elif(op=='move'):
        op_move(infile, outfile, exp)
    elif(op=='rotate'):
        op_rotate(infile, outfile, exp)
    elif(op=='join'):
        op_join(infile, outfile, exp)
    elif(op=='split'):
        op_split(infile, outfile, exp)
    elif(op=='resize'):
        op_resize(infile, outfile, exp)
    elif(op=='scale'):
        op_scale(infile, outfile, exp)
    else:
        assert(0)

def main():
    usage = '''Edit a pdf file for better printing.
shuffe operations:
add: add blank pages per expression "sub_exp[,sub_exp]*[@n_range]". sub_exp format is "f(n):g(n)". Both f(n) and g(n) are Python expressions of variable n, such as "12*n". Earlier sub_exp precedes over later ones, so they are not swapable. If n_range is not specified, it's default to "0-N" when N is the number of panges plus one. The format of n_range is "sub_range[,sub_range]*". Each sub_range is an integer or an interger pair splited with "-". Example 1: "5:1" means inserting a blank page just before page 5. Example 2: "5*n+1:2" means insert 2 blank pages just before page 1.6.11.16... Example 3: "5*n+1:2@0,2" is equavalent to "1:2,11,2".
delete: delete pages per expression "sub_exp[,sub_exp]*[@n_range]". The expression is a Python expression on variable n, such as "12*n". Example 1: "1,12*n+11,12*n+12" means deleting pages in the set {1, 12n+11, 12n+12 | integer n>=0}. The n_range usage is the same to the add operation.
move: move pages per expression. The expression format is the same to add with following semantic: earlier sub_exp precedes over later ones. Example 1: "5:1" means moving page 5 to just before page 1. Example 2: "5*n+5:5*n+1,5*n+4:5*n+1" means reorder all pages per 5n+5.5n+4.5n+1.5n+2.5n+3. Example 3: "5*n+4:5*n+1,5*n+5:5*n+1" means reorder all pages per 5n+4.5n+5.5n+1.5n+2.5n+3.

in-page edit operations:
rotate: rotate left (counter-clockwise) pages per an expression. The expression format is the same to delete.
join: join a page with the next one per an expression. The expression is the same to delete.
split: split a page into two parts per an expression. The expression is the same to delete.

page & content size operations:
resize: resize all pages one by one. pdfjam and printers resize all pages per the first page. This cause a disaster if pages are in different sizes. Supported sizes are: aNpaper, where N is an integer in [1,6]
scale: scale all pages' content, a.k.a change the margins of PDF file while keeping the physical page size the same. expression is: ratioX,ratioY.
'''
    parser = argparse.ArgumentParser(description=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-o', '--outfile', metavar='outfile', default=None, help='destination file or directory, edit inplace if not specified')
    parser.add_argument('infile', metavar='infile', help='source PDF file')
    subparsers = parser.add_subparsers(dest='op', help='sub-command help')
    supported_ops = ['add', 'delete', 'move', 'rotate', 'join', 'split', 'resize', 'scale']
    for op in supported_ops:
        subparser = subparsers.add_parser(op, help='help info of %s'%op)
        subparser.add_argument('exp')
    args = parser.parse_args()

    infile = os.path.abspath(args.infile)
    if(not os.path.isfile(infile)):
        print('infile is not a file: %s' % infile)
        return
    if(args.outfile):
        outfile = os.path.abspath(args.outfile)
        if(os.path.isdir(outfile)):
            outfile = os.path.join(outfile, os.path.basename(infile))
    else:
        outfile = infile

    if(args.op):
        if(args.op not in supported_ops):
            parser.error('operation not supported!')
        if(not args.exp):
            parser.error('expression is missing!')

    logFile = '/tmp/pdf_shuffer.log'
    # set up logging to file. Several traps here:
    # 1. If any loging.info(...) is invoked before logging.basicConfig(logFile), the logFile will not be created!
    # 2. If multiple scripts invokes logging.basicConfig(logFile), the logFile will be truncated!
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(message)s', filename=logFile, filemode='w')

    if(args.op):
        try:
            operate(infile, outfile, args.op, args.exp)
        except Exception as e:
            print(traceback.format_exc())
            print('Error: the above operation failed. The output file could be corrupt!')
    else:
        #interactive mode. Refers to http://pymotw.com/2/readline/.
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode emacs')
        special_ops = ['help', 'quit', 'exit']
        all_ops = supported_ops + special_ops
        print('type "help" for help, "quit" or "exit" to quit')
        prompt = '[op exp] '
        while(True):
            line = input(prompt)
            line = line.strip()
            tokens = line.split()
            if(not tokens or (not tokens[0] in all_ops) or tokens[0]=='help'):
                print(usage)
            elif(tokens[0] in ['quit', 'exit']):
                break
            elif(len(tokens) != 2):
                print(usage)
            else:
                try:
                    operate(infile, outfile, tokens[0], tokens[1])
                    # Only the first op is allowed to customize outfile. Later operations edit the file in place.
                    infile = outfile
                except Exception as e:
                    print(traceback.format_exc())
                    print('Error: the above operation failed. The output file could be corrupt!')
                    break

def test_expressions():
    max_pn = 420
    del_exp = "1,12*n+11,12*n+12@0-3"
    add_exp = "12*n+1:2,12*n+2:1@0,10"
    mov_exp = "12*n+7:12*n+1,12*n+8:12*n+1"
    print('max_pn: ' + str(max_pn))
    print('del_exp: ' + del_exp)
    print('add_exp: ' + add_exp)
    print('mov_exp: ' + mov_exp)
    print('del_exp is evaluated to: ')
    print(eval_del_exp(max_pn, del_exp))
    print('add_exp is evaluated to: ')
    print(eval_add_exp(max_pn, add_exp))
    print('mov_exp is evaluated to: ')
    print(eval_mov_exp(max_pn, mov_exp))
    import sys
    sys.exit()

if __name__ == '__main__':
    #test_expressions()
    main()

