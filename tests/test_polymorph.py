import traceback

from sqlalchemy.orm import Session

from models import PolyOwner, PolyOne, PolyTwo


def test_smoke_polymorph(session: Session):
    try:
        owner_one = PolyOwner()
        owner_two = PolyOwner()

        poly_one = PolyOne(field_one=111)
        poly_two = PolyTwo(field_two=222)

        owner_one.poly_item = poly_one
        owner_two.poly_item = poly_two

        session.add_all([owner_one, owner_two])
        session.commit()
    except Exception as e:
        traceback.print_exc()
        assert False, e
    else:
        assert owner_one.poly_item_id == poly_one.id
        assert poly_one.id is not None
        assert owner_two.poly_item_id == poly_two.id
        assert poly_two.id is not None


def test_multiple_polymorph(session: Session):
    try:
        owner_one = PolyOwner()
        owner_two = PolyOwner()

        poly_one = PolyOne(field_one=111)
        poly_two = PolyOne(field_one=222)

        owner_one.poly_item = poly_one
        owner_two.poly_item = poly_two

        session.add_all([owner_one, owner_two])
        session.commit()

        owner_one_from_db = session.query(PolyOwner).filter(PolyOwner.id == owner_one.id).one()
        owner_two_from_db = session.query(PolyOwner).filter(PolyOwner.id == owner_two.id).one()

        assert owner_one_from_db.poly_item_id == poly_one.id
        assert owner_two_from_db.poly_item_id == poly_two.id
        assert owner_one_from_db.poly_item.field_one == poly_one.field_one
        assert owner_two_from_db.poly_item.field_one == poly_two.field_one
    except Exception as e:
        traceback.print_exc()
        assert False, e
