# Group-4
V1 of the social book app Documentation

Team members names/ netID/ GitHub email: <br />
  Andrew Banks      - alb1424 - godzillamaster58127@gmail.com <br />
  Calvin Brinkman   - cdb1055 - calvinbrinkman30@gmail.com <br />
  Colin klein       - cik14   - colink7112@yahoo.com <br />
  Rojal Bishwokarma - rb2298  - Rojalbaraily07@gmail.com <br />
  Logan Christopher - clc1085 - logan.christopher@comcast.net <br />

Overall objective of the project: <br />
The objective is to create a facebook like social media app/ website <br />
it's functions for the website/app as listed are:
  1. Users should be able to login into their account to be able to access his/her timeline 
  2. Users should be able to compose,edit, and post on his\her timeline
  3. Users should be able to send and accept friend request from others which allows them to see their timelines
  4. Users should be able to like, comment, and share status of their timeline
  
Programmin languages/ tool use to bulid the website: <br />
Django as the web based framework use to create the website  <br />
Python- the language the team will use <br />
Pycharm- as the IDE to use Django <br />

Roles for the Team: <br />
Andrew Banks- Team Manager <br />
Calvin Brinkman- Researcher <br />
Colin Klein- Frontend Developer <br />
Rojal Bishwokarma- Backend Developer <br />
Logan Christopher- Developer <br />

Build & Run: <br />
// create virtual environment & install dependencies <br />
python -m venv . <br />
source bin/activate <br />
python -m pip install Django <br />
python -m pip install Pillow <br />

// Creates db tables & run server <br />
manage.py migrate --run-syncdb <br />
python manage.py runserver <br />

When changing database models apply migrations before running server again: <br />
python manage.py migrate <br />
python manage.py runserver <br />

Testing: <br />
python manage.py test core <br />