import csv 
from urllib.parse import quote_plus
from urllib.request import urlopen

from bs4 import BeautifulSoup

def search():
    print('크롤링 작업 중입니다.')
    url = f'''https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query={quote_plus(search)}'''
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    total = soup.select('.api_txt_lines.total_tit')
    
    data = []
    
    for i in total:
        # print(i.text)
        # print(i.attrs['href'])
        data.append([i.text, i.attrs['href']])
        
    return data
            
if __name__ == '__main__':
    data = search('인공지능')
    for x in data:
        print(x)