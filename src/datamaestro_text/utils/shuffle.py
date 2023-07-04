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
from pathlib import Path
import atexit
import numpy
import logging
from typing import TextIO, Optional, List

# Use 1GB
MEMORY = 1024**3


def shuffle_and_close(random, buf, f):
    random.shuffle(buf)
    f.writelines(buf)
    f.close()


def add_temporary_file(tmp_path: Path, files: List, rm_files: List[str]):
    tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=tmp_path)
    logging.info("Adding temporary file %s", tmp_file.name)
    files.append(tmp_file)
    rm_files.append(tmp_file.name)


def shuffle(
    input,
    output: TextIO,
    *,
    memory=MEMORY,
    random=None,
    tmp_path: Optional[Path] = None
):
    """Shuffle using temporary file"""
    if random is None:
        random = numpy.random.RandomState()
    files = []

    # --- Files to remove
    rm_files = []

    def remove_files():
        logging.info("Removing files")
        for path in rm_files:
            if os.path.exists(path):
                os.unlink(path)

    # In case of crash, remove the files
    atexit.register(remove_files)

    # Let's go
    add_temporary_file(tmp_path, files, rm_files)
    total_bytes = 0
    total_lines = 0
    buf = []
    bytes_used = 0

    # Create the temporary files
    for line in input:
        bytes_used += len(line)
        total_bytes += len(line)
        total_lines += 1
        buf.append(line)
        if bytes_used >= memory:
            shuffle_and_close(random, buf, files[-1])
            add_temporary_file(tmp_path, files, rm_files)

            buf = []
            bytes_used = 0

    if buf:
        shuffle_and_close(random, buf, files[-1])

    buf = []
    avg_bytes_per_line = total_bytes / float(total_lines)
    logging.info("Output from %d temporary files", len(files))

    files = [open(f.name) for f in files]
    while files:
        lines_per_file = int((memory / avg_bytes_per_line) / len(files))
        for f in files:
            lines = f.readlines(lines_per_file)
            buf += lines
            if not lines:
                files.remove(f)
                os.unlink(f.name)
                rm_files.remove(f.name)

        random.shuffle(buf)
        output.writelines(buf)
        buf = []

    remove_files()
    atexit.unregister(remove_files)
