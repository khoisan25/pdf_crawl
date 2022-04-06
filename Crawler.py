import urllib.request as urllib2
import os
import time
import threading
import queue
import inspect
import path
import logging

from bs4 import BeautifulSoup
from selenium import webdriver

class Crawler:
    def __init__(self):
        self.settings = Settings()
        #TODO unpack settings here.
        # crawler method, download params, extensions etc. make them class variables. Or just use settings.
        # fixed!. Deicded to use teh class variable aproach.
        self.url = self.settings.config.get('default', 'crawler', 'url')
        self.max_download_size = self.settings.config.get('default', 'crawler', 'max_download_size')
        self.file_extension = self.settings.config.get('default', 'crawler', 'file_extension')
        self.config_name = self.settings.config.get('default', 'crawler', 'config_name')
        self.output_dir = self.settings.config.get('default', 'crawler', 'output_dir')
        self.crawler_depth = self.settings.config.get('default', 'crawler', 'depth')
        self.crawler_method = self.settings.config.get('default', 'crawler', 'method')
        self.crawler_threads = self.settings.config.get('default', 'crawler', 'threads')
        self.crawler_timeout = self.settings.config.get('default', 'crawler', 'timeout')
        self.utils = Utils()
        self.handler = Handler()
        self.queue = queue.Queue()
        self.visited = set()
        self.lock = threading.Lock()
        self.threads = []
        self.start_time = time.time()
        self.download_count = 0
        self.download_size = 0
        self.logger = Logger(__file__)
        self.logger.log('Crawler started')
        self.logger.log('Crawling ' + self.url)
        self.logger.log('Crawling ' + self.url + ' with the following parameters ' + '\n' + '\t' + 'max_download_size: ' + self.max_download_size + '\n' + '\t' + 'file_extension: ' + self.file_extension + '\n' + '\t' + 'config_name: ' + self.config_name + '\n' + '\t' + 'output_dir: ' + self.output_dir + '\n' + '\t' + 'depth: ' + self.crawler_depth + '\n' + '\t' + 'method: ' + self.crawler_method + '\n' + '\t' + 'threads: ' + self.crawler_threads + '\n' + '\t' + 'timeout: ' + self.crawler_timeout)

    def crawl(self, url, depth):
        self.queue.put((url, depth))
        while True:
            try:
                url, depth = self.queue.get(timeout=self.crawler_timeout)
                self.crawl_url(url, depth)
            except queue.Empty:
                break
    def crawl_url(self, url, depth):
        if url in self.visited:
            return
        self.visited.add(url)
        if depth > 0:
            self.logger.log('Crawling ' + url + ' with depth ' + str(depth))
            try:
                if self.crawler_method == 'selenium':
                    self.crawl_url_selenium(url, depth)
                elif self.crawler_method == 'urllib2':
                    self.crawl_url_urllib2(url, depth)
                else:
                    self.logger.log('Crawler method ' + self.crawler_method + ' not supported')
            except Exception as e:
                self.logger.log('Crawler error: ' + str(e))
    def crawl_url_selenium(self, url, depth):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        # Can we do both at once?, multi-loops slow.
        #TODO 1. iter output and append hyperlinks
        #TODO 2. iter output and download files
        # Update 06.04.2022 | Needs testing.
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                if href.startswith('http'):
                    self.queue.put((href, depth - 1))
                else:
                    self.queue.put((urlparse.urljoin(url, href), depth - 1))
        for link in soup.find_all(self.file_extension):
            href = link.get('href')
            if href is not None:
                if href.startswith('http'):
                    self.download_file(href)
                else:
                    self.download_file(urlparse.urljoin(url, href))
    def crawl_url_urllib2(self, url, depth):
        try:
            request = urllib2.Request(url)
            #TODO use settings to set user agent
            response = urllib2.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Can we do both at once?, multi-loops slow.
            #TODO 1. iter output and append hyperlinks
            #TODO 2. iter output and download files
            # Update. Look above
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None:
                    if href.startswith('http'):
                        self.queue.put((href, depth - 1))
                    else:
                        self.queue.put((urlparse.urljoin(url, href), depth - 1))
            for link in soup.find_all(self.file_extension):
                href = link.get('href')
                if href is not None:
                    if href.startswith('http'):
                        self.download_file(href)
                    else:
                        self.download_file(urlparse.urljoin(url, href))
        except Exception as e:
            self.logger.log('Crawler error: ' + str(e))
    def download_file(self, url):
        try:
            request = urllib2.Request(url)
            #TODO use settings to set user agent
            response = urllib2.urlopen(request)
            file_name = response.info()['Content-Disposition'].split('filename=')[1]
            file_size = int(response.info()['Content-Length'])
            if file_size < int(self.max_download_size):
                if not self.handler.has_file_been_downloaded(url):
                    if not os.path.exists(self.output_dir):
                        os.makedirs(self.output_dir)
                    file_path = self.output_dir + file_name
                    with self.lock:
                        with open(file_path, 'wb') as file:
                            file.write(response.read())
                    self.handler.record_download(url, file_name, file_size)
                    self.download_count += 1
                    self.download_size += file_size
                    self.logger.log('Downloaded ' + file_name + ' with size ' + str(file_size) + ' bytes')
                else:
                    self.logger.log('File ' + file_name + ' has already been downloaded')
            else:
                self.logger.log('File ' + file_name + ' is too large to download')
        except Exception as e:
            self.logger.log('Crawler error: ' + str(e))

if __name__ == '__main__':
    crawler = Crawler()
    for i in range(int(crawler.crawler_threads)):
        thread = threading.Thread(target=crawler.crawl, args=(crawler.url, int(crawler.crawler_depth)))
        thread.start()
        crawler.threads.append(thread)
    for thread in crawler.threads:
        thread.join()
    crawler.logger.log('Crawling finished')
    crawler.logger.log('Crawled ' + str(crawler.download_count) + ' files with a total size of ' + str(crawler.download_size) + ' bytes')
    crawler.logger.log('Crawling took ' + str(time.time() - crawler.start_time) + ' seconds')
