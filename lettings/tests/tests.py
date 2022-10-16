from django.test import TestCase, Client
from django.urls import reverse
from lettings.models import Address, Letting


class TestLettingsIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_address = Address.objects.create(number='21',
                                                   street='Jump',
                                                   city='Paris',
                                                   state="dirty",
                                                   zip_code="200",
                                                   country_iso_code="033")
        self.test_address.save()
        self.test_letting = Letting.objects.create(title="TEST",
                                                   address=self.test_address)
        self.test_letting.save()
        self.response = self.client.get(reverse('lettings_index'))
        self.method = self.response.request['REQUEST_METHOD']
        self.url = self.response.request['PATH_INFO']
        self.code = self.response.status_code
        self.template = self.response.templates[0].name
        self.content = str(self.response.content)
        self.context = self.response.context
        print(f"\nRequest: {self.method} '{self.url}' Response: ",
              end="")

    def test_1_lettings_index_url(self):
        assert self.code == 200, f"code = {self.code}"
        print(f"code={self.code}")

    def test_2_lettings_index_template(self):
        assert self.template == 'lettings/index.html'
        print(f"template={self.template}")

    def test_3_lettings_index_title(self):
        try:
            title = self.content.split('<title>')[1].split('</title>')[0]
            assert title == 'Lettings'
        except IndexError:
            assert False, 'No title in index page.'
        print(f"title={title}")

    def test_4_lettings_index_context(self):
        assert 'lettings_list' in self.context
        assert len(self.context['lettings_list']) == 1
        assert self.context['lettings_list'][0] == self.test_letting


class TestLettingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_address = Address.objects.create(number='21',
                                                   street='Jump',
                                                   city='Paris',
                                                   state="dirty",
                                                   zip_code="200",
                                                   country_iso_code="033")
        self.test_address.save()
        self.test_letting = Letting.objects.create(title="TEST",
                                                   address=self.test_address)
        self.test_letting.save()
        self.response = self.client.get(reverse('letting',
                                                kwargs={"letting_id": self.test_letting.id}))
        self.method = self.response.request['REQUEST_METHOD']
        self.url = self.response.request['PATH_INFO']
        self.code = self.response.status_code
        self.template = self.response.templates[0].name
        self.content = str(self.response.content)
        self.context = self.response.context
        print(f"\nRequest: {self.method} '{self.url}' Response: ",
              end="")

    def test_1_lettings_url(self):
        assert self.code == 200, f"code = {self.code}"
        print(f"code={self.code}")

    def test_2_lettings_template(self):
        assert self.template == 'lettings/letting.html'
        print(f"template={self.template}")

    def test_3_lettings_index_title(self):
        try:
            title = self.content.split('<title>')[1].split('</title>')[0]
            assert title == self.test_letting.title
        except IndexError:
            assert False, 'No title in index page.'
        print(f"title={title}")

    def test_4_lettings_index_context(self):
        assert self.context["title"] == self.test_letting.title
        assert self.context["address"] == self.test_letting.address
