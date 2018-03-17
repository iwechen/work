


# from lxml import etree
import re
with open('str.txt','r') as f:
    b = f.read()
    c = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>',b,re.S)
    for d in c:
        e = re.findall(r'<td.*?>(.*?)</td>',d,re.S)
        print(e)






