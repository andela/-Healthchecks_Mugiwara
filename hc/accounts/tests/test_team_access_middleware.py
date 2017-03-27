from django.contrib.auth.models import User
from django.test import TestCase, tag
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):

    @tag('missing_profiles')
    def test_it_handles_missing_profile(self):
        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        self.client.login(username="ned@example.org", password="password")
        r = self.client.get("/about/")
        self.assertEqual(r.status_code, 200)

        ### Assert the new Profile objects count
        user = User.objects.count()
        self.assertEqual(user, 1, "Should return 1 as the value of user profiles.")
