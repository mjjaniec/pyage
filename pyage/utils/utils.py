__author__ = 'mjjaniec'
import random


def rand_letter():
    return str(chr(random.randint(ord('a'), ord('z'))))


def rand_bool():
    return random.random() < 0.5