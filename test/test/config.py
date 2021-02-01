#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file config.py

class Config(object):
    DEBUG = True


class DevelopConfig(Config):
    pass


class ProduceConfig(Config):
    Debug = False


configs = {
    'develop': DevelopConfig,
    'produce': ProduceConfig
}
