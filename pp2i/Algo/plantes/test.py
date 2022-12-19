import re
r1 = re.compile(",$")
if r1.search("spam.pdf,"):
    print("yes")
else:
    print("no")