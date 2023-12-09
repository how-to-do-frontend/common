
from ..constants import ClientStatus, GameMode, Mods
from ..objects import bStatusUpdate

from typing import Optional
from copy import copy

import app

def update(player_id: int, status: bStatusUpdate, client_hash: str) -> None:
    app.session.redis.hset(
        f'bancho:status:{player_id}',
        'hash', client_hash
    )

    status = copy(status)

    status.action = status.action.value
    status.mode = status.mode.value
    status.mods = status.mods.value

    for key in status.__dataclass_fields__.keys():
        app.session.redis.hset(
            f'bancho:status:{player_id}',
            key, getattr(status, key)
        )

def get(player_id: int) -> Optional[bStatusUpdate]:
    status = app.session.redis.hgetall(
        f'bancho:status:{player_id}'
    )

    if not status:
        return

    return bStatusUpdate(
        action=ClientStatus(int(status[b'action'])),
        mode=GameMode(int(status[b'mode'])),
        mods=Mods(int(status[b'mods'])),
        beatmap_id=int(status[b'beatmap_id']),
        beatmap_checksum=status[b'beatmap_checksum'],
        text=status[b'text'].decode(),
    )

def client_hash(player_id: int) -> Optional[str]:
    hash = app.session.redis.hget(
        f'bancho:status:{player_id}',
        'hash'
    )

    if not hash:
        return

    return hash.decode()

def delete(player_id: int) -> None:
    app.session.redis.hdel(
        f'bancho:status:{player_id}',
        'action', 'mode', 'mods', 'text', 'beatmap_id', 'beatmap_checksum', 'hash'
    )

def exists(player_id: int) -> bool:
    return app.session.redis.exists(
        f'bancho:status:{player_id}'
    )
