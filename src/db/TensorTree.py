import ZODB

storage = ZODB.FileStorage.FileStorage('matrixlistmodeldb.fs')
db = ZODB.DB(storage)
print(storage, db)


def getTensorTree():
    with db.transaction() as conn:
        return conn.root.model
