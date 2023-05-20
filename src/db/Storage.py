import ZODB.FileStorage

# from utils import createPath
from src.utils import createPath
from pathlib import Path

createPath(Path('data'))

storage = ZODB.FileStorage.FileStorage(str(Path('data') / 'storage.fs'))
db = ZODB.DB(storage)
connection = db.open()
# print(storage, db)


def getProperty(name: str, defaultValue: object):
    # print(connection.root)
    # if not connection.root.__contains__(name):
    # print(connection.root.__dir__())
    # print(connection.root[name])
    # if name not in connection.root:
    # if not connection.root.__contains__(name):
    # if not connection.root.has_key(name):
    # if not connection.root.items():
    #     connection.root[name] = defaultValue
    # print(connection.root.__getattr__(name))
    if name not in connection.root._root.data:
        connection.root.__setattr__(name, defaultValue)
        # connection.root[name] = defaultValue
    return connection.root.__getattr__(name)


def onExit():
    transaction = connection.transaction_manager.get()
    transaction.commit()
    connection.close()
    db.close()


# def getTensorDict():
#     with db.transaction() as conn:
#         if 'root' in (conn.__dir__()):
#             print("has root")
#             if 'tensorDict' in (conn.root.__dir__()):
#                 print("has tensorDict")
#                 return conn.root.TensorDict
#         # return conn.root.
