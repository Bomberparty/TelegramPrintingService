from aiogram.filters.base import Filter
from aiogram.types import Message

from loader import admins


class IsAdminFilter(Filter):
    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        return (str(message.from_user.id) in admins) == self.is_admin
