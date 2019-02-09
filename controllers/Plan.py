#!/usr/bin/env python

from library.Classes import Classes


class PlanController(Classes.BaseMinix):
    default_method = 'test'

    def test(self, one, two, three="hello"):
        print(one)
        print(two)
        print(three)
