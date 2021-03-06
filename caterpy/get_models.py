#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Return models by category."""


import os
from glob import glob


def return_models(limit=-1, all_words=False, diff=False):
    """Return two dicts with model data and model data with unique words."""
    if all_words:
        models = [m for m in glob('/usr/local/etc/classifiers/pt_BR/*.data')]
    else:
        models = [m for m in glob('/usr/local/etc/classifiers/*.data')]
    _data_models = dict()

    for model in models:
        model_name = os.path.splitext(model.split('/')[-1])[0]
        _data_models[model_name] = []
        _list_models = []
        for item in list(filter(None, open(model, 'r').read().split('\n'))):
            _list_models.append([item.split("|")[0], int(item.split("|")[1])])
        for word, count in list(sorted(_list_models, key=lambda f: f[1],
                                       reverse=True)):
            _data_models[model_name].append(word)

    _intersect = list(set.intersection(
            *[set(_data_models[name]) for name in _data_models]))

    for model in _data_models:
        _data_models[model] = [name for name in _data_models[model]
                               if name not in _intersect][0:limit]

    if diff:
        _diff_models = dict()
        for model in _data_models:
            _diff_models[model] = list(set(_data_models[model]).difference(
                *[set(_data_models[name]) for name in _data_models
                  if name != model]))
        return _diff_models

    return _data_models
