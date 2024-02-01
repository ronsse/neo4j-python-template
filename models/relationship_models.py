from datetime import datetime
import pytz
from neomodel import DateTimeProperty, StructuredRel


class TimedRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc), index=True)
