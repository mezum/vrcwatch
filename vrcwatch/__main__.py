#!/usr/bin/env python3
# Copyright (c) 2022 Kosaki Mezumona
# Distributed under the MIT License, see the LICENSE file.
from argparse import ArgumentParser, Namespace
from datetime import datetime
from time import sleep
from typing import Any, TextIO
from pythonosc import udp_client
from sys import argv, stderr


AVATAR_PARAMS_YEAR = '/avatar/parameters/DateTimeYear'
AVATAR_PARAMS_MONTH = '/avatar/parameters/DateTimeMonth'
AVATAR_PARAMS_DAY = '/avatar/parameters/DateTimeDay'
AVATAR_PARAMS_WEEKDAY = '/avatar/parameters/DateTimeWeekDay'
AVATAR_PARAMS_HOUR = '/avatar/parameters/DateTimeWeekHour'
AVATAR_PARAMS_MINUTE = '/avatar/parameters/DateTimeWeekMinute'
AVATAR_PARAMS_SECOND = '/avatar/parameters/DateTimeWeekSecond'
AVATAR_PARAMS_HOUR_F = '/avatar/parameters/DateTimeWeekHourF'
AVATAR_PARAMS_MINUTE_F = '/avatar/parameters/DateTimeWeekMinuteF'
AVATAR_PARAMS_SECOND_F = '/avatar/parameters/DateTimeWeekSecondF'
AVATAR_PARAMS_DAYTIME = '/avatar/parameters/DateTimeDayTime'


def parse_args(args: list[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        '--address',
        '-a',
        type=str,
        default='127.0.0.1',
        help='A destination IP address or host name.',
    )
    parser.add_argument(
        '--port',
        '-p',
        type=int,
        default=9000,
        help='A destination UDP port number',
    )
    parser.add_argument(
        '--frequency',
        '-f',
        type=float,
        default=1.0,
        help='An interval of sending the time in second.'
    )
    parser.add_argument(
        '--quiet',
        '-q',
        type=bool,
        default=False,
        help='No print verbose messages.'
    )
    return parser.parse_args(args)


def main(args: list[str]):
    parameters = parse_args(args)

    client = udp_client.SimpleUDPClient(parameters.address, parameters.port)
    print_if(not parameters.quiet, 'Press Ctrl + C to stop this program.')
    try:
        year = ReducedMessenger(client, AVATAR_PARAMS_YEAR)
        month = ReducedMessenger(client, AVATAR_PARAMS_MONTH)
        day = ReducedMessenger(client, AVATAR_PARAMS_DAY)
        weekday = ReducedMessenger(client, AVATAR_PARAMS_WEEKDAY)
        hour = ReducedMessenger(client, AVATAR_PARAMS_HOUR)
        minute = ReducedMessenger(client, AVATAR_PARAMS_MINUTE)
        second = ReducedMessenger(client, AVATAR_PARAMS_SECOND)
        hour_f = ReducedMessenger(client, AVATAR_PARAMS_HOUR_F)
        minute_f = ReducedMessenger(client, AVATAR_PARAMS_MINUTE_F)
        second_f = ReducedMessenger(client, AVATAR_PARAMS_SECOND_F)
        daytime = ReducedMessenger(client, AVATAR_PARAMS_DAYTIME)

        while True:
            now = datetime.now()
            year.send(now.year)
            month.send(now.month)
            day.send(now.day)
            weekday.send(now.weekday())
            hour.send(now.hour)
            minute.send(now.minute)
            second.send(now.second)
            hour_f.send(now.hour / 24)
            minute_f.send(now.minute / 60)
            second_f.send(now.second / 60)
            daytime.send(
                now.hour / 24 + now.minute / 1440 + now.second / 86400
            )
            sleep(parameters.frequency)

    except KeyboardInterrupt:
        print_if(not parameters.quiet, 'Terminate by user input.')


def print_if(enabled: bool, message: str, file: TextIO = stderr) -> None:
    if enabled:
        print(message, file=file)


class ReducedMessenger(object):
    __slots__ = (
        '_client',
        '_path',
        '_prev',
    )

    def __init__(self, client: udp_client.SimpleUDPClient, path: str):
        self._client = client
        self._path = path
        self._prev = None

    def send(self, value: Any) -> None:
        if value != self._prev:
            self._client.send_message(self._path, value)
            self._prev = value


if __name__ == '__main__':
    main(argv[1:])
