from uvicorn.logging import AccessFormatter, DefaultFormatter
from colorama import init
import logging
import click

init()


def colorize_record(record: logging.LogRecord):
    rules = {
        "debug": "bright_black",
        "info": "bright_blue",
        "warning": "yellow",
        "error": "red",
        "critical": "red",
        "access": 'bright_black'
    }
    levelname = record.levelname.lower()
    if levelname in rules.keys():
        record.levelname = click.style(levelname.upper(), bg=rules[levelname], fg='black')

    record.asctime = click.style(f'[{record.asctime}]', fg='bright_black')
    return record


class DefaultLogFormatter(DefaultFormatter):
    def __init__(self, color: bool = True):
        super().__init__(
            fmt='%(asctime)s %(levelname)s: %(message)s',
            use_colors=color
        )

    def formatMessage(self, record):
        return DefaultFormatter.formatMessage(
            self,
            colorize_record(record) if self.use_colors else record
        )


class AccessLogFormatter(AccessFormatter):
    def __init__(self, color: bool = True):
        super().__init__(
            fmt='%(asctime)s %(levelname)s: %(client_addr)s | "%(request_line)s" | %(status_code)s',
            use_colors=color
        )

    def formatMessage(self, record):
        record.levelname = 'ACCESS'
        return AccessFormatter.formatMessage(
            self,
            colorize_record(record) if self.use_colors else record
        )
