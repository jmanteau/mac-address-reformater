#!/usr/bin/python
# encoding: utf-8

import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3


import netaddr

from netaddr.strategy.eui48 import (
    mac_eui48,
    mac_unix,
    mac_cisco,
    mac_unix_expanded,
    mac_bare,
    mac_pgsql,
)

class mac_comware(mac_cisco):
    pass

mac_comware.word_sep = "-"
mac_comware.word_size = 16

class mac_procurve(mac_pgsql):
    pass

mac_procurve.word_sep = "-"
mac_procurve.word_size = 24

class macformatters:

    @staticmethod
    def cisco(mac1):
        return "Cisco",str(netaddr.EUI(mac1, dialect=mac_cisco))

    @staticmethod
    def unix_expanded(mac1):
        return "Unix Expanded",str(netaddr.EUI(mac1, dialect=mac_unix_expanded))

    @staticmethod
    def baremac(mac1):
        return "Bare Mac",str(netaddr.EUI(mac1, dialect=mac_bare))

    @staticmethod
    def baremaclower(mac1):
        return "Bare Mac Lower",str(netaddr.EUI(mac1, dialect=mac_bare)).lower()

 #   @staticmethod
 #   def pgsql(mac1):
 #       return "PGSQL", str(netaddr.EUI(mac1, dialect=mac_pgsql))

 #   @staticmethod
 #   def unix(mac1):
  #2a:00:a1:28:68:00      return "UNIX",str(netaddr.EUI(mac1, dialect=mac_unix))

    @staticmethod
    def maceui(mac1):
        return "EUI",str(netaddr.EUI(mac1))

#    @staticmethod
#    def comware(mac1):
#        return "Comware",str(netaddr.EUI(mac1, dialect=mac_comware))

#    @staticmethod
#   def procurve(mac1):
#       return "Procurve",str(netaddr.EUI(mac1, dialect=mac_procurve))

def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`

    import re
    import inspect

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args

    # Get query from Alfred
    if len(wf.args) == 1:
        mac1 = wf.args[0]
    else:
        mac1 = None

    macregex = re.compile(r"((?:[\da-fA-F]{2}[\s:.-]?){6})")

    if not macregex.match(mac1):
        wf.add_item(mac1, u"NOT a valid MAC")
    else:
        try:  # needed because easy to get an exception when a MAC isn't registered in OUI db
            wf.add_item(
                str(mac1), u"Manufacturer: " + netaddr.EUI(mac1).oui.registration().org
            )

        except Exception:
            pass
            wf.add_item(str(mac1), u"Manufacturer: MAC OUI not in OUI Database")


    method_list = [
        func
        for func in dir(macformatters)
        if callable(getattr(macformatters, func)) and not func.startswith("__")
    ]
    for formatmacname in method_list:
        formatmac = getattr(macformatters, formatmacname)
        text, mac = formatmac(mac1)

        # Add an item to Alfred feedback
        wf.add_item(title=mac, subtitle=text, arg=mac, valid=True, copytext=mac)

        # wf.add_item(title=cisco(mac1), subtitle=u"Cisco", arg=cisco(mac1),valid=True, copytext=cisco(mac1))
        # wf.add_item(title=unix_expanded(mac1), u"UNIX Expanded")
        # wf.add_item(baremac(mac1), u"Bare MAC")
        # wf.add_item(baremaclower(mac1), u"Bare MAC Lower")
        # wf.add_item(pgsql(mac1), u"PGSQL")
        # wf.add_item(unix(mac1), u"Unix")
        # wf.add_item(maceui(mac1), u"EUI")
        # wf.add_item(comware(mac1), u"Comware")
        # wf.add_item(procure(mac1), u"Procurve")

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == "__main__":
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
