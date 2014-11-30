
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


import re
import glob
import os.path
import argparse

from sh import pandoc, echo

from common import CommentBlock
from comment_parser import parse_comments


def md_to_rst(markdown_text):
    """
    Convert a string containing markdown to restructured text.
    """
    cmd = pandoc(echo(markdown_text), "--from", "markdown", "--to", "rst")
    return cmd.stdout


def indent(text, amount=4):
    """
    Prepends "    "s to all lines in a multiline block of text.
    """
    return "\n".join([" "*amount + line for line in text.split("\n")])


def header(text, underline="="):
    """
    An rst header of some variety.
    """
    _text = text.strip()
    repeat = len(text) / len(underline)
    assert repeat > 0
    return "{0}\n{1}\n".format(_text, underline * repeat)


def toctree(lines):
    """
    Creates an rst toctree.
    """
    body = [":maxdepth: 2", ""] + lines
    text = ".. toctree::" + indent("\n".join(body)) + "\n"
    return text


class DocumentationComment(CommentBlock):
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
        hint = self.lines[0][self.lines[0].index("[+]")+3:].strip()
        body = "\n".join(self.lines[1:])

        rst = ""
        if hint:
            name = hint
            options = ""
            if hint.count("("):
                name = hint[:hint.index("(")]
                options = hint[hint.index("("):]

            # FIXME: escape asterisks
            title = "*{0}* __{1}__\n\n".format(name, options)

            rst += header(name, "-")
            rst += md_to_rst(title + body)

        else:
            rst = md_to_rst(body)+"\n\n"

        return rst


class DocumentationPage(object):
    """
    Represents a page of documentation.
    """

    def __init__(self, src_path):
        comments = parse_comments(src_path, DocumentationComment)
        file_name = os.path.basename(src_path)
        self.comments = [c for c in comments if c.flagged()]
        self.src_path = file_name
        self.doc_path = ".".join(file_name.split(".")[:-1]+["rst"])
        self.title = file_name

    def __repr__(self):
        return "<DocumentPage {0}>".format(self.title)        

    def to_rst(self):
        output = "\n\n" + header(self.title) + "\n"
        for comment in self.comments:
            output += comment.process() + "\n\n"
        return output


def export_to_sphinx():
    """
    Commandline tool for generating JavaScript reference pages for
    Sphinx.
    """

    bio = """
    This is a tool for generating Sphinx reference pages for python
    projects.
    """

    parser = argparse.ArgumentParser(description = bio)
    parser.add_argument(
        "src_path", type=str, nargs="+",
        help="Path for JavaScript file or files to be documented.")
    parser.add_argument(
        "doc_path", type=str, nargs=1,
        help="The directory for which the output will be saved within.")
    args = parser.parse_args()
    
    src_paths = list(args.src_path)
    sources = []
    for path in src_paths:
        if os.path.isdir(path):
            sources += glob.glob(os.path.join(path, "*.js"))
        else:
            sources.append(path)
    # source files to be consumed:
    sources = [s for s in sources if os.path.isfile(s)]

    # directory where we will be saving the output:
    out_path = args.doc_path[0]

    if not os.path.isdir(out_path):
        print "Output directory does not exist!"
        exit(0)

    if not len(sources):
        print "No files to parse...?"
        exit(0)

    # save documentation pages
    pages = []
    for in_path in sources:
        page = DocumentationPage(in_path)
        if len(page.comments):
            pages.append(page)
            with open(os.path.join(out_path, page.doc_path), "w") as out_file:
                out_file.write(page.to_rst())

    # save documentation index
    tree = toctree([p.doc_path for p in pages])
    index_page = "\n\n" + header("API Reference") + "\n" + tree
    with open(os.path.join(out_path, "index.rst"), "w") as out_file:
        out_file.write(index_page)
