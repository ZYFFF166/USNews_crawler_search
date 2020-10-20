# coding=utf-8
# -*- coding: utf-8 -*-
import urllib
from urllib import request
from bs4 import BeautifulSoup as bs
import re
from queue import Queue
import numpy as np
import urllib.request
import urllib.error
import sys

# Your application should read a file of seed .gov  URLs and crawl the .gov pages.
# The application should also input the number of pages to crawl and the number of levels (hops (i.e. hyperlinks) away from the seed URLs).
# All crawled pages (html files) should be stored in a folder.

# base_url = r'https://www.usa.gov/'


def get_page_url(url):
    res = urllib.request.urlopen(url)
    base_soup = bs(res, 'html.parser')
    # print(base_soup)
    # next_url = base_soup.findAll('href')
    link_list = []
    link_temp = base_soup.find_all('a')
    for l in link_temp:
        link = str(l.get('href'))
        #link exits on the page
        if link is not None:
            p1 = r"https*://"
            pattern1 = re.compile(p1)
            #inner link
            if pattern1.findall(link) == []:
                next_url = str(url).strip('\n') + str(link)
            else:
                next_url = link
            # print(next_url)
            link_list.append(next_url)
        else:
            print('no link on this page')
    return link_list



def getHtml(url):
    try:

        html = urllib.request.urlopen(url).read()

    except:
        html = None
        pass

    return html


def saveHtml(file_name, file_content):
    with open("result/{0}.html".format(file_name), "wb") as f:
        f.write(file_content)

if __name__ == '__main__':
    arguments = sys.argv
    try:
        num_page = arguments[1]
        num_level = arguments[2]
        print('Start crawling ' + num_page +' seeds\n' +'Hop level is ' + num_level)
    except:
        print('Arguments passing error\n')
        print('Format: python3 cs172_project.py <num-seeds> <hops-away>')
        exits(1)

    init_url_array = []
    url_array = []
    seed_array = []
    Q = Queue()
    with open("seed_url.txt") as f:
        for line in f:
            line = str(line).strip('\n')
            seed_array.append(line)
        # print(content_array)
        for i in range(0,int(num_page)):
            html = getHtml(seed_array[i])
            if html is not None:
                file_name = 'seed'+str(i+1)
                saveHtml(file_name,html)
                output = 'crawling for seed No. '+ str(i+1) +'have completed'
                print(output)
                get_page_url(seed_array[i])
                link_list = get_page_url(seed_array[i])
                init_url_array = np.array(link_list)  # get page url
            else:
                pass

        temp_url_array = init_url_array.copy()
        temp_list =[]
        for j in range(1,int(num_level)):
            for n in range(1,5):#can only read the first six sub-urls
                try:
                    temp_list = get_page_url(temp_url_array[n])
                    temp_url_array = np.array(temp_list)
                    link_list = link_list + temp_list
                    init_url_array = np.array(link_list)
                except:
                    pass

        url_array = []

        for k in range(0,len(init_url_array)):
            if "#" in init_url_array[k]:
                pass
            elif '.gov' not in init_url_array[k]:
                pass
            else:
                if init_url_array[k] not in url_array:
                    url_array.append(init_url_array[k])

        print(url_array)

        for count in range(0,len(url_array)):

            html = getHtml(url_array[count])
            if html is not None:
                file_name = 'crawl'+str(count)
                saveHtml(file_name, html)
                output = 'crawling for level ' + str(count) + ' have completed'
                print(output)
            else:
                pass
                print("error")
