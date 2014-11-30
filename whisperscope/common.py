
# This file is part of Whjsper
#
# Whjsper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Whjsper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Waterworks.  If not, see <http://www.gnu.org/licenses/>.


import os.path
import re


def common_part(lhs, rhs, restrict=[]):
    """
    Returns the number of consequtive characters that are the same
    between two strings, starting from the beginning.

    The restrict parameter allows for only a subset of characters to
    be allowed to be matched.
    """
    if not lhs or not rhs:
        return 0
    max_common = min(len(lhs), len(rhs))
    common = 0
    for i in range(max_common):
        if lhs[i] == rhs[i]:
            if restrict:
                if lhs[i] in restrict:
                    common += 1
                else:
                    break
            else:
                common += 1
        else:
            break
    return common


def find_indentation(lines, restrict=[" ", "\t"]):
    """
    Find the number of characters in from the left hand side for which
    each line is the same.
    """
    indent = 0
    if len(lines) >= 2:
        best = None
        noise = set(restrict)
        for i in range(1, len(lines)-1):
            lhs = lines[i-1]
            rhs = lines[i]
            if set(lhs) == noise.intersection(lhs) \
               or set(rhs) == noise.intersection(rhs):
                # throw out this comparison because one or both of the
                # lines appears to contain only noise
                continue
            elif not lhs or not rhs:
                # throw out this comparison because one or both of the
                # lines is empty
                continue
            else:
                test = common_part(lhs, rhs, noise)
                if best is None or test < best:
                    best = test
        if best:
            indent = best
    return indent


class CommentBlock(object):
    """
    Represents a C-style comment block.
    """

    def __init__(self, file_name, line_number, multiline_notation):
        self._multiline_notation = multiline_notation
        self.file_name = file_name
        self.line_number = line_number
        self._range = 0
        self.lines = []

    def __repr__(self):
        return "<CommentBlock {0} line {1}>".format(
            os.path.basename(self.file_name),
            self.line_number)
    
    @property
    def text(self):
        return "\n".join(self.lines)

    @property
    def end_line(self):
        return self.line_number + self._range

    def add_line(self, line):
        """
        Add a new line of text to this comment.
        """
        self.lines.append(line)
        self._range += 1

    def reflow(self):
        """
        Called to reflow the whitespace at the beginning of the comment
        lines and remove syntatic cruft.
        """

        noise_chars = [" ", "/t"]
        if self._multiline_notation:
            noise_chars.append("*")
            self._reflow_multiline()
        else:
            self._reflow_consequtive()

        cut = find_indentation(self.lines, noise_chars)
        new_lines = []
        omit_blanks = True
        for line in self.lines:
            new_line = line[cut:]
            if not new_line.strip():
                if omit_blanks:
                    continue
                else:
                    new_line = ""
            else:
                omit_blanks = False
            new_lines.append(new_line)
        self.lines = new_lines
        
    def _reflow_multiline(self):
        """
        Strip out syntatic cruft from /* multiline */ comments.
        """
        
        # remove the leading slash from the first line
        first = self.lines[0]
        assert first.startswith("/*")
        self.lines[0] = first[1:]

        # remove last line if it contains nothing
        if not self.lines[-1]:
            self.lines.pop()
        
    def _reflow_consequtive(self):
        """
        Strip out syntatic cruft from consequtive // comments.
        """

        # remove the leading "//" from the lines
        assert self.lines[0].startswith("//")
        self.lines = [line[2:] for line in self.lines]
