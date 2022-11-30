from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowersCount,Comment,EventPost,AttendingEvent,RvspEvent
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = [request.user.username]
    feed = []


    user_following = FollowersCount.objects.filter(follower=request.user.username, re=1)
    userss_following = FollowersCount.objects.filter(user=request.user.username, re=1)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # event post display
    event_following = EventPost.objects.filter(po_lvl=0)
    ww = []
    event = []
    for users in event_following:
        ww.append(users.user)

    for usernames in ww:
        ee = EventPost.objects.filter(user=usernames,po_lvl=0)
        event.append(ee)
    event_list = list(chain(*event))

    # comment section
    comments = []

    for posts in feed_list:
        comment_list = Comment.objects.filter(post_id=posts.id)
        comments.append(comment_list)

    post_comments = list(chain(*comments))
    
    # user-suggestion start
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if(x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'events': event_list,'posts': feed_list,'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'post_comments': post_comments})

@login_required(login_url='signin')
def events(request):
    if request.method =='POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        location = request.POST['location']
        ans = request.POST['answer']
        if ans == 'public':
            ## when the user wants the post to appear in every user post feed
            new_event = EventPost.objects.create(user=user, image=image,po_lvl=0,location=location, caption=caption)
            new_event.id_str = new_event.id
            new_event.save()
        elif ans == 'private':
            ## when the user wants only the people who follow the user to see the event
            new_event = EventPost.objects.create(user=user, image=image,po_lvl=0, location=location, caption=caption)
            new_event.id_str = new_event.id
            new_event.save()
    return redirect('/')

@login_required(login_url='signin')
def attendingEvent(request):
    username = request.user.username
    event_id = request.GET.get('event_id')

    event = EventPost.objects.get(id=event_id)

    like_filter = AttendingEvent.objects.filter(event_id=event_id, username=username).first()
    if like_filter == None:
        new_attend = AttendingEvent.objects.create(event_id=event_id, username=username)
        new_attend.save()
        event.no_of_attending = event.no_of_attending + 1
        event.save()
        return redirect('/')
    else:
        like_filter.delete()
        event.no_of_attending = event.no_of_attending - 1
        event.save()
        return redirect('/')

@login_required(login_url='signin')
def rsvpEvent(request):
    username = request.user.username
    event_id = request.GET.get('event_id')

    event = EventPost.objects.get(id=event_id)

    like_filter = RvspEvent.objects.filter(event_id=event_id, username=username).first()
    if like_filter == None:
        new_attend = RvspEvent.objects.create(event_id=event_id, username=username)
        new_attend.save()
        event.no_of_rvsp = event.no_of_rvsp + 1
        event.save()
        return redirect('/')
    else:
        like_filter.delete()
        event.no_of_rvsp = event.no_of_rvsp - 1
        event.save()
        return redirect('/')

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = EventPost.objects.create(user=user, image=image, caption=caption)
        new_post.id_str = new_post.id
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []
        for users in username_object:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_list =  Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))
    return render(request,'search.html',{'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def listss(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    username = request.user.username
    if request.method == 'POST':
        follower = request.POST['type']
        if follower == 'followers':
            user_following = FollowersCount.objects.filter(re=1)

            user_following_all = []
            all_users = User.objects.all()
            feed = []
            for user in user_following:
                user_list = User.objects.get(username=user.user)
                user_following_all.append(user_list)
            new_suggestions_list = [x for x in list(all_users) if (len(FollowersCount.objects.filter(user=request.user.username, re=1, follower=x)) == 1)]
            current_user = User.objects.filter(username=request.user.username)
            final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]

            username_profile = []
            usernames_profile_list = []

            for users in final_suggestions_list:
                username_profile.append(users.id)

            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)
                usernames_profile_list.append(profile_lists)
            username_profile_list = list(chain(*usernames_profile_list))
        elif follower == 'following':
            user_following = FollowersCount.objects.filter(re=1)

            user_following_all = []
            all_users = User.objects.all()
            feed = []
            for user in user_following:
                user_list = User.objects.get(username=user.user)
                user_following_all.append(user_list)
            new_suggestions_list = [x for x in list(all_users) if (len(FollowersCount.objects.filter(user=x, re=1, follower=request.user.username)) == 1)]
            current_user = User.objects.filter(username=request.user.username)
            final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]

            username_profile = []
            usernames_profile_list = []

            for users in final_suggestions_list:
                username_profile.append(users.id)

            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)
                usernames_profile_list.append(profile_lists)
            username_profile_list = list(chain(*usernames_profile_list))

    return render(request,'search.html',{'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter ==None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    comments = []

    for posts in user_posts:
        comment_list = Comment.objects.filter(post_id=posts.id)
        comments.append(comment_list)

    post_comments = list(chain(*comments))

    follower = request.user.username
    user = pk

    user_following = FollowersCount.objects.filter(re=2)

    user_following_all = []
    all_users = User.objects.all()
    feed = []
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [x for x in list(all_users) if (len(FollowersCount.objects.filter(user=request.user.username, re=2,follower=x))==1)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    suggestions_username_profile_list = list(chain(*username_profile_list))


    if 1 == len(FollowersCount.objects.filter(follower=follower, re=2, user=pk)):
        user_re = 2
    elif len(FollowersCount.objects.filter(follower=follower, re=1, user=pk)) == 1:
        user_re = 1
    else:
        user_re = 0

    user_followers = len(FollowersCount.objects.filter(user=pk, re=1))
    user_following = len(FollowersCount.objects.filter(follower=pk, re=1))
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'user_followers': user_followers,
        'user_following': user_following,
        'user_re': user_re,
        'suggestions_username_profile_list': suggestions_username_profile_list,
        'post_comments': post_comments,
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            FollowersCount.re = 0
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()

            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, re=2, user=user)
            new_follower.save()


            return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def comment_post(request):
    if request.method == 'POST':
        username = request.user.username
        post_id = request.POST.get('post-id')
        text = request.POST['text']

        comment = Comment.objects.create(post_id=post_id, username=username, text=text)
        comment.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def delete(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    comment_txt = request.GET.get('comment_txt')

    if post_id != None:
        post = Post.objects.get(id=post_id)
        if post.user == username:
            post.delete()
    elif comment_txt != None:
        comment = Comment.objects.filter(text=comment_txt, username=username).first()
        if comment != None:
            comment.delete()

    return redirect('/')

@login_required(login_url='signin')
def edit(request):
    if request.method == 'POST':
        username = request.user.username
        post_id = request.POST.get('post_id')

        post = Post.objects.get(id=post_id)
        if post.user == username:
            image = request.FILES.get('image_upload')
            caption = request.POST['caption']

            if image:
                post.image = image
            if caption:
                post.caption = caption
            post.save()

    return redirect('/')

@login_required(login_url='signin')
def share(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    new_post = Post.objects.get(id=post_id)
    new_post.pk = None
    if new_post.o_user == "":
        new_post.o_user = new_post.user

    new_post.no_of_likes = 0
    new_post.user = username
    new_post.save()
    new_post.id_str = new_post.id
    new_post.save()

    return redirect('/')

def friends(request):
    if request.method == 'POST':
        user = request.user.username
        follower = request.POST['follower']
        ans = request.POST['answer']
        if ans == 'yes':
            if FollowersCount.objects.filter(user=user, re=2, follower=follower):
                new_follower = FollowersCount.objects.create(follower=follower, re=1, user=user)
                new_follower.save()
                delete_follower = FollowersCount.objects.get(follower=follower, re=2, user=user)
                delete_follower.delete()

        elif ans == 'no':
            if FollowersCount.objects.filter(user=user, re=2, follower=follower):
                delete_follower = FollowersCount.objects.get(follower=follower, re=2, user=user)
                delete_follower.delete()

        return redirect('/profile/'+user)


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            birthday = request.POST['birthday']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.birthday = birthday
            user_profile.user.first_name = first_name
            user_profile.user.last_name = last_name
            user_profile.user.save()
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            birthday = request.POST['birthday']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.birthday = birthday
            user_profile.user.first_name = first_name
            user_profile.user.last_name = last_name
            user_profile.user.save()
            user_profile.save()
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        birthday = request.POST['birthday']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                ## login the user to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, birthday=birthday, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invaild')
            return redirect('signin')

    return render(request, "signin.html")

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
