from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import RequestFactory, TestCase, Client
from django.contrib import messages

from core.models import Profile
from core.views import signin, logout

# https://docs.djangoproject.com/en/4.1/intro/tutorial05/
class TestCases(TestCase):
    def setUp(self):
        # every test needs access to RequestFactory to build http requests
        # https://docs.djangoproject.com/en/4.1/topics/testing/advanced/#django.test.RequestFactory
        self.factory = RequestFactory()

        # create a django user and social book profile obj in temporary db
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.profile.bio = 'tests are the best'
        self.profile.location = 'earth'

    # request to signin as the user created in setup
    def test_signin_success(self):
        request = self.factory.post('/signin', {'username': self.user.username, 'password': '123'})
        AddMiddleware(request)

        response = signin(request)
        response.client = Client()
        
        # 302 redirect to / on success
        self.assertRedirects(response, '/', target_status_code=302)
        
    # request to signin with the wrong username
    def test_signin_failure_username(self):
        request = self.factory.post('/signin', {'username': 'logan2', 'password': '123'})
        AddMiddleware(request)

        response = signin(request)
        response.client = Client()
        message = get_message(request)

        # responds with message and redirect to /signin on failure
        self.assertEqual(message, 'Credentials Invaild')
        self.assertRedirects(response, '/signin')

    # request to signin with the wrong password
    def test_signin_failure_password(self):
        request = self.factory.post('/signin', {'username': self.user.username, 'password': '124'})
        AddMiddleware(request)

        response = signin(request)
        response.client = Client()
        message = get_message(request)

        # responds with message and redirect to /signin on failure
        self.assertEqual(message, 'Credentials Invaild')
        self.assertRedirects(response, '/signin')

    # request to logout the user created at setup
    def test_logout(self):
        request = self.factory.get('/logout')
        AddMiddleware(request)

        # simulate authenticated user
        request.user = self.user

        response = logout(request)
        response.client = Client()

        self.assertRedirects(response, '/signin')

# Helpers ---------------------------------------------------------------

# add default middleware config to request
def AddMiddleware(request):
    middleware = SessionMiddleware(request)
    middleware.process_request(request)
    request._messages = messages.storage.default_storage(request)

# return the first message in storage or None if empty
def get_message(request):
    storage = messages.get_messages(request)
    message = None
    for message in storage:
        break
    return str(message)