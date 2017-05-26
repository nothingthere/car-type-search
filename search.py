#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-05-17 12:18:41
# Code:
'''
入口文件。
数据库车牌信息格式：{'name':'....', 'type':[2-50]}
'''


import re

import data

# 匹配车牌的正则对象
REGEX = re.compile(
    '^[{}][A-Z][0-9a-z]{{5}}$'.format('|'.join(data.PROVICE_ABBREVS)), flags=re.IGNORECASE)


def is_valid(name):
    '判断车牌格式是否正确。'
    return REGEX.match(name)


def normalize_name(name):
    '检查车牌格式是否正确，并返回大写形式。'
    if is_valid(name):
        return str.upper(name)
    else:
        return None


def delete(name):
    '删除本地数据库车牌。'
    pass


def cache_to_local_db(result):
    '将远端数据库搜索到的车牌添加到本地数据库。'
    # print('缓存到本地')
    data.update_local(result)


def search_in_local_db(name):
    '在本地数据库查找。'
    # print('在本地查找')
    return data.search_local(name)


def search_in_remote_db(name):
    '在远端数据库查找。'
    # print('在远端查找')
    return data.search_remote(name)


def search(name):
    '查询并返回车牌信息。'
    result = None

    name = normalize_name(name)
    if not name:
        return '车牌格式错误。'

    # 先在本地数据库查找
    result = search_in_local_db(name)
    if result:
        return result

    # 否则在远端查找，如果找到则将其添加到本地数据库
    result = search_in_remote_db(name)
    if result:
        cache_to_local_db(result)

    return result


def show_result(lsts):
    for pair in lsts:
        print('车牌：{pair[0]}\t座位数：{pair[1]}'.format(pair=pair))


if __name__ == '__main__':
    def test(name):
        res = search(name)
        if isinstance(res, str):
            raise ValueError(res)
        if res:
            show_result(res)
        else:
            print('没找到：{}'.format(name))

    print('测试少量车牌：')
    for name in ['川a6882q', '川a6926q']:
        test(name)

    print('-' * 50)
    print('测试存在数据库中的大量车牌：')
    for pair in data.search_all(data.REMOTE_DB, data.TABLE)[0:10]:
        test(pair[0])

    print('-' * 50)
    print('测试随机车牌：')
    for i in range(10):
        test(data.random_data_item()[0])
