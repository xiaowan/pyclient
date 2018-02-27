#!/usr/bin/env python

from .Base import BaseController


class PlanController(BaseController):
    default_method = 'test'

    def test(self, one, two, three="hello"):
        print(one)
        print(two)
        print(three)