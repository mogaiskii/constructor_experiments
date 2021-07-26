from models import ComponentsOwner, BaseComponent
from services.component_relation import component_relation_factory


class ComponentsOwnerBuilder:
    def __init__(self, product: ComponentsOwner = None):
        if product is None:
            product = ComponentsOwner()

        self._product = product

    def add_component(self, component: BaseComponent):
        relation = component_relation_factory(component)
        order = len(self._product.components)
        relation.order = order
        self._product.components.append(relation)

        if component.index_as:
            self._product.make_index(component)

    @property
    def product(self):
        return self._product
