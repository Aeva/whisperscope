
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


class CommentBlock(object):
    """
    Represents a javascript comment block.
    """

    def __init__(self, file_name, line_number, multiline_notation):
        self._multiline_notation = multiline_notation
        self.file_name = file_name
        self.line_number = line_number
        self.lines = []

    def __repr__(self):
        return "<CommentBlock {0} line {1}>".format(
            os.path.basename(self.file_name),
            self.line_number)
    
    @property
    def text(self):
        return "\n".join(self.lines)

    def add_line(self, line):
        cleaned = self._clean(line)
        if cleaned:
            self.lines.append(cleaned)
        else:
            self.lines.append("")

    def _clean(self, line):
        if self._multiline_notation:
            return self._clean_multline(line)
        else:
            return self._clean_consequtive(line)

    def _clean_multline(self, line):
        """
        Scrub cruft from comments in multiline notation.
        """
        if len(self.lines) == 0:
            line = line[line.index("/*")+2:].strip()
        
        # strip off random crap at the beginning and end of the line
        line = re.sub(r'^[\s\*]*', '', line)
        line = re.sub(r'[\s\*]*$', '', line)
        line = line.strip()
        return line

    def _clean_consequtive(self, line):
        """
        Scrub cruft from single line comments.
        """
        return line[line.index("//")+2:].strip()
