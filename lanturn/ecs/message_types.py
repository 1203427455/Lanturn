from lib.enum import enum

MESSAGE_TYPE = enum(
    'CREATE_ENTITY',
    'CLIENT_CONNECT',
    'CREATE_BATTLE',
    'PLAYER_BATTLE_MOVE'
)
