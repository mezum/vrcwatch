[日本語: README.md](README.md)

# VRCWatch

VRCWatch sends the time on your PC to VRChat through OpenSound Control (OSC).

## How to use

1. Install Python (3.9 or above)
2. Execute `setup.bat` if first use.
3. Launch VRChat.
4. Enable OSC feature in VRChat if disabled.
5. Execute `run.bat`.
6. Press both Ctrl and C keys on the command prompt to terminate `run.bat`.

## Avatar Parameters

This script sends the following avatar parameters to VRChat through OSC (OpenSound Control).
All parameters start with `DateTime`.

- `DateTimeYear`
- `DateTimeMonth`
- `DateTimeDay`
- `DateTimeWeekDay`
- `DateTimeHour`
- `DateTimeMinute`
- `DateTimeSecond`
- `DateTimeHourF`
- `DateTimeMinuteF`
- `DateTimeSecondF`
- `DateTimeDayTime`
- `DateTimeHourFA`
- `DateTimeMinuteFA`
- `DateTimeSecondFA`

// TODO: Add details and examples.

## Copyright / License

Copyright (c) 2022 Kosaki Mezumona

MIT License, see [LICENSE](LICENSE).
