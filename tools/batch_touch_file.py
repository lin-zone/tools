import re
import os

from gooey import Gooey, GooeyParser


range_re = re.compile('{(\d+),\s*(\d+)}')


def gen_filenames(filename):
    m = re.search(range_re, filename)
    if m:
        start, stop = map(int, m.groups())
        filename_fmt = re.sub(range_re, '{}', filename)
        for i in range(start, stop + 1):
            yield filename_fmt.format(i)
    else:
        yield filename


def touch(folder, filename):
    for name in gen_filenames(filename):
        open(os.path.join(folder, name), 'w').close()


@Gooey(
    program_name="批量生成文件",
    language="Chinese",
)
def main():
    parser = GooeyParser()
    parser.add_argument("folder", widget="DirChooser", metavar="选择目录")
    parser.add_argument("filename", metavar="文件名")
    args = parser.parse_args()
    touch(args.folder, args.filename)


if __name__ == "__main__":
    main()
