#!/usr/bin/env python

from app import app, db
from app.models import Tag, SlackMessage

db.create_all()

tag = Tag(name='sample')
message = SlackMessage(url='https://optimizely.slack.com/archives/CEC864U4B/p1563377721005600',
                       description='Some message from #backend-infra',
                       message_text='In late this AM, in by lunch',
                       author='trent.robbins',
                       annotator='yuan.chen')

db.session.add(tag)
db.session.add(message)
message.tags.append(tag)

db.session.commit()
