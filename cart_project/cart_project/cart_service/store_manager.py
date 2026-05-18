from infrastructure.models import db, Product


class StoreManager:

    def add_to_store(self, item: Product) -> str:
        existing_item = db.session.execute(
            db.select(Product).filter_by(name=item.name)
        ).scalar_one_or_none()

        if existing_item:
            existing_item.quantity += item.quantity
        else:
            db.session.add(item)

        db.session.commit()

        return item.name

    def get_catalog(self) -> list[dict]:
        whole_catalog = db.session.execute(db.select(Product)).scalars().all()

        return [i.to_dict() for i in whole_catalog]
