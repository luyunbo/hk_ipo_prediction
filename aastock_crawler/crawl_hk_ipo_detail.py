#!/user/bin/env python
# coding:utf-8

from selenium import webdriver

base_link = 'http://www.aastocks.com/sc/stocks/market/ipo/sponsor.aspx'


def crawl_target_link(ds, outfile):
    try:
        stocks = ds.find_elements_by_xpath('//*[@id="tblData"]/tbody/tr')
        for stock in stocks:
            items = []
            for element in stock.find_elements_by_xpath('.//td'):
                items.extend(str.split(element.text.strip().strip('"'), '\n'))
            print('\t'.join(items), file=outfile)
        return
    except Exception as e:
        print(e)


def crawl_hk_ipo_detail():
    # df = pd.read_csv('../data/ipo_list', sep='\t', index_col='code')
    # df.aggregate
    outfile = open('../data/ipo_details', 'w')
    header = ['date',  # 日期
              'name',  # 名称
              'code',  # 代号
              'sponsor',  # 保荐人
              'industry', # 行业
              'gray_market',  # 暗盘变现
              'chg_on_debut',  # 首日表现
              'acc_chg' # 累计表现
              ]
    print('\t'.join(header), file=outfile)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    ds = webdriver.Chrome(options=options)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(60)
    ds.maximize_window()
    ds.get(base_link)


    crawl_finish = 0
    cur_page_num = 1
    while crawl_finish == 0:

        print('Crawling page ' + str(cur_page_num))
        crawl_target_link(ds, outfile)

        try:
            next_page_button = ds.find_element_by_class_name("p_last")
            next_page_button.click()
            cur_page_num += 1
        except Exception as e:
            print(str(e))
            print('Crawling Finished!')
            crawl_finish = 1


if __name__ == '__main__':
    crawl_hk_ipo_detail()
