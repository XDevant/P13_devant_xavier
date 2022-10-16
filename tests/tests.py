from django.test import TestCase, Client
from django.urls import reverse


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('index'))
        self.method = self.response.request['REQUEST_METHOD']
        self.url = self.response.request['PATH_INFO']
        self.code = self.response.status_code
        self.template = self.response.templates[0].name
        self.content = str(self.response.content)
        print(f"\nRequest: {self.method} '{self.url}' Response: ",
              end="")

    def test_1_index_url(self):
        assert self.code == 200, f"code = {self.code}"
        print(f"code={self.code}")

    def test_2_index_template(self):
        assert self.template == 'oc_lettings_site/index.html'
        print(f"template={self.template}")

    def test_3_index_title(self):
        try:
            title = self.content.split('<title>')[1].split('</title>')[0]
            assert title == 'Holiday Homes'
        except IndexError:
            assert False, 'No title in index page.'
        print(f"title={title}")
