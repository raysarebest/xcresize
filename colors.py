import colorama

colorama.init()

def __module_for_background__(background):
    if background:
        return colorama.Back
    else:
        return colorama.Fore

def __terminate_color__(string, module):
    return string + module.RESET

def yellow(string, background=False):
    module = __module_for_background__(background)
    return __terminate_color__(module.YELLOW + string, module)

def green(string, background=False):
    module = __module_for_background__(background)
    return __terminate_color__(module.GREEN + string, module)

def red(string, background=False):
    module = __module_for_background__(background)
    return __terminate_color__(module.RED + string, module)