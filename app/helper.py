import queue as Q
from app.models import Tag, SlackMessage
from app.models.message import Message
from app import app, db

def searchMessage(terms):
    q = Q.PriorityQueue(maxsize=10)
    messages = SlackMessage.query.all()

    '''
    Create a new Message object here to put in the queue
    because at the moment, it's easier to just create an object with the property
    `score`, rather than injecting score into SlackMessage model
    '''
    for message in messages:
        msg = Message(url=message.url,
                        description=message.description,
                        score=0,
                        tags=message.tags,
                        author=message.author,
                        annotator=message.annotator)
        text = msg.description.lower()
        tags = set()
        for tag in msg.tags:
            tags.add(tag.name)
        for term in terms:
            if term in text:
                msg.setScore(msg.getScore() + 1)
            for tag in tags:
                if term in tag or tag in term:
                    msg.setScore(msg.getScore() + 5)
        q.put(msg)
    
    return q

def saveMessage(url, description, message_text, author="None", annotator, tags):
    db_tags = []
    for tag in tags:
        tag_obj = Tag.query.filter_by(name=tag).first()
        if tag_obj:
            db_tags.append(tag_obj)
        else:
            new_tag = Tag(name=tag)
            db_tags.append(new_tag)
            db.session.add(new_tag)
    new_message = SlackMessage(url=url,
                               description=description,
                               message_text=message_text,
                               author=author,
                               annotator=annotator)
    new_message.tags.extend(db_tags)
    db.session.add(new_message)
    db.session.commit()

def deleteMessage(url):
    message = SlackMessage.query.filter_by(url=url).first()
    if message is None: 
        return False
    else:
        db.session.delete(message)
        db.session.commit()
        return True

def updateMessage(url, **args):
    message = SlackMessage.query.filter_by(url=url).first()
    description = args.get('description', None)
    if not description is None:
        message.description = description
    message_text = args.get('text', None)
    if not message_text is None:
        message.message_text = message_text
    tags = args.get('tags', None)
    if not tags is None:
        tag_name = set()
        for msg_tag in message.tags:
            tag_name.add(msg_tag.name)
        for tag in tags:
            if not tag in tag_name:
                new_tag = Tag(name=tag)
                db.session.add(new_tag)
                message.tags.append(new_tag)
    author = args.get('author', None)
    if not author is None:
        message.author = author
    annotator = args.get('annotator', None)
    if not annotator is None:
        message.annotator = annotator
    db.session.commit()

                    
            
        
    
