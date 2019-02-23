#!/usr/bin/env python2

import netrc
import sys

MACHINE = "pinboard.in"


def token():
    n = netrc.netrc()
    auth = n.authenticators(MACHINE)
    if auth is None:
        sys.exit("Add %s to your ~/.netrc" % MACHINE)

    user = auth[0] or auth[1]
    password = auth[2]

    if user is None or password is None:
        sys.exit("Invalid netrc entry for %s" % MACHINE)

    return "%s:%s" % (user, password)
