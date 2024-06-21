

class CollectionError(Exception):
    '''Just used to help understand what is happening while reading the code.'''
    pass

class ParameterError(Exception):
    '''A error that doesn't have a major impact coming from a Parameter not being what was expected.'''
    pass