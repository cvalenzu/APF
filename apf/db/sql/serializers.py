from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from apf.db.sql.models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ClassSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Class

    name = ma.auto_field()
    acronym = ma.auto_field()

class TaxonomySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Taxonomy

    name = ma.auto_field()

class ClassifierSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Classifier

    name = ma.auto_field()
    taxonomy_name = ma.auto_field()

class AstroObjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AstroObject

    oid = ma.auto_field()
    nobs = ma.auto_field()
    meanra = ma.auto_field()
    meandec = ma.auto_field()
    sigmara = ma.auto_field()
    sigmadec = ma.auto_field()
    deltajd = ma.auto_field()
    lastmjd = ma.auto_field()
    firstmjd = ma.auto_field()

class ClassificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Classification

    astro_object = ma.auto_field()
    classifier_name = ma.auto_field()
    class_name = ma.auto_field()
    probability = ma.auto_field()
    probabilities = ma.auto_field()

class MagnitudeStatisticsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MagnitudeStatistics

    oid = ma.auto_field()
    magnitude_type = ma.auto_field()
    fid = ma.auto_field()
    mean = ma.auto_field()
    median = ma.auto_field()
    max_mag = ma.auto_field()
    min_mag = ma.auto_field()
    sigma = ma.auto_field()
    last = ma.auto_field()
    first = ma.auto_field()

class FeaturesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FeaturesObject

    object_id = ma.auto_field()
    features_version = ma.auto_field()
    data = ma.auto_field()
