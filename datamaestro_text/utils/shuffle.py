# Copyright (c) 2016 Salle, Alexandre <atsalle@inf.ufrgs.br>
# Author: Salle, Alexandre <atsalle@inf.ufrgs.br>
# Modified: Benjamin Piwowarski <b@piwowarski.fr>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import tempfile
import random
import logging
from typing import TextIO

# need better way to estimate this given overhead for str. setting to
# 0.5GB uses rougly 4GB of ram.
MEMORY = int(float(os.environ.get("MEMORY", 4.0)) / 8 * 1024 ** 3)


def shuffle_and_close(buf, f):
    random.shuffle(buf)
    f.writelines(buf)
    f.close()


def shuffle(input, output: TextIO, memory=MEMORY):
    """Shuffle using temporary file
    """
    files = []
    files.append(tempfile.NamedTemporaryFile(mode="w", delete=False))
    total_bytes = 0
    total_lines = 0
    buf = []
    bytes_used = 0

    for line in input:
        bytes_used += len(line)
        total_bytes += len(line)
        total_lines += 1
        buf.append(line)
        if bytes_used >= memory:
            shuffle_and_close(buf, files[-1])
            files.append(tempfile.NamedTemporaryFile(mode="w", delete=False))
            buf = []
            bytes_used = 0
    if buf:
        shuffle_and_close(buf, files[-1])

    buf = []
    avg_bytes_per_line = total_bytes / float(total_lines)
    logging.info("Output from %d temporary files", len(files))
    files = [open(f.name) for f in files]
    while files:
        rm_files = []
        lines_per_file = int((memory / avg_bytes_per_line) / len(files))
        for f in files:
            lines = f.readlines(lines_per_file)
            if not lines:
                rm_files.append(f)
            buf += lines
        random.shuffle(buf)
        output.writelines(buf)
        buf = []
        for f in rm_files:
            files.remove(f)
            os.unlink(f.name)
