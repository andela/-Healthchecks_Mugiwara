from django.test import tag
from hc.api.models import Check
from hc.test import BaseTestCase



class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    @tag('team_access_works')
    def test_team_access_works(self):
        url ="/checks/add/"
        self.client.login(username="bob@example.org", password="password")
        r = self.client.post(url)
        team_access = Check.objects.get()
        self.assertIn(team_user.user, self.alice)
