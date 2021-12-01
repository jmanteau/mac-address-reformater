import netaddr

from netaddr.strategy.eui48 import (
    mac_eui48,
    mac_unix,
    mac_cisco,
    mac_unix_expanded,
    mac_bare,
    mac_pgsql,
)
import re, inspect

macregex = re.compile(r"((?:[\da-fA-F]{2}[\s:.-]?){6})")


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

mac1="8c:85:90:44:ee:bb"

method_list = [func for func in dir(macformatters) if callable(getattr(macformatters, func)) and not func.startswith("__")]
for formatmacname in method_list:
    formatmac= getattr(macformatters,formatmacname)
    mac = formatmac(mac1)
    print(mac)
