import requests
import xml.etree.ElementTree as ET
"""
q = requests.get(
    "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1/?"
    "format=XML"
    "&key=9D6AA7810AF5EF66B3A70566614DE147"
    "&player_name=mabufula"
    "&matches_requested=1")
"""
r = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1/?"
                 "format=%s"
                 "&key=%s"
                 "&player_name=%s"
                 "&matches_requested=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147","mabufula","1"))
tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
asdf=tree.find("matches").find("match").find("players").find("player").find("level")
print r.text
print asdf.text
