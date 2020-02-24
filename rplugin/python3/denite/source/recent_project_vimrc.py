from my_project_opener import RecentVimrcsFile
from pathlib import Path
from .base import Base
from ..kind.file import Kind as File

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'recent_project_vimrc'
        self.kind = Kind(vim)
        self.default_action = 'source'

    def on_init(self, context):
        pass

    def highlight(self):
        pass

    def define_syntax(self):
        pass

    def gather_candidates(self, context):
        project_vimrc_path = \
            self.vim.eval('g:my_project_opener_recent_project_vimrc_file')
        recent_vimrc_files = \
            RecentVimrcsFile.for_reading(Path(project_vimrc_path))

        # Sort by most recent first when showing
        lines = reversed(recent_vimrc_files.read())
        return [{ "word": path } for path in lines]

class Kind(File):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'project_vimrc'

    def action_source(self, context):
        path = context['targets'][0]['word']
        self.vim.call('MyProjectOpenerSource', path)
