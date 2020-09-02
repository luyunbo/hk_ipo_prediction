#!/user/bin/env python3
# coding:utf-8

import selenium
from selenium import webdriver

start_link = 'http://www.aastocks.com/sc/stocks/market/ipo/listedipo.aspx'

def get_sotcks_info(ds, outfile):
    stocks = ds.find_elements_by_xpath('//*[@id="IPOListed"]/table/tbody/tr')
    for stock in stocks:
        items = []
        for element in stock.find_elements_by_xpath('.//td'):
            items.extend(str.split(element.text.strip().strip('"'), '\n'))
        print(items)
        print('\t'.join(items), file=outfile)
    return 0


def crawl_hk_ipo():
    outfile = open('../data/ipo_list', 'w')
    header = 'date' + '\t' + 'code' + '\t' + 'name' + '\t' + 'category' + '\t' + 'ipo_price' + '\t' + 'buy_ratio' + '\t' + 'one_hand' + '\t' + 'draw_prob' + '\t' + 'firstday_performance' + '\t' + 'now_price' + '\t' + 'total_performance'
    print(header.encode('utf-8'))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    ds = webdriver.Chrome(options=options)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(60)
    ds.maximize_window()
    crawl_finish = 0
    ds.get(start_link)

    cur_page_num = 1
    while crawl_finish == 0:

        print('Crawling page ' + str(cur_page_num))
        get_sotcks_info(ds, outfile)

        try:

            next_page_button = ds.find_element_by_class_name("p_last")
            next_page_button.click()
            cur_page_num += 1
        except Exception as e:
            print(str(e))
            print('Crawling Finished!')
            crawl_finish = 1

    return 0


if __name__ == '__main__':
    crawl_hk_ipo()
