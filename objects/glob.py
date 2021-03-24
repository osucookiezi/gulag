# -*- coding: utf-8 -*-

# note that this is not used directly in this
# module, but it frequently used through the
# `glob.config.attr` syntax outside of here.
import config  # NOQA

# this file contains no actualy definitions
if __import__('typing').TYPE_CHECKING:
    from asyncio import Queue
    from typing import Optional

    from aiohttp.client import ClientSession
    from cmyui import AsyncSQLPool
    from cmyui import Server
    from cmyui import Version
    from datadog import ThreadStats

    from objects.achievement import Achievement
    from collections import PlayerList
    from collections import ChannelList
    from collections import MatchList
    from collections import ClanList
    from collections import MapPoolList
    from objects.player import Player
    from objects.score import Score
    from packets import BanchoPacket
    from packets import Packets

__all__ = (
    # current server state
    'players', 'channels', 'matches',
    'pools', 'clans', 'achievements',
    'version', 'bot', 'api_keys',
    'bancho_packets', 'db', 'http',
    'datadog', 'sketchy_queue',
    'oppai_built', 'cache'
)

# server object
app: 'Server'

# current server state
players: 'PlayerList'
channels: 'ChannelList'
matches: 'MatchList'
clans: 'ClanList'
pools: 'MapPoolList'
achievements: dict[int, list['Achievement']] # per vn gamemode

bot: 'Player'
version: 'Version'

# currently registered api tokens
api_keys: dict[str, int] # {api_key: player_id}

# list of registered packets
bancho_packets: dict['Packets', 'BanchoPacket']

# active connections
db: 'AsyncSQLPool'
http: 'ClientSession'
datadog: 'Optional[ThreadStats]'

# queue of submitted scores deemed 'sketchy'; to be analyzed.
sketchy_queue: 'Queue[Score]'

# whether or not the oppai-ng binary was located at startup.
oppai_built: bool

# gulag's main cache.
# the idea here is simple - keep a copy of things either from sql or
# that take a lot of time to produce in memory for quick and easy access.
# ideally, the cache is hidden away in methods so that developers do not
# need to think about it.
cache = {
    # algorithms like brypt these are intentionally designed to be
    # slow; we'll cache the results to speed up subsequent logins.
    'bcrypt': {}, # {bcrypt: md5, ...}
    # we'll cache results for osu! client update requests since they
    # are relatively frequently and won't change very frequently.
    'update': { # default timeout is 1h, set on request.
        'cuttingedge': {'check': None, 'path': None, 'timeout': 0},
        'stable40': {'check': None, 'path': None, 'timeout': 0},
        'beta40': {'check': None, 'path': None, 'timeout': 0},
        'stable': {'check': None, 'path': None, 'timeout': 0}
    },
    # cache all beatmap data calculated while online. this way,
    # the most requested maps will inevitably always end up cached.
    'beatmap': {}, # {md5: {timeout, map}, ...}
    # cache all beatmaps which we failed to get from the osuapi,
    # so that we do not have to perform this request multiple times.
    'unsubmitted': set() # {md5, ...}
}
