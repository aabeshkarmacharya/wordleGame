from termcolor import colored


def correct_letter(text):
    return colored(f" {text} ", on_color="on_green")


def present_letter(text):
    return colored(f" {text} ", on_color="on_yellow")


def absent_letter(text):
    return colored(f" {text} ", on_color="on_red")


def light_blue(text):
    return colored(text, "light_blue")


def cyan(text):
    return colored(text, "cyan")


def blue(text):
    return colored(text, "blue")


def red(text):
    return colored(text, "red")


def dark_grey(text):
    return colored(text, "dark_grey")


def black(text):
    return colored(text, "black")


def green(text):
    return colored(text, "green")
