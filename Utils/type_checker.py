def type_check(name, var, req_typ):
    t = type(var)
    if t is not req_typ:
        raise TypeError(f"Invalid type for \'{name}\': Expected \'{req_typ.__qualname__}\' got \'{t.__qualname__}\'")


def type_check_num(name, var):
    t = type(var)
    if t is not float and t is not int:
        raise TypeError(f"Invalid type for \'{name}\': Expected \'float\' or \'int\' got \'{t.__qualname__}\'")


def types_check(name, var, *posib_types):
    t = type(var)
    for pos_typ in posib_types:
        if t is pos_typ: break
    else:
        ex = ", ".join(f"\'{t.__qualname__}\'" for t in posib_types[:-1])
        raise TypeError(
            f"Invalid type for {name}: Expected one of {ex} or \'{posib_types[-1].__qualname__}\' got \'{t.__qualname__}\'")