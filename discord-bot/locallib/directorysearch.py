from email.mime import text
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import html2text

async def check_is_student(rcs):
    base = r'http://info.rpi.edu/directory-search/'
    async with aiohttp.ClientSession() as session:
        async with session.get(base + str(rcs)) as resp:
        #async with session.get('https://www.google.com') as resp:
            print(resp.status)
            content = await resp.text()
            #print(content)
            soup = BeautifulSoup(content,'html.parser')
            l = []
            for a in soup.find_all('td'):
                # print(repr(str(a)))
                try:
                    # print('\n')
                    s1 = re.search(r'>[\s,\S]{1,}<',str(a),re.M).group(0).strip('<').strip('>').strip()
                    # print(repr(s1))
                    l.append(s1)
                except Exception as e:
                    print(e)
                    # print('\n')
                    # print("None")
                # print("\n\n")
            # for li in l:
            #     print(repr(li))
            if len(l) < 3:
                return (False, 'Not Found',None)
            else:
                for i in range(len(l)):
                    if re.match(rcs + '@rpi.edu',l[i]) is not None:
                        #print(l)
                        return (l[i+1] == '',l[i+1],re.search(r'>[\s,\S]{1,}<',l[0],re.M).group(0).strip('<').strip('>').strip())
                return (False,'Not Found',None)

async def update_alerts():
    alerturl = r'https://alert.rpi.edu/'
    lastalert = ""
    while True:
        await asyncio.sleep(10)
        async with aiohttp.ClientSession() as session:
            async with session.get(alerturl) as alerttxt:
                content = await alerttxt.text()
                soup = BeautifulSoup(content, "lxml")
                incident_type = "incident"
                for incident in soup.findAll("div", {"class": incident_type}):
                    alert = html2text.html2text(str(incident))
                # print(repr(content))
                # print(content.splitlines()[0][:-1][16:].strip("\""))
                # alert = content.splitlines()[0][:-1][16:].strip("\"")
                if alert == "":
                    continue
                elif alert == lastalert:
                    continue
                else:
                    return alert

async def checkprint(rcs):
    val = await update_alerts()
    print(val)

if __name__ == "__main__":
    print('running...')
    testcheckrcs = 'persap'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checkprint(testcheckrcs))



# page = Request(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0'})
# print(urlopen(page).read())
