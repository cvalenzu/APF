from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only

Base = declarative_base()
Session = sessionmaker()

"""
    Check if record exists in database.

    :param session: The connection session
    :param model: The class of the model to be instantiated
    :param dict filter_by: attributes used to find object in the database
    :param dict kwargs: attributes used to create the object that are not used in filter_by

    :returns: True if object exists else False

"""


def check_exists(session, model, filter_by=None):
    return session.query(
        session.query(model).filter_by(**filter_by).exists()
    ).scalar()


def get_or_create(session, model, filter_by=None, **kwargs):
    """
    Initializes a model by creating it or getting it from the database if it exists

    Parameters
    ----------

    session : Session
        The connection session
    model : Model
        The class of the model to be instantiated
    filter_by : dict
        attributes used to find object in the database
    kwargs : dict
        attributes used to create the object that are not used in filter_by

    Returns
    ----------
    instance, created
        Tuple with the instanced object and wether it was created or not
    """
    instance = session.query(model).options(
        load_only(*filter_by.keys())).filter_by(**filter_by).first()
    if instance:
        return instance, False
    else:
        filter_by.update(kwargs)
        instance = model(**filter_by)
        session.add(instance)
        return instance, True


def update(instance, args):
    """
    Updates an object

    Parameter
    -----------

    instance : Model
        Object to be updated
    args : dict
        Attributes updated

    Returns
    ----------
    instance
        The updated object instance
    """
    for key in args.keys():
        setattr(instance, key, args[key])
    return instance


def get_session(db_config):
    """
    Gets the database session

    Parameters
    ------------

    db_config : dict
        Credentials to set up the database connection

    Returns
    -----------
    Session
        a session instance
    """
    psql_config = db_config["PSQL"]
    db_credentials = 'postgresql://{}:{}@{}:{}/{}'.format(
        psql_config["USER"], psql_config["PASSWORD"], psql_config["HOST"], psql_config["PORT"], psql_config["DB_NAME"])
    engine = create_engine(db_credentials)
    Session.configure(bind=engine)
    return Session()


def add_to_database(session, objects):
    """
    Adds objects to the database by adding them to the session.

    Parameters
    ------------

    session: Session
        Session object connected to the database
    objects: list/model
        Model instances to be added
    """
    if isinstance(objects, list):
        session.add_all(objects)
    else:
        session.add(objects)
    session.commit()


def bulk_insert(objects, model, session):
    """
    Inserts multiple objects to the database improving performance

    Parameters
    -----------

    objects : list
        Objects to be added
    model: Model
        Class of the model to be added
    session: Session
        Session instance 
    """
    session.bulk_insert_mappings(model, objects)


def query(session, model, page=None, page_size=None, total=None, sort_by=None, sort_desc=None, *params):
    offset = None
    limit = None
    if page and page_size:
        offset = page_size * (page -1)
        limit = page_size + offset
    sql_query = session.query(model).filter(*params)
    if not total:
        total = sql_query.order_by(None).count()
    if sort_by is not None:
        if sort_desc:
            sql_query.order_by(sort_by)
        else:
            sql_query.order_by(sort_by)
    results = sql_query[offset:limit]
    return {
        "total": total,
        "results": results
    }


def multiple_query(session, model1=None, model2=None, model3=None, page=None, page_size=None, total=None,
                   sort_by=None, sort_desc=None, *params):
    offset = None
    limit = None
    if page and page_size:
        offset = page_size * (page - 1)
        limit = page_size + offset
    if model3 is None:
        sql_query = session.query(model1,model2).filter(*params)
    else:
        sql_query = session.query(model1,model2,model3).filter(*params)
    if not total:
        total = sql_query.order_by(None).count()
    if sort_by is not None:
        if sort_desc:
            sql_query = sql_query.order_by(sort_by.desc())
        else:
            sql_query = sql_query.order_by(sort_by.asc())
    results = sql_query[offset:limit]
    return {
        "total": total,
        "results": results
    }

