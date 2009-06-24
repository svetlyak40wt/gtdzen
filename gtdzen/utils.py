# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

def get_or_create(model, **kwargs):
    from sqlalchemy.orm.exc import NoResultFound
    try:
        return model.query.filter_by(**kwargs).one()
    except NoResultFound:
        return model(**kwargs)

def make_list(str_or_list):
    '''Makes list from a string or passes argument as is.'''
    if isinstance(str_or_list, basestring):
        return [str_or_list,]
    return str_or_list

