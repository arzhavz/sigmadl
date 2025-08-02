# -*- coding: utf-8 -*-
from rich.progress import TextColumn

class HumanSizeColumn(TextColumn):
    """Custom column that displays file sizes in human-readable format"""
    def __init__(self):
        super().__init__("{task.completed}") 
    
    def render(self, task):
        completed = task.completed or 0
        total = task.total or 0
        def fmt(sz):
            if sz < 1024:
                return f"{sz} B"
            elif sz < 1024 * 1024:
                return f"{sz/1024:.1f} KB"
            else:
                return f"{sz/(1024*1024):.2f} MB"
        return f"[progress.completed][bright_black]{fmt(completed)} / {fmt(total)}[/]"