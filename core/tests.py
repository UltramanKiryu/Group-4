# Calls Libraries
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase, Client
from django.contrib import messages

from django.contrib.auth.models import User
from core.models import Profile, FollowersCount
from core.views import follow, settings, signup, signin, logout

# https://docs.djangoproject.com/en/4.1/intro/tutorial05/

class FollowTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')
        self.user2 = User.objects.create_user(username='logan2', email='logan2@email.com', password='321')

    # request to follow user2 as user
    def test_follow(self):
        request = self.factory.post('/follow', {'follower': self.user.username, 'user': self.user2.username})
        AddMiddleware(request)

        # simulate authenticated user
        request.user = self.user

        response = follow(request)
        response.client = Client()
        
        # 302 redirect to /profile/user2 on success
        self.assertRedirects(response, '/profile/'+self.user2.username, target_status_code=302)

        # verify model updated
        following = str(FollowersCount.objects.get(follower=self.user, user=self.user2))
        self.assertEqual(following, self.user2.username)

    # request to unfollow user2 as user
    def test_unfollow(self):
        request = self.factory.post('/follow', {'follower': self.user.username, 'user': self.user2.username})
        AddMiddleware(request)

        # simulate authenticated user
        request.user = self.user

        follow(request)            # follow
        response = follow(request) # unfollow
        response.client = Client()
        
        # 302 redirect to /profile/user2 on success
        self.assertRedirects(response, '/profile/'+self.user2.username, target_status_code=302)

        # verify model updated
        self.assertRaises(FollowersCount.DoesNotExist, FollowersCount.objects.get, follower=self.user, user=self.user2)


class SettingsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)

    # request to update settings
    def test_update_settings(self):
        request = self.factory.post('/settings', {'bio': 'new bio', 'location': 'here'})
        AddMiddleware(request)

        # simulate authenticated user
        request.user = self.user
        response = settings(request)
        response.client = Client()
        
        # 302 redirect to /settings on success
        self.assertRedirects(response, '/settings', target_status_code=302)

        # verify model updated
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'new bio')
        self.assertEqual(profile.location, 'here')


class SignUpTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.new_user = User(username='logan2', email='email@email.com', password='123')

    # request to signup
    def test_signup(self):
        request = self.factory.post('/signup', {'username': self.new_user.username, 'email': self.new_user.email, 'password': self.new_user.password, 'password2': self.new_user.password})
        AddMiddleware(request)

        response = signup(request)
        response.client = Client()
        
        # 302 redirect to /settings on success
        self.assertRedirects(response, '/settings', target_status_code=302)

        # verify models created
        user = User.objects.get(username=self.new_user.username)
        self.assertTrue(user.check_password(self.new_user.password))
        self.assertEqual(user.email, self.new_user.email)
        
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.id_user, user.id)
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.location, '')

    # request to signup with non-matching passwords
    def test_non_matching_passwords(self):
        request = self.factory.post('/signup', {'username': self.new_user.username, 'email': self.new_user.email, 'password': self.new_user.password, 'password2': '1234'})
        AddMiddleware(request)

        response = signup(request)
        response.client = Client()
        message = get_message(request)
        
        # responds with message and redirect to /signup on failure
        self.assertEqual(message, 'Password Not Matching')
        self.assertRedirects(response, '/signup')

    # request to signup with a taken email
    def test_email_taken(self):
        request = self.factory.post('/signup', {'username': self.new_user.username, 'email': self.user.email, 'password': self.new_user.password, 'password2': self.new_user.password})
        AddMiddleware(request)

        response = signup(request)
        response.client = Client()
        message = get_message(request)
        
        # responds with message and redirect to /signup on failure
        self.assertEqual(message, 'Email Taken')
        self.assertRedirects(response, '/signup')

    # request to signup with a taken username
    def test_username_taken(self):
        request = self.factory.post('/signup', {'username': self.user.username, 'email': self.new_user.email, 'password': self.new_user.password, 'password2': self.new_user.password})
        AddMiddleware(request)

        response = signup(request)
        response.client = Client()
        message = get_message(request)
        
        # responds with message and redirect to /signup on failure
        self.assertEqual(message, 'Username Taken')
        self.assertRedirects(response, '/signup')


class SignInTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')

    # request to signin as the user created in setup
    def test_signin(self):
        print("\n[*] Testing signin...")

        # craft a post request to signin as the user created in setup
        request = self.factory.post('/signin', {'username': 'logan', 'password': '123'})

        # add session middleware
        AddMiddleware(request)
        request.session.save()

        # simulate a logged-in user by setting request.user manually.
        request.user = self.user

        # test view as if it were deployed at /signin
        print("[*] Request: %s" % request)
        print("[*] Attempting sign in...")
        response = signin(request)
        response.client = Client()
        print("[*] Response: %s" % response)

        # redirect to / on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        
    # request to signin with the wrong username
    def test_wrong_username(self):
        request = self.factory.post('/signin', {'username': 'logan2', 'password': '123'})
        AddMiddleware(request)

        response = signin(request)
        response.client = Client()
        message = get_message(request)

        # responds with message and redirect to /signin on failure
        self.assertEqual(message, 'Credentials Invaild')
        self.assertRedirects(response, '/signin')

    # request to signin with the wrong password
    def test_wrong_password(self):
        request = self.factory.post('/signin', {'username': self.user.username, 'password': '124'})
        AddMiddleware(request)

        response = signin(request)
        response.client = Client()
        message = get_message(request)

        # responds with message and redirect to /signin on failure
        self.assertEqual(message, 'Credentials Invaild')
        self.assertRedirects(response, '/signin')


class LogoutTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logan', email='logan@email.com', password='123')

    # request to logout the user created at setup
    def test_logout(self):
        # logout user
        request = self.factory.get('/logout')
        AddMiddleware(request)

        # simulate authenticated user
        request.user = self.user
        response = logout(request)
        response.client = Client()

        # responds with redirect to /signin on success
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
