from lib.enum import enum

MESSAGE_TYPE = enum(
    'CREATE_ENTITY',
    'DESTROY_ENTITY',
    'MOVE_ENTITY',
    'INIT_MOVEMENT_PLANNER',
    'JUMPED',
    'LANDED',
    'AIRBORNE',
    'COLLISION',
    'QUAD_TREE',
    'CLIENT_CONNECT',
)
