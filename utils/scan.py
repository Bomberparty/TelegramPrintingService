import asyncio
from os import path

from database import Format
from loader import scanner


class ScanException(Exception):
    """Some printing errors"""


class ConvertionException(Exception):
    """Some convertion errors"""


async def get_scan_command(file_path) -> str:
    return " ".join(
        ["scanimage", "-o", f"{file_path}", "--device", scanner, "--format=png"]
    )


async def get_convert_command(old_path, new_path) -> str:
    return " ".join(["convert", old_path, new_path])


async def convert_file(command: str):
    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stderr:
        raise ConvertionException(stderr.decode())


async def scan_file(task_id: int, scan_id: int, format_: Format) -> str:
    path1 = path.join("media", "scan", f"{task_id}_{scan_id}.png")
    path2 = path.join("media", "scan", f"{task_id}_{scan_id}." f"{format_.value}")
    proc = await asyncio.create_subprocess_shell(
        await get_scan_command(path1),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stderr:
        raise ScanException(stderr.decode())
    if format_ == Format.PDF:
        await convert_file(await get_convert_command(path1, path2))
    return path2
