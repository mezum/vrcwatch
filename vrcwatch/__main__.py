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
AVATAR_PARAMS_HOUR = '/avatar/parameters/DateTimeHour'
AVATAR_PARAMS_MINUTE = '/avatar/parameters/DateTimeMinute'
AVATAR_PARAMS_SECOND = '/avatar/parameters/DateTimeSecond'
AVATAR_PARAMS_HOUR_F = '/avatar/parameters/DateTimeHourF'
AVATAR_PARAMS_MINUTE_F = '/avatar/parameters/DateTimeMinuteF'
AVATAR_PARAMS_SECOND_F = '/avatar/parameters/DateTimeSecondF'
AVATAR_PARAMS_HOUR_FA = '/avatar/parameters/DateTimeHourFA'
AVATAR_PARAMS_MINUTE_FA = '/avatar/parameters/DateTimeMinuteFA'
AVATAR_PARAMS_SECOND_FA = '/avatar/parameters/DateTimeSecondFA'
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
        '--interval',
        '-i',
        type=float,
        default=1.0,
        help='An interval of sending the time in second.'
    )
    parser.add_argument(
        '--sync',
        '-s',
        type=float,
        default=5.0,
        help='Force sync per the specified in second.'
    )
    parser.add_argument(
        '--with-analog',
        action='store_true',
        default=False,
        help='Send analog value together.'
    )
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        default=False,
        help='No print verbose messages.'
    )
    return parser.parse_args(args)


def main(args: list[str]):
    parameters = parse_args(args)

    print_if(
        not parameters.quiet,
        f'''server: {parameters.address}:{parameters.port}
interval: {parameters.interval} sec.
sync: {parameters.sync} sec.
analog: {parameters.with_analog}
''')

    client = udp_client.SimpleUDPClient(parameters.address, parameters.port)
    print_if(not parameters.quiet, 'Press Ctrl + C to stop this program.')
    try:
        sync = int(parameters.sync / parameters.interval)
        year = ReducedMessenger(client, AVATAR_PARAMS_YEAR, sync)
        month = ReducedMessenger(client, AVATAR_PARAMS_MONTH, sync)
        day = ReducedMessenger(client, AVATAR_PARAMS_DAY, sync)
        weekday = ReducedMessenger(client, AVATAR_PARAMS_WEEKDAY, sync)
        hour = ReducedMessenger(client, AVATAR_PARAMS_HOUR, sync)
        minute = ReducedMessenger(client, AVATAR_PARAMS_MINUTE, sync)
        second = ReducedMessenger(client, AVATAR_PARAMS_SECOND, sync)
        hour_f = ReducedMessenger(client, AVATAR_PARAMS_HOUR_F, sync)
        minute_f = ReducedMessenger(client, AVATAR_PARAMS_MINUTE_F, sync)
        second_f = ReducedMessenger(client, AVATAR_PARAMS_SECOND_F, sync)
        hour_fa = ReducedMessenger(client, AVATAR_PARAMS_HOUR_FA, sync)
        minute_fa = ReducedMessenger(client, AVATAR_PARAMS_MINUTE_FA, sync)
        second_fa = ReducedMessenger(client, AVATAR_PARAMS_SECOND_FA, sync)
        daytime = ReducedMessenger(client, AVATAR_PARAMS_DAYTIME, sync)

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

            second_analog = now.second / 60 + now.microsecond / 60000000
            minute_analog = now.minute / 60 + second_analog / 3600
            hour_analog = now.hour / 24 + minute_analog / 1440
            if parameters.with_analog:
                hour_fa.send(hour_analog)
                minute_fa.send(minute_analog)
                second_fa.send(second_analog)
            daytime.send(hour_analog)

            sleep(parameters.interval)

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
        '_count',
        '_max_count'
    )

    def __init__(self, client: udp_client.SimpleUDPClient, path: str, count: int = 5):
        self._client = client
        self._path = path
        self._prev = None
        self._count = count
        self._max_count = count

    def send(self, value: Any) -> None:
        self._count -= 1
        if value != self._prev or self._count < 0:
            self._client.send_message(self._path, value)
            self._prev = value
            self._count = self._max_count


if __name__ == '__main__':
    main(argv[1:])
