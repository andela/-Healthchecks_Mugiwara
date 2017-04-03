from django.test.utils import override_settings
from django.test import tag
from hc.api.models import Channel, Check
from hc.test import BaseTestCase
import pdb


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)

        self.assertRedirects(response, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        query = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(query.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            response = self.client.get(url)
            self.assertContains(response, "Integration Settings", status_code=200)

    ### Test that the team access works
    @tag('team_access_working')
    def test_team_access_working(self):
        self.client.login(username="bob@example.org", password="password")
        url = "/checks/add/"
        self.client.post(url)
        team_access =  Check.objects.get()
        self.assertEqual(team_access.user, self.alice, "Should return a valid team member")
        
        
    ### Test that bad kinds don't work
    @tag('bad_kinds')
    def test_bad_kinds_dont_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = "jabbajabba"
        url = "/integrations/add_%s" % kinds
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, "Should return a 404 error for bad kinds.")

