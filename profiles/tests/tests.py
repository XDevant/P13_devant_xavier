from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile


class TestProfilesIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='user', password='1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_profile = Profile.objects.create(user=self.test_user, favorite_city="Paris")
        self.test_profile.save()
        self.response = self.client.get(reverse('profiles_index'))
        self.method = self.response.request['REQUEST_METHOD']
        self.url = self.response.request['PATH_INFO']
        self.code = self.response.status_code
        self.template = self.response.templates[0].name
        self.content = str(self.response.content)
        self.context = self.response.context
        print(f"\nRequest: {self.method} '{self.url}' Response: ",
              end="")

    def test_1_profiles_index_url(self):
        assert self.code == 200, f"code = {self.code}"
        print(f"code={self.code}")

    def test_2_profiles_index_template(self):
        assert self.template == 'profiles/index.html'
        print(f"template={self.template}")

    def test_3_profiles_index_title(self):
        try:
            title = self.content.split('<title>')[1].split('</title>')[0]
            assert title == 'Profiles'
        except IndexError:
            assert False, 'No title in index page.'
        print(f"title={title}")

    def test_4_profiles_index_context(self):
        assert 'profiles_list' in self.context
        assert len(self.context['profiles_list']) == 1
        assert self.context['profiles_list'][0] == self.test_profile


class TestProfilesView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='user',
                                                  password='1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_profile = Profile.objects.create(user=self.test_user,
                                                   favorite_city="Paris")
        self.test_profile.save()
        self.response = self.client.get(reverse('profile',
                                                kwargs={
                                                    "username": self.test_profile.user.username
                                                       }
                                                ))
        self.method = self.response.request['REQUEST_METHOD']
        self.url = self.response.request['PATH_INFO']
        self.code = self.response.status_code
        self.template = self.response.templates[0].name
        self.content = str(self.response.content)
        self.context = self.response.context
        print(f"\nRequest: {self.method} '{self.url}' Response: ",
              end="")

    def test_1_profiles_url(self):
        assert self.code == 200, f"code = {self.code}"
        print(f"code={self.code}")

    def test_2_profiles_template(self):
        assert self.template == 'profiles/profile.html'
        print(f"template={self.template}")

    def test_3_profiles_title(self):
        try:
            title = self.content.split('<title>')[1].split('</title>')[0]
            assert title == self.test_profile.user.username
        except IndexError:
            assert False, 'No title in index page.'
        print(f"title={title}")

    def test_4_profiles_context(self):
        assert 'profile' in self.context
        assert self.context['profile'] == self.test_profile
