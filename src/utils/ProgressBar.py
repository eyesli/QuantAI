# progress_bar.py
from typing import Dict
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.style import Style
from enum import Enum, auto

from utils.InvestmentStrategy import InvestmentStrategy


class ProgressStatus(Enum):
    PENDING = auto()    # 等待中
    WORKING = auto()    # 工作中
    DONE = auto()       # 完成
    ERROR = auto()      # 错误

class ProgressBar:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.status = ProgressStatus.PENDING
        self.message = ""

    def set_status(self, status: ProgressStatus, message: str = ""):
        self.status = status
        self.message = message

class MultiProgressBar:
    def __init__(self):
        self.console = Console()
        self.tasks: Dict[str, ProgressBar] = {}
        self.table = Table(show_header=False, box=None)
        self.live = Live(self.table, console=self.console, refresh_per_second=5)
        self.started = False

    def start(self):
        if not self.started:
            self.live.start()
            self.started = True

    def stop(self):
        if self.started:
            self.live.stop()
            self.started = False

    def update(self, task_name: InvestmentStrategy, status: ProgressStatus, message: str = ""):
        if task_name not in self.tasks:
            self.tasks[task_name.english] = ProgressBar(task_name.english)
        self.tasks[task_name.english].set_status(status, message)
        self._refresh()

    def _refresh(self):
        self.table.columns.clear()
        self.table.add_column()
        self.table.rows.clear()

        for task in self.tasks.values():
            status_text = Text()

            if task.status == ProgressStatus.DONE:
                icon = "✓"
                style = Style(color="green", bold=True)
            elif task.status == ProgressStatus.ERROR:
                icon = "✗"
                style = Style(color="red", bold=True)
            elif task.status == ProgressStatus.WORKING:
                icon = "⋯"
                style = Style(color="blue")
            else:  # PENDING
                icon = "-"
                style = Style(color="white")

            status_text.append(f"{icon} ", style=style)
            status_text.append(f"{task.task_name:<25}", style=Style(bold=True))
            if task.message:
                status_text.append(f" {task.message}", style=style)

            self.table.add_row(status_text)

progress = MultiProgressBar()
