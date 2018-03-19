###### WEB SCRAPER
#######################

##### Imports
from bs4 import BeautifulSoup as bs
import csv

##### Variables
headers = ["Name", "Term", "GPA", "Approval", "Program", "Major", "Support" ]
names = []
terms = []
gpas = []
approval = []
program = []
money = []
majors = []

##### Functions
def get_span(lst):
    for ele in lst:
        try:
            content = ele.find('span')
            return content.contents
        except:
            continue
    return ""

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def deList(lst):
    final = ""
    for i in lst:
        final += i
    return final

def write(_row):
    with open("StudyAbroadSF18.csv", "a") as f:
        writer = csv.writer(f, quoting = csv.QUOTE_NONNUMERIC)
        writer.writerow(_row)

##### Code
with open("html.txt", "r") as txtFile:
    htmlData = txtFile.read()
    soup = bs(htmlData, 'html.parser')
    tableHtml = soup.find_all('table',class_="table-bordered table-condensed data-table")
    rowHtml = soup.find_all('td', class_="LightSolidBorder", valign="top")

    for personData in tableHtml:
        personRows = personData.find_all("tr")
        for row in personRows:
            spans = row.find_all('span')

            # the first span (ie spans[0]) gives content Id
            #
            # only want:
            #      1) 1-1, Advisor Approval
            #      2) 2-1, Study Abroad Program
            #      3) 2-6, Financial Need
            #      4) 2-9, Major Field of Study
            try:
                if spans[0].string.strip() == "1-1":
                    try:
                        approval.append(spans[1].string.strip())
                    except:
                        approval.append("check approval")

                if spans[0].string.strip() == "2-1":
                    try:
                        program.append(spans[1].string.strip())
                    except:
                        print("no program")

                if spans[0].string.strip() == "2-6":

                    try:
                        financialInfo = ''

                        for e in spans[1].findAll('br'):
                            e.replace_with(' ')

                        for e in spans[1].findAll('strong'):
                            e.replace_with(' ')

                        for i in spans[1].contents:
                            financialInfo += i.strip() + " "

                        money.append(financialInfo)

                    except:
                        money.append("check attachment")

                if spans[0].string.strip() == "2-9":
                    try:
                        majors.append(spans[1].string.strip())
                    except:
                        print("no major")

            except:
                continue


    ## Get Names, GPAS and terms
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

# Due to html format, we lost a approval, GPA and Term observation
# Add missing entry manually
terms.insert(21,"Summer")
gpas.insert(21,"0")
approval.append("YES")

# Already checked lists are all same length
# Write CSV File
write(headers)
for i in range(len(names)):
    rowData = [names[i],terms[i], gpas[i], approval[i], program[i], majors[i], money[i]]
    write(rowData)
