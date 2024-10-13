from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary, Boolean, BigInteger
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='RESTRICT'))
    topic_id = Column(Integer, ForeignKey('topic.id', ondelete='RESTRICT'))

    responses = relationship('Response', back_populates='question', cascade='all, delete')

    def __repr__(self):
        return f"<Question(id={self.id}, question_text={self.question_text[:20]})>"

class Response(Base):
    __tablename__ = 'response'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
    response_text = Column(Text)
    image = Column(LargeBinary)

    question = relationship('Question', back_populates='responses')

    def __repr__(self):
        return f"<Response(id={self.id}, question_id={self.question_id}, response_text={self.response_text[:20]})>"
    
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)