# -*- coding: utf-8 -*-
# author: Roman Kharitonov, refaim.vl@gmail.com

import sys

from common import bytes_to_human

class ProgressBar(object):
    def __init__(self, maxval, fout=sys.stderr, width=50, displaysize=False, enabled=True):
        self.curval, self.maxval = 0, maxval
        self.fout = fout
        self.width = width
        self.displaysize = displaysize
        self.enabled = enabled

    def update(self, value):
        assert value <= self.maxval
        assert (self.curval + value) <= self.maxval
        self.curval += value
        self._write()

    def set(self, value):
        assert value <= self.maxval
        self.curval = value
        self._write()

    def start(self):
        self.set(0)

    def finish(self):
        if self.curval != self.maxval:
            self.set(self.maxval)

    def _getbarstr(self):
        return (u'=' * int(self.percentage() * (self.width / 100.0))
                + u'>').ljust(self.width)

    def _getsizestr(self):
        fmt = u'[{cur} / {max}]'
        return fmt.format(
            cur = bytes_to_human(self.curval),
            max = bytes_to_human(self.maxval))

    def _write(self):
        if not self.enabled:
            return
        line = u'[{bar}] {prc}%'.format(
            bar = self._getbarstr(),
            prc = self.percentage()
            )
        if self.displaysize:
            line = u'{main} {size}'.format(
                main = line,
                size = self._getsizestr()
                )

        if self.curval == self.maxval:
            suffix = u'\n'
        else:
            suffix = u'\r'

        self.fout.write((line.ljust(max(len(line), 79)) + suffix).encode(self.fout.encoding))
        self.fout.flush()

    def percentage(self):
        return int(self.curval / float(self.maxval) * 100.0)

    def clear(self):
        '(Temporarily) clear progress bar off screen, e.g. to write log line.'
        if not self.enabled:
            return
        self.fout.write(' ' * 79 + '\r')
        self.fout.flush()

class ProgressBarSafeLogger(object):
    'Wraps logger to clear progress bar before logging something.'
    def __init__(self, log, pbar=None):
        self.log = log
        self.pbar = pbar

    def set_pbar(self, pbar):
        self.pbar = pbar

    def debug(self, *args, **kw):
        self.pbar.clear()
        self.log.debug(*args, **kw)

    def info(self, *args, **kw):
        self.pbar.clear()
        self.log.info(*args, **kw)

    def warning(self, *args, **kw):
        self.pbar.clear()
        self.warning.info(*args, **kw)

    def error(self, *args, **kw):
        self.pbar.clear()
        self.error.info(*args, **kw)
