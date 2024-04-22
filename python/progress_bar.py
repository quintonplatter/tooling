import colorsys
from rich.progress import Progress, BarColumn, Task
from rich.console import Console, RenderableType
from rich.style import Style
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn
)
class RainbowBarColumn(BarColumn):
    def render(self, task: "Task") -> RenderableType:
        "Render a color-changing progress bar."
        # Calculate the completion fraction
        completed = task.completed
        total = task.total
        fraction_complete = completed / total

        # Calculate the hue value across a spectrum (0 to 360)
        hue = int(1440 * fraction_complete) % 360
        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue / 360.0, 0.5, 1)
        # Convert RGB from 0-1 to 0-255
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        # Format into hex color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        final_hex = f"#00cc00"
        
        # Temporarily update the style for this bar
        # Set the color style for the completed part of the bar
        complete_style = Style(color=hex_color)
        # Apply style modifications locally without altering the base class properties
        self.complete_style = complete_style
        self.finished_style = Style(color=final_hex)
        #self.style = hex_color
        return super().render(task)

def custom_progress_bar(iterable, total_size, description="Downloading", rgb=False):
    """
    A custom progress bar which can optionally display a cycling rainbow bar.
    """
    columns = [
        TextColumn("[progress.description]{task.description}"),
        RainbowBarColumn() if rgb else BarColumn(),
        TextColumn("{task.completed} of {task.total}"),
        TransferSpeedColumn(),
        TextColumn("eta"),
        TimeRemainingColumn(),
    ]

    progress = Progress(*columns, refresh_per_second=10)
    task_id = progress.add_task(description, total=total_size)
    try:
        with progress:
            for item in iterable:
                yield item
                progress.update(task_id, advance=1)
    finally:
        progress.stop()

import time

def download_simulation():
    for _ in range(100):
        time.sleep(0.1)
        yield 1

# Example call with the rainbow bar enabled
for _ in custom_progress_bar(download_simulation(), 100, rgb=True):
    pass
