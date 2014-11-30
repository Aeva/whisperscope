
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


from common import CommentBlock


def parse_comments(file_path, CommentType=CommentBlock):
    """
    This method reads in a javascript file and parses out what it
    thinks are the comment lines.  It returns a list of CommentBlock
    instances.
    """
    with open(file_path, "r") as file_ob:
        lines = file_ob.readlines()
    
    comments = []
    builder = None
    line_num = 0
    
    for raw_line in lines:
        line_num += 1
        line = raw_line.strip()
        
        if builder and builder._multiline_notation:
            # we are currently within a multiline comment block
            if line.count("*/"):
                # we reached the end of a multiline comment block
                cut = line.index("*/")
                builder.add_line(line[:cut])
                comments.append(builder)
                builder = None
                continue
            else:
                builder.add_line(line)
        else:
            if not builder and line.startswith("/*"):
                # we are in the beginning of a multiline comment block
                builder = CommentType(file_path, line_num, True)
                builder.add_line(line)
                if line.count("*/"):
                    # single line comment
                    comments.append(builder)
                    builder = None
                continue
            else:
                if builder and not builder._multiline_notation:
                    # the current builder comment is not a multiline block
                    if line.startswith("//"):
                        builder.add_line(line)
                        continue
                    else:
                        # we reached the end of sequential single line comments
                        comments.append(builder)
                        builder = None
                        continue
                elif line.startswith("//"):
                    # the beginning of a block made up of single line comments
                    # or maybe just a singular single line comment
                    builder = CommentType(file_path, line_num, False)
                    builder.add_line(line)
                    continue

    if builder and builder._multiline_notation:
        msg = "Unterminated multiline comment in file {0} on line {1}"
        raise AssertionError(msg.format(file_path, builder.line_number))
    
    else:
        return comments
