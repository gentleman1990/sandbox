#!/usr/bin/python

import os


FULL_PATH_TO_LOGS = os.path.dirname(os.path.realpath(__file__)) + "/logs/"


def log_error_to_file(function, message):
    with open(FULL_PATH_TO_LOGS + "log.txt", "a") as log_file:
        log_file.write(("Function: %s - log message: %s \r\n")%(function, message))