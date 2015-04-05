def enum(*sequential, **named):
    if len(sequential) > 0:
        if isinstance(sequential[0], tuple):
            identifiers = [pair[0] for pair in sequential]
            enum_values = [pair[1] for pair in sequential]
        else:
            identifiers = sequential
            enum_values = range(len(sequential))

    enums = dict(zip(identifiers, enum_values), **named)
    return type('Enum', (), enums)
