import pynvim

from collections import deque
from pathlib import Path

@pynvim.plugin
class MyProjectOpener(object):

    def __init__(self, vim):
        self.vim = vim

    @pynvim.function('MyProjectOpenerSource')
    def source(self, args):
        vimrc_path_full = Path(args[0]).expanduser().resolve()

        self.vim.command('cd ' + str(vimrc_path_full.parent))
        self.vim.command('source ' + str(vimrc_path_full))

        recent_vimrc_path = \
                Path(self.vim.eval('g:my_project_opener_recent_project_vimrc_file'))
        recent_vimrc_count = \
                self.vim.eval('g:my_project_opener_recent_project_vimrc_max_projects')
        RecentVimrcsFile(recent_vimrc_path, recent_vimrc_count).add(vimrc_path_full)


class RecentVimrcsFile(object):

    def __init__(self, path, max_count):
        self.path = path
        self.max_count = max_count

    def read(self):
        if self.path.exists():
            with self.path.open(encoding='utf-8') as f:
                return f.read().strip().splitlines()
        else:
            return []

    def add(self, new_path):
        recent_project_vimrcs = self.read()
        recent_project_vimrcs.append(str(new_path))
        new_recent_project_vimrcs = \
                sorted(set(recent_project_vimrcs), key=recent_project_vimrcs.index)

        if len(new_recent_project_vimrcs) > self.max_count:
            del new_recent_project_vimrcs[0]

        with self.path.open('w', encoding='utf-8') as f:
            f.writelines('\n'.join(new_recent_project_vimrcs))

    @classmethod
    def for_reading(cls, path):
        # max_count is unnecessary only for reading
        return cls(path, None)
