from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from core.models import Profile
from core.views import signin

# https://docs.djangoproject.com/en/4.1/intro/tutorial05/
class TestCases(TestCase):
    def setUp(self):
        print("\n[*] Running setup...")
        # every test needs access to RequestFactory to build requests
        # https://docs.djangoproject.com/en/4.1/topics/testing/advanced/#django.test.RequestFactory
        self.factory = RequestFactory()

        # create a django user and social book profile obj in db
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.profile.bio = "tests are the best"
        self.profile.location = "earth"

        print("[*] Created new User\n  username: "+self.user.username+"\n  email: "+self.user.email+"\n  password: 123")
        print("[*] Created new Profile\n  id: "+str(self.user.id)+"\n  bio: "+self.profile.bio+"\n  location: "+self.profile.location)

    def test_signin_success(self):
        print("\n[*] Testing signin success...")

        # craft a post request to signin as the user created in setup
        request = self.factory.post('/signin', {'username': 'logan', 'password': '123'})

        # add session middleware manually
        middleware = SessionMiddleware(request)
        middleware.process_request(request)

        # simulate a logged-in user by setting request.user manually.
        request.user = self.user

        # test view as if it were deployed at /signin
        print("[*] Request: %s" % request)
        print("[*] Attempting sign in...")
        response = signin(request)
        print("[*] Response: %s" % response)
        
        # redirect to / on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        