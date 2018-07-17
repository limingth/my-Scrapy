import requests
import json
import sys
import xlsxwriter

#print(sys.argv)
reload(sys)
sys.setdefaultencoding('utf8')

begin = int(sys.argv[1])
end = int(sys.argv[2])
print 'Start to crawl page from ', begin, 'to', end

filename = 'page'+ sys.argv[1] + 'to' + sys.argv[2] + '.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'productName')
worksheet.write('B1', 'companyName')
worksheet.write('C1', 'companyAddress')
worksheet.write('D1', 'pfLists')

#worksheet.write(1, 1, '1 1')
#worksheet.write(1, 2, '1 2')
#worksheet.write(1, 3, '1 3')

global row
row = 0
global col
col = 0
global gstr

for page in range(begin, end+1):
  s = str(page)

  headers = {
      'Origin': 'http://125.35.6.80:8080',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3472.3 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded;utf-8',
      'Accept': '*/*',
      'Referer': 'http://125.35.6.80:8080/ftba/fw.jsp',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
  }

  params = (
      ('method', 'getBaNewInfoPage'),
  )

  data = [
    ('on', 'true'),
    ('page', s),
    ('pageSize', '30'),
    ('productName', ''),
    ('conditionType', '1'),
    ('applyname', ''),
    ('applysn', ''),
  ]
  #print data

  response = requests.post('http://125.35.6.80:8080/ftba/itownet/fwAction.do', headers=headers, params=params, data=data)
  #print response.content

  #test = '{"filesize":"12","list":"key"}'
  #obj = json.loads(test)

  obj = json.loads(response.content)
  #print obj
  #print obj["list"][0]

  count = 0

  for item in obj["list"]:
    #print item
    count = count + 1
    print 'Page: ', page, '-', count
    print item['productName'],
    print item['enterpriseName'], #item['processid']

    col = 0
    row = row + 1
    worksheet.write(row, col, item['productName'])
    col = col + 1
    worksheet.write(row, col, item['enterpriseName'])
    processid = item['processid']
    #nextUrl = "http://125.35.6.80:8080/ftba/itownet/hzp_ba/fw/pz.jsp?processid="+processid+"&nid="+processid
    #print nextUrl

    headers = {
        'Origin': 'http://125.35.6.80:8080',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3472.3 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://125.35.6.80:8080/ftba/itownet/hzp_ba/fw/pz.jsp?processid='+processid+'&nid='+processid,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('method', 'getBaInfo'),
    )

    data = [
      ('processid', processid),
    ]

    response = requests.post('http://125.35.6.80:8080/ftba/itownet/fwAction.do', headers=headers, params=params, data=data)
    #print response.content

    obj2 = json.loads(response.content)
    print obj2["scqyUnitinfo"]["enterprise_name"], '-',  obj2["scqyUnitinfo"]["enterprise_address"]
    
    #col = col + 1
    #worksheet.write(row, col, obj2["scqyUnitinfo"]["enterprise_name"])
    col = col + 1
    worksheet.write(row, col, obj2["scqyUnitinfo"]["enterprise_address"])

    gstr = ''
    print '{',
    for pfItem in obj2["pfList"]:
      print pfItem["cname"],
      gstr = gstr + ' ' + pfItem["cname"]
    print '}'

    col = col + 1
    worksheet.write(row, col, gstr)

    print ''


workbook.close()
exit
