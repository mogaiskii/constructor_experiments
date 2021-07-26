from models import BaseComponent, ComponentRelation


def component_relation_factory(component: BaseComponent) -> ComponentRelation:
    component_relation = ComponentRelation()
    component_relation.component = component

    return component_relation
