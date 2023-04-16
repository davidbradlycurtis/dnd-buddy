#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author: David Curtis
# Contact: davidbradlycurtis.com
# ---------------------------------------------------------------------------
""" A simple Discord Bot to help in running Tabletop games"""
# ---------------------------------------------------------------------------

import logging
import os
import sys

import discord
from discord.ext import commands

# ---------------------------------------------------------------------------

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
OPEN_ROLL = False
VERSION = '1.0.0'
QUIET_MODE = True if os.getenv('QUIET_MODE', False) else False
ENV_TOKEN = 'DISCORD_TOKEN'
COMMAND_PREFIX = '&'
CHECK_TYPES = {
    'str': 'Strength',
    's': 'Strength',
    'ath': 'Athletics',
    'dex': 'Dexterity',
    'd': 'Dexterity',
    'acro': 'Acrobatics',
    'sle': 'Sleight of Hand',
    'stl': 'Stealth',
    'int': 'Intelligence',
    'i': 'Intelligence',
    'arc': 'Arcana',
    'his': 'History',
    'inv': 'Investigation',
    'nat': 'Nature',
    'rel': 'Religion',
    'con': 'Constitution',
    'wis': 'Wisdom',
    'w': 'Wisdom',
    'hand': 'Animal Hanlding',
    'ins': 'Insight',
    'med': 'Medicine',
    'per': 'Perception',
    'sur': 'Survial',
    'char': 'Charisma',
    'dec': 'Deception',
    'inti': 'Intimidation',
    'perf': 'Performance',
    'pers': 'Persuasion'
}
ROLL_CHANNELS = ['rolls', 'general']
MEME_CHANNELS = ['memes']
HELP_MESSAGE = """
Dnd-Buddy is simple Discord bot who's function is to assist in running tabletop games in Discord.

Commands:
    - &info: prints this message
    - &roll: prompt the users for a roll check
    - &save: prompt the users for a saving throw
    - &init: promt the users to roll for initiative
"""
SPACER = '#################################################################################\n'
CLOSER = '---------------------------------  END  ---------------------------------'
EVERYONE_ROLL_MESSAGE = '--------------------- Everyone roll a {type} check! ---------------------'
SPECIFIC_ROLL_MESSAGE = '--------------------- Roll a {type} check {players}! --------------------'
EVERYONE_SAVE_MESSAGE = '--------------------- Everyone roll a {type} saving throw! ---------------------'
SPECIFIC_SAVE_MESSAGE = '--------------------- Roll a {type} saving throw {players}! --------------------'
ROLL_FOR_INITIATIVE = '-------------------------- Roll for initative! --------------------------'
ROLL_TYPES = 'Roll types: '

BINGUS = 'https://media.tenor.com/kVfrg-iSDEsAAAAd/floppa-hiss-floppa-angery.gif'
BENIS = '🍆'

# ---------------------------------------------------------------------------

logging.basicConfig(format = LOGGING_FORMAT)
LOGGER = logging.getLogger('dnd-buddy')
LOGGER.setLevel('INFO')

########################################

def fail():
    LOGGER.critical('Encountered a faital error, exiting...')
    sys.exit(1)

########################################

def get_token():
    token = os.getenv(ENV_TOKEN, None)

    if token is None:
        LOGGER.error(f'Token not set in env variable: {ENV_TOKEN}')
        fail()

    return token

########################################

def log_command(context, command, **args):
    LOGGER.info(f'Processing command {command}')
    LOGGER.info(f'- Channel: {context.channel.name}')
    LOGGER.info(f'- User: {context.author.display_name}')
    if args:
        LOGGER.info(f'- Args:')
        for arg in args:
            LOGGER.info(f'-- {arg} = {args.get(arg)}')

########################################

def get_roll_type(check: str):
    _type = CHECK_TYPES.get(check.lower(), None)
    if _type is None:
        LOGGER.info(f'- Could not find matching check type for check: {check}')
        _type = check

    return _type

########################################

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(intents = intents, command_prefix = COMMAND_PREFIX)
    token = get_token()

    @bot.event
    async def on_ready():
        LOGGER.info(f'Dnd-Buddy connected as: {bot.user}')
        LOGGER.info(f'Running in quiet mode: {QUIET_MODE}')
        LOGGER.info('')

###########################################
############## Main Commands ##############

    @bot.command()
    async def info(context):
        """
        Provides a help message for using Dnd-Buddy

        Example:
            &info
        """
        global QUIET_MODE

        log_command(context, 'info')
        if QUIET_MODE:
            await context.message.delete()

        await context.send(HELP_MESSAGE)
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def space(context):
        """
        Print a spacer

        Example:
            &space
        """
        global QUIET_MODE

        log_command(context, 'space')
        if QUIET_MODE:
            await context.message.delete()

        await context.send(SPACER)
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def roll(context, check: str, players = None):
        """
        Prompts the users for a roll check
        
        Example:
            &roll dex
        """
        global OPEN_ROLL
        global QUIET_MODE

        log_command(context, 'roll', check = check, players = players)
        if QUIET_MODE:
            await context.message.delete()

        if OPEN_ROLL:
            await context.send(CLOSER)
            await context.send(SPACER)
        if context.channel.name in ROLL_CHANNELS:
            check = get_roll_type(check)
            if not players:
                await context.send(
                    EVERYONE_ROLL_MESSAGE.format(
                        type = check
                    )
                )
            else:
                await context.send(
                    SPECIFIC_ROLL_MESSAGE.format(
                        type = check,
                        players = players.replace(',', ', ')
                    )
                )
            OPEN_ROLL = not OPEN_ROLL
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def save(context, check: str, players = None):
        """
        Prompts the users for a roll check
        
        Example:
            &roll dex
        """
        global OPEN_ROLL
        global QUIET_MODE

        log_command(context, 'save', check = check, players = players)
        if QUIET_MODE:
            await context.message.delete()

        if OPEN_ROLL:
            await context.send(CLOSER)
            await context.send(SPACER)
        if context.channel.name in ROLL_CHANNELS:
            check = get_roll_type(check)
            if not players:
                await context.send(
                    EVERYONE_SAVE_MESSAGE.format(
                        type = check
                    )
                )
            else:
                await context.send(
                    SPECIFIC_SAVE_MESSAGE.format(
                        type = check,
                        players = players.replace(',', ', ')
                    )
                )
            OPEN_ROLL = not OPEN_ROLL
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def init(context):
        """
        Prompts the users to roll for initiative
        
        Example:
            &init
        """
        global OPEN_ROLL
        global QUIET_MODE

        log_command(context, 'init')
        if QUIET_MODE:
            await context.message.delete()

        if OPEN_ROLL:
            await context.send(CLOSER)
            await context.send(SPACER)
        if context.channel.name in ROLL_CHANNELS:
            await context.send(
                ROLL_FOR_INITIATIVE
            )
            OPEN_ROLL = not OPEN_ROLL
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def getRolls(context):
        """
        Returns the list of roll types
        
        Example:
            &getRolls
        """
        global OPEN_ROLL
        global QUIET_MODE

        log_command(context, 'init')
        if QUIET_MODE:
            await context.message.delete()

        if context.channel.name in ROLL_CHANNELS:
            await context.send(ROLL_TYPES)
            await context.send(CHECK_TYPES)
        LOGGER.info('--SUCCESS\n')

###########################################
############## Meme Commands ##############
    @bot.command()
    async def bingus(context):
        """
        Bingus

        Example:
            &bingus
        """
        global QUIET_MODE

        log_command(context, 'init')
        if QUIET_MODE:
            await context.message.delete()

        if context.channel.name in MEME_CHANNELS:
            await context.send(BINGUS)
        LOGGER.info('--SUCCESS\n')

    @bot.command()
    async def benis(context):
        """
        Benis

        Example:
            &bingus
        """
        global QUIET_MODE

        log_command(context, 'init')
        if QUIET_MODE:
            await context.message.delete()

        if context.channel.name in MEME_CHANNELS:
            await context.send(BENIS)
        LOGGER.info('--SUCCESS\n')


###########################################
##################  Run  ##################
    bot.run(token)

########################################

if __name__ == '__main__':
    main()
