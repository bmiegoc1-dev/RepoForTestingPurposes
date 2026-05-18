

class UserNotFoundError(Exception):
    """Raised when a user_id does not exist in the database."""
    pass


class CartEmptyError(Exception):
    """Raised when a user exists but their cart has no items."""
    pass


class ProductNotFoundError(Exception):
    """Raised when a product_id does not exist in the database."""
    pass