#!/usr/bin/python

from file_operations import get_full_path_to_log_directory

def log_error_to_file(function, message):
    with open(get_full_path_to_log_directory() + "log.txt", "a") as log_file:
        log_file.write("Function: %s - log message: %s \r\n" % (function, message))

