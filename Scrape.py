###### WEB SCRAPER
#######################

##### Imports
from bs4 import BeautifulSoup as bs

##### Variables
names = []
terms = []
gpas = []


##### Functions
def get_span(lst):
    for ele in lst:
        try:
            content = ele.find('span')
            return content.contents
        except:
            continue
    return ""

##### Code
with open("html.txt", "r") as txtFile:
    htmlData = txtFile.read()
    soup = bs(htmlData, 'html.parser')
    headerHtml = soup.find_all('span',class_="H5b")
    rowHtml = soup.find_all('td', class_="LightSolidBorder", valign="top")
    tableHtml = soup.find_all('table')

    count=1
    for ele in rowHtml:

        info = ele.contents

        if (count%3 == 1):
            for i in info:

                try:
                    i = i.contents[0].replace(u'\xa0', u'')
                    i = i.replace(u'\n', u'')
                    i = i.replace(u'\t', u'')
                    names.append(i)
                except:
                    continue

        elif (count%3 == 2):
            for i in info:
                i = i.contents[0]
                if "Academic" in i:
                    continue
                terms.append(i)

        else:
            for i in info:
                i = i.string.replace(u'\xa0', u'')
                i = i.replace(u'\n', u'')
                i = i.replace(u'\t', u'')
                if (i == ''):
                    continue
                gpas.append(i)

        count += 1


print(names)
print(gpas)
print(terms)

'''
for ele in headerHtml:
    l = ele.string
    if (l != "None") or ("Academic" in l):
        print(ele.string)
'''
