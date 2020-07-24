#!/usr/bin/env python3

class NameNotFoundError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        return 