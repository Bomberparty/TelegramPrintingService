import asyncio
import logging
from database import SidesCount


class PrintException(Exception):
    """Some printing errors"""


async def get_command(file_path, copies: int, mode: str):
    return " ".join(["lp", file_path, "-o", f"sides={mode}", "-n", str(copies)])


async def print_file(file_path: str, copies: int, mode: str):
    proc = await asyncio.create_subprocess_shell(
        await get_command(file_path, copies, mode),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(stdout, stdout)
    if stderr:
        raise PrintException(stderr.decode())
