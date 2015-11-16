#!/usr/bin/env python
# coding: utf-8
"""
Created On Nov 19, 2013

@Author : Jun Wang
"""

class MQError(Exception):
    """
    This exception raised when decode error.
    """
    def __init__(self, message):
        super(MQError, self).__init__(message)
        self.message = message

    def __str__(self):
        return "Message Queue error: %s" % self.message
