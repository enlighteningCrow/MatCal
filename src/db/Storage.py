import ZODB.FileStorage

from utils import createPath
from pathlib import Path

createPath(Path('data'))

storage = ZODB.FileStorage.FileStorage(str(Path('data') / 'storage.fs'))
db = ZODB.DB(storage)
connection = db.open()


def getProperty(name: str, defaultValue: object):
    if name not in connection.root._root.data:
        connection.root.__setattr__(name, defaultValue)
    return connection.root.__getattr__(name)


def onExit():
    transaction = connection.transaction_manager.get()
    transaction.commit()
    connection.close()
    db.close()
