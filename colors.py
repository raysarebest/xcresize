import colorama

colorama.init()

def __module_for_background__(background):
    if background:
        return colorama.Back
    else:
        return colorama.Fore

def __terminate_color__(string, module):
    return string + module.RESET

def __colorize__(string, color, reset_colors, module):
    result = color + string
    if reset_colors:
        result = __terminate_color__(result, module)
    return result

def yellow(string, background=False, reset_colors=True):
    module = __module_for_background__(background)
    return __colorize__(string, module.YELLOW, reset_colors, module)

def green(string, background=False, reset_colors=True):
    module = __module_for_background__(background)
    return __colorize__(string, module.GREEN, reset_colors, module)

def red(string, background=False, reset_colors=True):
    module = __module_for_background__(background)
    return __colorize__(string, module.RED, reset_colors, module)