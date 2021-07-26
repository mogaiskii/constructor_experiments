import re
from functools import lru_cache
from typing import Dict

from sqlalchemy import String, Column, Integer, ForeignKey, VARCHAR, Boolean
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


class ComponentsRegistry(type(BaseModel)):
    registry = set()
    def __new__(mcls, name, bases, attrs):
        new_cls = super().__new__(mcls, name, bases, attrs)

        if '__abstract__' not in attrs:
            ComponentsRegistry.registry.add(new_cls)

        return new_cls


class BaseComponent(BaseModel, metaclass=ComponentsRegistry):
    __abstract__ = True
    __value_field__ = None

    unique = Column(Boolean)  # should be checked on owner level
    nullable = Column(Boolean)
    index_as = Column(VARCHAR)  # should be set on owner level

    def validate(self):
        if not self.nullable and self.__value_field__:
            assert getattr(self, self.__value_field__, None) is not None


class TitleComponent(BaseComponent):
    title = Column(VARCHAR(255))


class PriceComponent(BaseComponent):
    price = Column(Integer)


class ComponentRelation(BaseModel):
    owner_id = Column(Integer, ForeignKey('components_owner.id'))
    order = Column(Integer)

    component_type = Column(VARCHAR)
    title_id = Column(Integer, ForeignKey(TitleComponent.id))
    title = relationship(TitleComponent, lazy='joined')

    price_id = Column(Integer, ForeignKey(PriceComponent.id))
    price = relationship(PriceComponent, lazy='joined')

    @property
    def component(self) -> BaseComponent:
        return getattr(self, self.component_type, None)

    @component.setter
    def component(self, component):
        rel_map = self.get_relations_map()

        relation = rel_map.get(component)
        assert relation is not None, 'There is no relation for this component'

        setattr(self, relation, component)
        self.component_type = relation

    @classmethod
    @lru_cache
    def get_relations_map(cls) -> Dict[BaseComponent, str]:
        items = cls.__mapper__.relationships.items()
        class_getter = lambda rel: rel.mapper.class_
        return {class_getter(relation): name for name, relation in items}


class ComponentsOwner(BaseModel):
    components = relationship(ComponentRelation, uselist=True, lazy='joined', order_by=ComponentRelation.order)

    def make_index(self, component: BaseComponent):
        setattr(self, component.index_as, component)
