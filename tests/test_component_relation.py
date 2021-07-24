import traceback

from sqlalchemy.orm import Session

from models import TitleComponent, PriceComponent, ComponentRelation, ComponentsOwner


def test_smoke_component_relation(session: Session):
    try:
        title = TitleComponent(title='abc')
        price = PriceComponent(price=123)

        rel_1 = ComponentRelation(component_type='title')
        rel_1.title = title

        rel_2 = ComponentRelation(component_type='price')
        rel_2.price = price

        session.add_all([rel_1, rel_2])
        session.commit()

    except Exception as e:
        traceback.print_exc()
        assert False, e

    else:
        assert title.id is not None
        assert price.id is not None

        assert rel_1.title_id == title.id
        assert rel_2.price_id == price.id

        assert rel_1.component.id == title.id
        assert rel_2.component.id == price.id

        assert rel_1.price_id is None
        assert rel_2.title_id is None


def test_smoke_components_owner(session: Session):
    try:
        title = TitleComponent(title='abc')
        price = PriceComponent(price=123)

        rel_1 = ComponentRelation(component_type='title')
        rel_1.title = title

        rel_2 = ComponentRelation(component_type='price')
        rel_2.price = price

        owner = ComponentsOwner()
        owner.components = [rel_1, rel_2]

        session.add(owner)
        session.commit()

    except Exception as e:
        traceback.print_exc()
        assert False, e

    else:
        assert title.id is not None
        assert price.id is not None

        assert rel_1.title.id == title.id
        assert rel_2.price.id == price.id

        assert owner.components is not None
        assert len(owner.components) == 2

        for component_item in owner.components:
            component = component_item.component
            if isinstance(component, TitleComponent):
                assert component.id == title.id
            elif isinstance(component, PriceComponent):
                assert component.id == price.id
            else:
                assert False, 'unknown type of component'
