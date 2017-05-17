#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-05-17 13:33:39
# Code:
'''
数据处理文件。
数据库中车牌信息存储格式：{'name':'车牌','typo':[0-50]}
'''
import functools
import random
import sqlite3
import string

PROVICE_ABBREVS = [
    '川', '云', '贵'
]

# 本地和远端数据库文件名
LOCAL_DB = './local.db'
REMOTE_DB = './remote.db'

# 数据库中表名
TABLE = 'cars'


def create(db, table):
    con = sqlite3.connect(db)
    con.execute('CREATE TABLE {} (name text, type integer)'.format(table))
    con.close()


@functools.lru_cache(maxsize=128)
def search(db, table, name):
    '在数据库中查询车牌为NAME的项目。'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE name=?'.format(table), (name,))
    return c.fetchall()


def search_local(name):
    return search(LOCAL_DB, TABLE, name)


def search_remote(name):
    return search(REMOTE_DB, TABLE, name)


def search_all(db, table):
    '返回所有。'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM {}'.format(table))
    return c.fetchall()


def update(db, table, name, typo):
    '将NAME和TYPO更新到数据库。'
    conn = sqlite3.connect(db)
    if not search(db, table, name):
        c = conn.cursor()
        c.execute("INSERT INTO {} values ('{}',{})".format(table, name, typo))
        conn.commit()
    conn.close()


def update_local(lsts):
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    for pair in lsts:
        update(LOCAL_DB, TABLE, pair[0], pair[1])
    conn.close()


def build_fake_datebase(db=REMOTE_DB, table=TABLE, num=10000):
    '创建模拟远程数据库。'
    name = ''
    for i in range(num):
        name = random.choice(PROVICE_ABBREVS)
        name += random.choice(string.ascii_uppercase)
        for j in range(5):
            name += random.choice(string.digits + string.ascii_uppercase)

        typo = random.randrange(2, 50)

        update(db, table, name, typo)


if __name__ == '__main__':
    # for db in LOCAL_DB, REMOTE_DB:
    #     create(db, TABLE)
    # create(LOCAL_DB, TABLE)
    # print(random.choice('abbrevs'))
    # build_fake_datebase()
    # update(REMOTE_DB, TABLE, '川A6882Q', 19)
    # update(REMOTE_DB, TABLE, '川A6926Q', 29)
    # update_local(search_remote('川A6882Q'))
    print(search_all(LOCAL_DB, TABLE))
