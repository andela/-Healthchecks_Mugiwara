from django.test import tag
from hc.test import BaseTestCase
from hc.api.models import Check

@tag('switch_team')
class SwitchTeamTestCase(BaseTestCase):

    @tag('it_switches')
    def test_it_switches(self):
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)

        ### Assert the contents of r
        self.assertContains(r, "bob@example.org")

    @tag('checks_membership')
    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url)
        ### Assert the expected error code
        self.assertEquals(r.status_code, 403, "Should return a forbidden access code.")

    @tag('switches_own_team')
    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        ### Assert the expected success code
        self.assertEquals(r.status_code, 200, "Should return an OK status code.")
