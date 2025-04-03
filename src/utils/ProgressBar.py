# progress_bar.py
from typing import Dict
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.style import Style


class ProgressBar:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.status = "pending"
        self.message = ""

    def set_status(self, status: str, message: str = ""):
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

    def update(self, task_name: str, status: str, message: str = ""):
        if task_name not in self.tasks:
            self.tasks[task_name] = ProgressBar(task_name)
        self.tasks[task_name].set_status(status, message)
        self._refresh()

    def _refresh(self):
        self.table.columns.clear()
        self.table.add_column()
        self.table.rows.clear()

        for task in self.tasks.values():
            status_text = Text()

            if task.status == "done":
                icon = "✓"
                style = Style(color="green", bold=True)
            elif task.status == "error":
                icon = "✗"
                style = Style(color="red", bold=True)
            elif task.status == "working":
                icon = "⋯"
                style = Style(color="blue")
            else:
                icon = "-"
                style = Style(color="white")

            status_text.append(f"{icon} ", style=style)
            status_text.append(f"{task.task_name:<25}", style=Style(bold=True))
            if task.message:
                status_text.append(f"{task.message}", style=style)

            self.table.add_row(status_text)
progress = MultiProgressBar()
