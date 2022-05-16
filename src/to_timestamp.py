from datetime import datetime
from time import mktime


def year_to_timestamp(year):
    try:
        return (
            t
            if (
                t := int(mktime(datetime.strptime(str(year), "%Y").timetuple()))
            )
            > 0
            else 0
        )
    except:
        print(year)


def date_to_timestamp(date):
    try:
        return (
            t
            if (
                t := int(
                    mktime(datetime.strptime(str(date), "%Y-%m-%d").timetuple())
                )
            )
            > 0
            else 0
        )
    except:
        print(date)
