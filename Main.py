import requests
from bs4 import BeautifulSoup
def getElementsSalahFromTr(tr):
    R = []
    for row in tr[1:]:
        td = row.find_all('td')
        Day = str(td[0]).split('<')[1].split('>')[1]
        DayNumberHijri = str(td[1]).split('<')[1].split('>')[1]
        DayNumberMiladi = str(td[2]).split('<')[1].split('>')[1]
        Fajr = str(td[3]).split('<')[1].split('>')[1]
        Sunrise = str(td[4]).split('<')[1].split('>')[1]
        Dhuhr = str(td[5]).split('<')[1].split('>')[1]
        Asr = str(td[6]).split('<')[1].split('>')[1].replace('\n            \t','').replace('            ','')
        Maghrib = str(td[7]).split('<')[1].split('>')[1].replace('\n            \t','')
        Isha = str(td[8]).split('<')[1].split('>')[1]
        R.append({
            'Day':Day,
            'DayNumberHijri':DayNumberHijri,
            'DayNumberMiladi':DayNumberMiladi,
            'Fajr':Fajr,
            'Sunrise':Sunrise,
            'Dhuhr':Dhuhr,
            'Asr':Asr,
            'Maghrib':Maghrib,
            'Isha':Isha
        })
    return R


def getSalahHour(url:str):
    resp = requests.get(url)
    data = resp.text
    soup = BeautifulSoup(data, features="html.parser")
    table = soup.find('table')
    # loop in the data 
    tr = table.find_all('td',class_="wakt")
    ## get Wakit
    # for t in tr:
    #     print(t)
    hijri = str(tr[1]).split('<')[1].split('>')[1]
    miladi = str(tr[2]).split('<')[1].split('>')[1]
    tr = table.find_all('tr')
    Salat = getElementsSalahFromTr(tr)
    return {
        'hijri':hijri,
        'miladi':miladi,
        'Salat':Salat
    }



url = "http://www.habous.gov.ma/prieres/horaire_hijri.php"
resp = requests.get(url)
data = resp.text
soup = BeautifulSoup(data, features="html.parser")
# First we will get the cities of this url 
selects = soup.find_all('select',attrs={'name':'ville'})
# print(selects)
# loop in the selects 
# the groups
# the citeis

for select in selects:
    if select.has_attr("name") and select['name'] == "ville": 
        groups = select.find_all('optgroup')
        for group in groups:
             lable = group['label']
             for option in group:
                 # the city
                 if(option.has_attr('value')):
                    value = option['value']
                    city = str(option).split('<')[1].split('>')[1]
                    id = str(option).split('<')[1].split('?ville=')[1].split('"')[0]
                    dataUrl = url+"?ville="+id
                    data = getSalahHour(dataUrl)
                    R = {
                        'value':value,
                        'city':city,
                        'dataUrl':dataUrl,
                        'id':id,
                        'data':data
                    }
                    print(R)


