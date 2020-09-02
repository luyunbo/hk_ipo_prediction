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
            e = str.split(element.text.strip().strip('"'), '\n')
            items.extend(e)
        items.remove('')
        if '跌穿上市价' in items:
            items.remove('跌穿上市价')
        print(items)
        print('\t'.join(items), file=outfile)
    return 0


def crawl_hk_ipo():
    outfile = open('../data/ipo_list', 'w')
    header = ['name',  # 名称
              'code',  # 代号
              'date',  # 上市日期
              'lot_size',  # 每手股数
              'market_cap',  # 上市市值(亿元)
              'offer_price',  # 招股价
              'listing_price',  # 上市价
              'over_sub_rate',  # 超额倍数
              'applied_lots_for_one_lot',  # 稳中一手
              'one_lot_success_rate',  # 中签率
              'last',  # 现价
              'chg_on_debut', # 首日表现
              'acc_chg'] #累计表现
    print('\t'.join(header), file=outfile)
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
