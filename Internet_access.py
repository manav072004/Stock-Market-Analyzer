import requests as rq
import json,lxml,re
from bs4 import BeautifulSoup
import pandas as pd




def stock_summary(stock):
    url = 'https://finance.yahoo.com/quote/' + stock
    r = rq.get(url)

    web_content = BeautifulSoup(r.text, "lxml")
    table_values = web_content.find_all(
        "tr", class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)"
    )
    
    for row in table_values:
        tds = [td.get_text(strip=True) for td in row.select("td")]
        print(*tds)

def latest_news(number_news):
    html = rq.get('https://finance.yahoo.com/')
    soup = BeautifulSoup(html.text, 'lxml')

    all_script_tags = soup.select('script')

    matched_string = ''.join(re.findall(r'root\.App\.main = (.*);\n+}\(this\)\);\n+</script>', str(all_script_tags)))
    matched_string_json = json.loads(matched_string)
    matched_string_json_stream = matched_string_json['context']['dispatcher']['stores']['ThreeAmigosStore']['data']['ntk']['stream']

    for top_news_result_index in range(0, number_news):
        teaser = matched_string_json_stream[top_news_result_index]['editorialContent']['teaser']
        title = matched_string_json_stream[top_news_result_index]['editorialContent']['title']
        source = matched_string_json_stream[top_news_result_index]['editorialContent']['content']['provider']['displayName']
        canonical_url = matched_string_json_stream[top_news_result_index]['editorialContent']['content']['canonicalUrl']['url']

        print(f'News result number: {top_news_result_index}')
        print(f'DESCRIPTION: {teaser}')
        print(f'TITLE: {title}')
        print(f'SOURCE OF ARTICLE: {source}')
        print(f'ARTICLE LINK:{canonical_url}\n')

def top_gainers():
    url = 'https://finance.yahoo.com/gainers'
    r = rq.get(url)

    web_content = BeautifulSoup(r.text, "html")    

    top_shift = web_content.find_all(
        'tr', class_="simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)" 
    )

    for row in top_shift:
        tds = [td.get_text(strip=True) for td in row.select("td")]
        for value in tds:
            print(value)

def top_losers():
    url = 'https://finance.yahoo.com/losers'
    r = rq.get(url)

    web_content = BeautifulSoup(r.text, "html")    

    top_shift = web_content.find_all(
        'tr', class_="simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)" 
    )

    for row in top_shift:
        tds = [td.get_text(strip=True) for td in row.select("td")]
        for value in tds:
            print(value)


    


if __name__ == '__main__':
    

    value = input('What do you want to search?(stocks, latest news, top stock gainers)')

    while value != 'exit':
        if value.lower() == 'stocks':
            stock = input('Enter a stock symbol that you want data for?')
            stock_summary(stock)
        elif value.lower() == 'news':
            news = input('How many latest news articles do you want?(Max is 10)')
            if news <= 10:
                latest_news(news)
            else:
                print('pick less than or equal to 10 stocks')
        elif value.lower() == 'top stock gainers':
            val = input('Enter top gainers or top losers')
            if val == 'gainers':
                top_gainers()
            else:
                top_losers()
        else:
            print('Try again')
        value = input('What do you want to search?(stocks or news)\n To leave enter exit')
