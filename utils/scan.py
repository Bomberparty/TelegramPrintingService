import asyncio
import logging
from database import SidesCount
from os import path


class ScanException(Exception):
    """Some printing errors"""


async def get_scan_command(file_path, format_: str) -> str:
    return " ".join(["scanimage", "-o", f"{file_path}.{format_}", "--device",
                     "'airscan:e0:Pantum-M6500W-Series FFFFFF (USB)'",
                     f"--format={format_}"])


async def get_convert_command(old_path, new_path) -> str:
    return " ".join(["convert", old_path, new_path])


async def scan_file(task_id: int, scan_id: int, format_: str) -> str:
    format1 = "png" if format_ == "pdf" else format_
    file_path = path.join("media", "scan", f"{task_id}_{scan_id}.{format_}")


