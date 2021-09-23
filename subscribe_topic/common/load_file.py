'''
@Author: xiaoming
@Date: 2018-12-01 11:42:43
@LastEditors: xiaoming
@LastEditTime: 2018-12-05 14:16:00
@Description: 用于读取yml或json文件中的内容
'''

import json
import os

import yaml



class LoadFile(object):
    '''
    把json或者yaml文件转为python字典或者列表字典
    @file:文件的绝对路径
    '''

    def __init__(self, file):
        if file.split('.')[-1] != 'yaml' and file.split('.')[-1] != 'json' and file.split('.')[-1] != 'yml':
            raise Exception("文件格式必须是yaml或者json")
        self.file = file

    def get_data(self):
        '''
        传入任意yaml或json格式的文件，调用该方法获取结果
        '''
        if self.file.split('.')[-1] == "json":
            return self.load_json()
        return self.load_yaml()

    def load_json(self):
        '''
        Convert json file to dictionary
        '''
        try:
            with open(self.file, encoding="utf-8") as f:
                result = json.load(f)
                if isinstance(result, list):
                    result = [i for i in result if i != '']
                return result
        except FileNotFoundError as e:
            raise e

    def load_yaml(self):
        '''
        Convert yaml file to dictionary
        '''
        try:
            with open(self.file, encoding="utf-8")as f:
                result = yaml.load(f)
                if isinstance(result, list):
                    result = [i for i in result if i != '']
                return result
        except FileNotFoundError as e:
            raise e




