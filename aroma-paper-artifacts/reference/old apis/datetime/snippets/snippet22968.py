import datetime
import typing
from pamqp import body, commands, header


@property
def timestamp(self) -> typing.Optional[datetime.datetime]:
    'Provides the ``timestamp`` property value if it is set.'
    return self.header.properties.timestamp
