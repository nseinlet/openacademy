# -*- coding: utf-8 -*-
import random

from locust import HttpUser, TaskSet, task
from requests.adapters import HTTPAdapter


class ReuseCookiesTaskSet(TaskSet):
    cookies = {}

    def on_start(self):
        self.client.mount('https://', HTTPAdapter(pool_connections=1000, pool_maxsize=1000))

    @task(1)
    def login(self):
         self.cookies = {}
         r = self.client.request("get", "/web/login", cookies=self.cookies)
         if not self.cookies:
             self.cookies = r.cookies 

class PreXP(ReuseCookiesTaskSet):
    
    def on_start(self):
        super(PreXP, self).on_start()
        self.urls = []
        with open('urls') as f:
            self.urls = [l.strip('\n') for l in f.readlines()]

    @task(10)
    def get_randon_url(self):
        self.client.request("get", random.choice(self.urls), cookies=self.cookies, allow_redirects=False)


class MyLocust(HttpUser):
    host = "http://localhost:8069"
    tasks = [PreXP]
    min_wait = 150
    max_wait = 150