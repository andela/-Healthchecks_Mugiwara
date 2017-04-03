from hchanel.api.models import Channel
from hchanel.test import BaseTestCase


class AddWebhookTestCase(BaseTestCase):

    def test_it_adds_two_webhook_urls_and_redirects(self):
        form = {"value_down": "http://foo.com", "value_up": "https://bar.com"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_webhook/", form)
        self.assertRedirects(response,  "/integrations/")

        chanel = Channel.objects.get()
        self.assertEqual(chanel.value, "http://foo.com\nhttps://bar.com")

    def test_it_adds_webhook_using_team_access(self):
        form = {"value_down": "http://foo.com", "value_up": "https://bar.com"}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post("/integrations/add_webhook/", form)

        chanel = Channel.objects.get()
        self.assertEqual(chanel.useresponse,  self.alice)
        self.assertEqual(chanel.value, "http://foo.com\nhttps://bar.com")

    def test_it_rejects_non_http_webhook_urls(self):
        form = {"value_down": "foo", "value_up": "bar"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_webhook/", form)
        self.assertContains(response,  "Enteresponse a valid URL.")

        self.assertEqual(Channel.objects.count(), 0)

    def test_it_handles_empty_down_url(self):
        form = {"value_down": "", "value_up": "http://foo.com"}

        self.client.login(username="alice@example.org", password="password")
        self.client.post("/integrations/add_webhook/", form)

        chanel = Channel.objects.get()
        self.assertEqual(chanel.value, "\nhttp://foo.com")
