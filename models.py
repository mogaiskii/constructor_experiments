import re

from sqlalchemy import String, Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        # PascalCase to snake_case
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name


class PolyBase(BaseModel):
    poly_type = Column(String)

    __mapper_args__ = {"polymorphic_on": poly_type}


class PolyOwner(BaseModel):
    poly_item_id = Column(Integer, ForeignKey(PolyBase.id))
    poly_item = relationship(PolyBase)


class PolyOne(PolyBase):
    id = Column(Integer, ForeignKey(PolyBase.id), primary_key=True)
    field_one = Column(Integer)

    __mapper_args__ = {"polymorphic_identity": "PolyOne"}


class PolyTwo(PolyBase):
    id = Column(Integer, ForeignKey(PolyBase.id), primary_key=True)
    field_two = Column(Integer)

    __mapper_args__ = {"polymorphic_identity": "PolyTwo"}


class TitleComponent(BaseModel):
    title = Column(VARCHAR(255))


class PriceComponent(BaseModel):
    price = Column(Integer)


class ComponentRelation(BaseModel):
    owner_id = Column(Integer, ForeignKey('components_owner.id'))

    component_type = Column(VARCHAR)
    title_id = Column(Integer, ForeignKey(TitleComponent.id))
    title = relationship(TitleComponent, lazy='joined')

    price_id = Column(Integer, ForeignKey(PriceComponent.id))
    price = relationship(PriceComponent, lazy='joined')

    @property
    def component(self):
        return getattr(self, self.component_type, None)


class ComponentsOwner(BaseModel):
    components = relationship(ComponentRelation, uselist=True, lazy='joined')
