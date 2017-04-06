from django.contrib.auth.hashers import make_password
from django.test import tag
from hc.test import BaseTestCase



class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
    
    @tag('it_shows_form')
    def test_it_shows_form(self):
        response = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(response, "You are about to log in")
    @tag('it_redirects')
    def test_it_redirects(self):
        response = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    @tag('logged_in')
    def test_it_redirects_logged_in(self):
        login = self.client.login(username="jonathan@hc.com", password="password")
        form = {"email":"jonathan@hc.com"}
        resp = self.client.post("/accounts/profile/", form)
        print(resp.status_code)
        self.assertRedirects(resp, '/accounts/login/?next=/accounts/profile/')

    ### Login with a bad token and check that it redirects
    @tag('bad_token')
    def test_bad_token(self):
        resp = self.client.post("/accounts/check_token/alice/bad-token/")
        self.assertRedirects(resp, "/accounts/login/")


    ### Any other tests?
