from flask.ext.sqlalchemy import get_debug_queries
from flaskdepot.models import *

db.create_all()

banned = Usergroup(name=u'Banned', is_banned=True)
db.session.add(banned)

member = Usergroup(name=u'Member', is_default=True)
db.session.add(member)

admin = Usergroup(name=u'Admin', is_admin=True)
db.session.add(admin)

guest = Usergroup(name=u'Guest')
db.session.add(guest)

db.session.commit()

user_1 = User(username=u'Admin', group=admin)
user_1.set_password(u'admin')
db.session.add(user_1)

user_2 = User(username=u'Gebruiker', group=member)
user_2.set_password(u'gebruiker')
db.session.add(user_2)

broadcat = BroadCategory(name=u'TestBroadCategory')
db.session.add(broadcat)

db.session.commit()

narrwcat = NarrowCategory(name=u'TestNarrowCategory')
broadcat.narrow_categories = [narrwcat]
db.session.add(narrwcat)

db.session.commit()

file = File(name=u'TestFile', description=u'A test file', version=u'1.0', author=user_2,
            num_views=3, file_name='MyTestFile.zip', preview1_name='MyPrev.png', preview2_name='MyPrev.gif',
            broad_category=broadcat, narrow_category=narrwcat)
db.session.add(file)

db.session.commit()

comment = Comment(text=u'Some nice comment text. We love you!', file=file, user=user_1)
db.session.add(comment)

dl_1 = Download(last_downloaded=datetime.datetime.utcnow(), file=file, user=user_1)
dl_2 = Download(last_downloaded=datetime.datetime.utcnow(), file=file, user=user_2)

vote = Vote(value=-3, file=file, user=user_1)
vote = Vote(value=7, file=file, user=user_2)
vote = Vote(value=-2, file=file, user=user_1)

db.session.commit()

print(get_debug_queries())
