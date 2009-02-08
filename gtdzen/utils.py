from sqlalchemy.orm.exc import NoResultFound

def get_or_create(model, **kwargs):
    try:
        return model.query.filter_by(**kwargs).one()
    except NoResultFound:
        return model(**kwargs)
