import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "":
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


main()
