import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))

db = scoped_session(sessionmaker(bind=engine))

db.execute('DROP TABLE users')
db.commit()

db.execute(
    'CREATE TABLE users ('
    'id SERIAL PRIMARY KEY, '
    'username VARCHAR NOT NULL, '
    'pw VARCHAR NOT NULL);'
)
db.commit()

db.execute(
    "INSERT INTO users (username, pw) VALUES ('benkawecki', 'benrules');"
)
db.commit()


print(db.execute("SELECT username FROM users WHERE username = 'benkawecki'")).fetchall()
print('finished!')
