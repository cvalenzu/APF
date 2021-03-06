from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float, Boolean, JSON, Index, DateTime
from sqlalchemy.orm import relationship
from .. import generic
from sqlalchemy_serializer import SerializerMixin

taxonomy_class = Table('taxonomy_class', Base.metadata,
                       Column('class_name', String, ForeignKey('class.name')),
                       Column('taxonomy_name', String,
                              ForeignKey('taxonomy.name'))
                       )


class Class(Base, generic.AbstractClass, SerializerMixin):
    __tablename__ = 'class'

    name = Column(String, primary_key=True)
    acronym = Column(String)
    taxonomies = relationship(
        "Taxonomy",
        secondary=taxonomy_class,
        back_populates="classes")
    classifications = relationship("Classification")

    def get_taxonomies(self):
        return self.taxonomies

    def get_classifications(self):
        return self.classifications

    def __repr__(self):
        return "<Class(name='%s', acronym='%s')>" % (self.name, self.acronym)


class Taxonomy(Base, generic.AbstractTaxonomy, SerializerMixin):
    __tablename__ = 'taxonomy'

    name = Column(String, primary_key=True)
    classes = relationship(
        "Class",
        secondary=taxonomy_class,
        back_populates="taxonomies"
    )
    classifiers = relationship("Classifier")

    def get_classes(self):
        return self.classes

    def get_classifiers(self):
        return self.classifiers

    def __repr__(self):
        return "<Taxonomy(name='%s')>" % (self.name)


class Classifier(Base, generic.AbstractClassifier, SerializerMixin):
    __tablename__ = 'classifier'
    name = Column(String, primary_key=True)
    taxonomy_name = Column(String, ForeignKey('taxonomy.name'))
    classifications = relationship("Classification")

    def get_classifications(self):
        return self.classifications

    def __repr__(self):
        return "<Classifier(name='%s')>" % (self.name)


class AstroObject(Base, generic.AbstractAstroObject, SerializerMixin):
    __tablename__ = 'astro_object'

    oid = Column(String, primary_key=True)
    nobs = Column(Integer)
    meanra = Column(Float)
    meandec = Column(Float)
    sigmara = Column(Float)
    sigmadec = Column(Float)
    deltajd = Column(Float)
    lastmjd = Column(Float)
    firstmjd = Column(Float)

    __table_args__ = (
        Index("object_nobs", "nobs", postgresql_using="btree"),
        Index("object_firstmjd", "firstmjd", postgresql_using="btree"),
        Index("object_lastmjd", "lastmjd", postgresql_using="btree"),
    )

    xmatches = relationship("Xmatch")
    magnitude_statistics = relationship("MagnitudeStatistics", uselist=False)
    classifications = relationship("Classification")
    non_detections = relationship("NonDetection")
    detections = relationship("Detection")
    features = relationship("FeaturesObject")

    def get_classifications(self):
        return self.classifications

    def get_magnitude_statistics(self):
        return self.magnitude_statistics

    def get_xmatches(self):
        return self.xmatches

    def get_non_detections(self):
        return self.non_detections

    def get_detections(self):
        return self.detections

    def get_features(self):
        return self.features

    def get_lightcurve(self):
        return {
            "detections": self.get_detections(),
            "non_detections": self.get_non_detections()
        }

    def __repr__(self):
        return "<AstroObject(oid='%s')>" % (self.oid)


class Classification(Base, generic.AbstractClassification, SerializerMixin):
    __tablename__ = 'classification'

    astro_object = Column(String, ForeignKey(
    'astro_object.oid'), primary_key=True)
    classifier_name = Column(String, ForeignKey(
    'classifier.name'), primary_key=True)
    class_name = Column(String, ForeignKey('class.name'), primary_key=True)
    probability = Column(Float)
    probabilities = Column(JSON)

    classes = relationship("Class", back_populates='classifications')
    objects = relationship("AstroObject", back_populates='classifications')
    classifiers = relationship("Classifier", back_populates='classifications')

    def __repr__(self):
        return "<Classification(class_name='%s', probability='%s', astro_object='%s', classifier_name='%s')>" % (self.class_name,
                                                                                                                 self.probability, self.astro_object, self.classifier_name)


class Xmatch(Base, generic.AbstractXmatch, SerializerMixin):
    __tablename__ = 'xmatch'

    oid = Column(String, ForeignKey('astro_object.oid'))
    catalog_id = Column(String, primary_key=True)
    catalog_oid = Column(String, primary_key=True)


class MagnitudeStatistics(Base, generic.AbstractMagnitudeStatistics, SerializerMixin):
    __tablename__ = 'magnitude_statistics'

    oid = Column(String, ForeignKey('astro_object.oid'), primary_key=True)
    magnitude_type = Column(String, primary_key=True)
    fid = Column(Integer, primary_key=True)
    mean = Column(Float)
    median = Column(Float)
    max_mag = Column(Float)
    min_mag = Column(Float)
    sigma = Column(Float)
    last = Column(Float)
    first = Column(Float)

    __table_args__ = (
        Index('mag_mean', 'mean', postgresql_using='btree'),
        Index('mag_median', 'median', postgresql_using='btree'),
        Index('mag_min', 'min_mag', postgresql_using='btree'),
        Index('mag_max', 'max_mag', postgresql_using='btree'),
        Index('mag_first', 'first', postgresql_using='btree'),
        Index('mag_last', 'last', postgresql_using='btree'))


class Features(Base, generic.AbstractFeatures, SerializerMixin):
    __tablename__ = 'features'

    version = Column(String, primary_key=True)


class FeaturesObject(Base, SerializerMixin):
    __tablename__ = 'features_object'

    object_id = Column(String, ForeignKey(
    'astro_object.oid'), primary_key=True)
    features_version = Column(String, ForeignKey(
        'features.version'), primary_key=True)
    data = Column(JSON)
    features = relationship("Features")


class NonDetection(Base, generic.AbstractNonDetection, SerializerMixin):
    __tablename__ = 'non_detection'

    oid = Column(String, ForeignKey('astro_object.oid'), primary_key=True)
    fid = Column(Integer, primary_key=True)
    datetime = Column(DateTime,primary_key=True)
    mjd = Column(Float,nullable=False)
    diffmaglim = Column(Float, nullable=False)
    __table_args__ = (Index('non_det_oid', 'oid', postgresql_using='hash'),)

class Detection(Base, generic.AbstractDetection, SerializerMixin):
    __tablename__ = 'detection'

    candid = Column(String, primary_key=True)
    mjd = Column(Float, nullable=False)
    fid = Column(Integer, nullable=False)
    magpsf = Column(Float, nullable=False)
    magpsf_corr = Column(Float)
    magap = Column(Float, nullable=False)
    magap_corr = Column(Float)
    sigmapsf = Column(Float, nullable=False)
    sigmapsf_corr = Column(Float)
    sigmagap = Column(Float, nullable=False)
    sigmagap_corr = Column(Float)
    ra = Column(Float, nullable=False)
    dec = Column(Float, nullable=False)
    rb = Column(Float)
    alert = Column(JSON, nullable=False)
    oid = Column(String, ForeignKey('astro_object.oid'), nullable=False)
    avro = Column(String)

    __table_args__ = (Index('object_id', 'oid', postgresql_using='hash'),)

class OutlierDetector(Base, generic.AbstractOutlierDetector, SerializerMixin):
    __tablename__ = 'outlier_detector'

    name = Column(String, primary_key=True)

class OutlierScore(Base, generic.AbstractOutlierScore, SerializerMixin):
    __tablename__ = 'outlier_score'
    astro_object = Column(String, ForeignKey(
    'astro_object.oid'), primary_key=True)
    detector_name = Column(String, ForeignKey(
    'outlier_detector.name'), primary_key=True)
    score = Column(Float, primary_key=True)
    scores = Column(JSON)
