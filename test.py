import re

str = r'[0_1_0_0] srcdemonm74icqjvejew6fprssuolyoc2usjdwflevbdpqoetw4x3ead.onion/search?q=list visit in 18.68386197090149, full process in 60.04549837112427'
reg = re.compile(r'^\[(?P<index>.*)\] (?P<onion_domain>.*) visit in (?P<time>.*),')
regMatch = reg.match(str)
regDic = regMatch.groupdict()

for k, v in regDic.items():
    print("{} : ({}) {}".format(k, type(v), v))
