import asyncio
import logging


class PrintException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


async def get_command(file_path, copies, mode):
    return " ".join(["lp", file_path, "-o", "sides", mode, "-n", copies])


async def print_file(file_path: str, copies: str, mode: str):
    proc = await asyncio.create_subprocess_shell(
        await get_command(file_path, copies, mode),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stderr:
        raise PrintException(stderr.decode())
