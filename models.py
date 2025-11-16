import json
from sqlalchemy import Column, String, Float, DateTime, Integer, Boolean, create_engine, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JSONList(TypeDecorator):
    """Custom type to store Python lists as JSON strings in SQLite"""
    impl = String
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

class Satellite(Base):
    __tablename__ = 'satellites'
    
    sat_id = Column(String, primary_key=True)
    norad_cat_id = Column(Float, unique=True, nullable=True)
    norad_follow_id = Column(Float, nullable=True)
    name = Column(String, nullable=False)
    names = Column(String, nullable=True)
    image = Column(String, nullable=True)
    status = Column(String, nullable=True)
    decayed = Column(DateTime, nullable=True)
    launched = Column(DateTime, nullable=True)
    deployed = Column(DateTime, nullable=True)
    website = Column(String, nullable=True)
    operator = Column(String, nullable=True)
    countries = Column(String, nullable=True)
    telemetries = Column(JSONList, nullable=True)  # Stores list as JSON
    updated = Column(DateTime, nullable=True)
    citation = Column(String, nullable=True)
    is_frequency_violator = Column(Boolean, default=False)
    associated_satellites = Column(JSONList, nullable=True)  # Stores list as JSON
    
    def __repr__(self):
        return f"<Satellite(sat_id={self.sat_id}, name={self.name}, status={self.status})>"
    
    def get_info(self):
        return f"Satellite({self.norad_cat_id}): {self.name}, Status: {self.status}, Launched: {self.launched}, Operator: {self.operator}, Countries: {self.countries}"

if __name__ == "__main__":
    engine = create_engine('sqlite:///satellites.db')
    Base.metadata.create_all(engine)