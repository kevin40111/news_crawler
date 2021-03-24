import requests

url = "https://udndata.com/ndapp/Story?no=2&page=1&udndbid=udndata&SearchString=pGq%2Bx6bbqnYrpOm0wT49MTk1MTAxMDErpOm0wTw9MjAyMTAzMjM%3D&sharepage=20&select=0&kind=2&article_date=1959-12-20&news_id=105722249"


headers = {
  'Content-Type': 'application/json',
  'cookie': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9; JSESSIONID=25E8E49BE991755666530B194F5F415E-n1',
  'Cookie': 'JSESSIONID=7C50A62C73EA63DE090BC45861E6BCCD-n1; _ga=GA1.2.743700092.1616483827; _gid=GA1.2.483597604.1616483827'
}

response = requests.request("GET", url, headers=headers)

print(response.text)
