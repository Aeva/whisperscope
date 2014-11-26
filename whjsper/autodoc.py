
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

from sh import pandoc, echo

from common import CommentBlock


def md_to_rst(markdown_text):
    """
    Convert a string containing markdown to restructured text.
    """
    cmd = pandoc(echo(markdown_text), "--from", "markdown", "--to", "rst")
    return cmd.stdout


def indent(text):
    """
    Prepends "    "s to all lines in a multiline block of text.
    """
    return "\n".join(["    " + line for line in text.split("\n")])




class Documentation(CommentBlock):
    def __init__(self, *args, **kargs):
        CommentBlock.__init__(self, *args, **kargs)

    def __repr__(self):
        return "<Documentation {0} line {1}>".format(
            os.path.basename(self.file_name),
            self.line_number)
        
    def flagged(self):
        """
        Returns True if this comment is formatted for documentation.
        """
        return len(self.lines) > 1 and self.lines[0].startswith("[+]")

    def process(self):
        """
        Output something useful or interesting.
        """
        header = self.lines[0][self.lines[0].index("[+]")+3:].strip()
        body = "\n".join(self.lines[1:])

        rst = ""
        if header:
            rst = ".. js:function:: {0}\n".format(header)
            rst += indent(md_to_rst(body))
            
        else:
            rst = md_to_rst(body)

        return rst


