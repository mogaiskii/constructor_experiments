from api import ComponentRelationAbstract
from models import ComponentsRegistry, ComponentRelation


def test_components_realisation():
    existent_components = ComponentsRegistry.registry
    relations_map = ComponentRelation.get_relations_map()
    relation_realisation = set(relations_map.keys())
    assert existent_components == relation_realisation, 'all components should be registered as relation'

    for name in relations_map.values():
        assert name in ComponentRelationAbstract.__dict__, 'all components should have api realisation'
