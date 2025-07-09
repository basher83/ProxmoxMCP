"""
Reusable UI components for Proxmox MCP output.
"""

from typing import List, Optional

from .colors import ProxmoxColors
from .theme import ProxmoxTheme


class ProxmoxComponents:
    """Reusable UI components for formatted output."""

    @staticmethod
    def _calculate_column_widths(
        headers: List[str], rows: List[List[str]]
    ) -> List[int]:
        widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                max_line_length = max(len(line) for line in str(cell).split("\n"))
                widths[i] = max(widths[i], max_line_length)
        return widths

    @staticmethod
    def _build_title_section(title: str, total_width: int) -> List[str]:
        title_str = ProxmoxColors.colorize(
            title, ProxmoxColors.CYAN, ProxmoxColors.BOLD
        )
        padding = (total_width - len(title) - 2) // 2
        title_separator = "+" + "-" * (total_width - 2) + "+"
        return [
            title_separator,
            "|"
            + " " * padding
            + title_str
            + " " * (total_width - padding - len(title) - 2)
            + "|",
            title_separator,
        ]

    @staticmethod
    def _build_table_headers(headers: List[str], widths: List[int]) -> List[str]:
        separator = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        header = (
            "|"
            + "|".join(
                f" {ProxmoxColors.colorize(h, ProxmoxColors.CYAN):<{w}} "
                for h, w in zip(headers, widths)
            )
            + "|"
        )
        return [separator, header, separator]

    @staticmethod
    def _format_row_lines(row: List[str], widths: List[int]) -> List[str]:
        row_cell_lines = [str(cell).split("\n") for cell in row]
        max_lines = max(len(lines) for lines in row_cell_lines)
        padded_cells = [
            lines + [""] * (max_lines - len(lines)) for lines in row_cell_lines
        ]

        lines = []
        for i in range(max_lines):
            line_parts = [
                f" {padded_cells[col_idx][i]:<{widths[col_idx]}} "
                for col_idx in range(len(widths))
            ]
            lines.append("|" + "|".join(line_parts) + "|")
        return lines

    @staticmethod
    def create_table(
        headers: List[str], rows: List[List[str]], title: Optional[str] = None
    ) -> str:
        widths = ProxmoxComponents._calculate_column_widths(headers, rows)
        total_width = sum(widths) + len(widths) + 1
        separator = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

        result = []
        if title:
            result.extend(ProxmoxComponents._build_title_section(title, total_width))

        result.extend(ProxmoxComponents._build_table_headers(headers, widths))

        for idx, row in enumerate(rows):
            result.extend(ProxmoxComponents._format_row_lines(row, widths))
            if idx < len(rows) - 1:
                result.append(separator)

        result.append(separator)
        return "\n".join(result)

    @staticmethod
    def create_progress_bar(value: float, total: float, width: int = 20) -> str:
        """Create a progress bar with percentage.

        Args:
            value: Current value
            total: Maximum value
            width: Width of progress bar in characters

        Returns:
            Formatted progress bar string
        """
        percentage = min(100, (value / total * 100) if total > 0 else 0)
        filled = int(width * percentage / 100)
        color = ProxmoxColors.metric_color(percentage)

        bar = "█" * filled + "░" * (width - filled)
        return f"{ProxmoxColors.colorize(bar, color)} {percentage:.1f}%"

    @staticmethod
    def create_resource_usage(used: float, total: float, label: str, emoji: str) -> str:
        """Create a resource usage display with progress bar.

        Args:
            used: Used amount
            total: Total amount
            label: Resource label
            emoji: Resource emoji

        Returns:
            Formatted resource usage string
        """
        from .formatters import ProxmoxFormatters

        (used / total * 100) if total > 0 else 0
        progress = ProxmoxComponents.create_progress_bar(used, total)

        return (
            f"{emoji} {label}:\n"
            f"  {progress}\n"
            f"  {ProxmoxFormatters.format_bytes(int(used))} / "
            f"{ProxmoxFormatters.format_bytes(int(total))}"
        )

    @staticmethod
    def create_key_value_grid(data: dict, columns: int = 2) -> str:
        """Create a grid of key-value pairs.

        Args:
            data: Dictionary of key-value pairs
            columns: Number of columns in grid

        Returns:
            Formatted grid string
        """
        # Calculate max widths for each column
        items = list(data.items())
        rows = [items[i : i + columns] for i in range(0, len(items), columns)]

        key_widths = [0] * columns
        val_widths = [0] * columns

        for row in rows:
            for i, (key, val) in enumerate(row):
                key_widths[i] = max(key_widths[i], len(str(key)))
                val_widths[i] = max(val_widths[i], len(str(val)))

        # Format rows
        result = []
        for row in rows:
            formatted_items = []
            for i, (key, val) in enumerate(row):
                key_str = ProxmoxColors.colorize(f"{key}:", ProxmoxColors.CYAN)
                formatted_items.append(
                    f"{key_str:<{key_widths[i] + 10}} {val:<{val_widths[i]}}"
                )
            result.append("  ".join(formatted_items))

        return "\n".join(result)

    @staticmethod
    def create_status_badge(status: str) -> str:
        """Create a status badge with emoji.

        Args:
            status: Status string

        Returns:
            Formatted status badge string
        """
        status = status.lower()
        emoji = ProxmoxTheme.get_status_emoji(status)
        return f"{emoji} {status.upper()}"
