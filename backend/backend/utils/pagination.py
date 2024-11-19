def get_pagination_data(page: int, per_page: int = 10):
    """
    Calculate skip and limit for pagination.

    Args:
        page (int): The current page number (1-indexed).
        per_page (int): Number of items per page. Default is 10.

    Returns:
        tuple: A tuple containing 'skip' and 'limit'.
    """
    if page < 1:
        raise ValueError('Page number must be greater than or equal to 1.')
    if per_page < 1:
        raise ValueError('Items per page must be greater than or equal to 1.')

    skip = (page - 1) * per_page
    limit = per_page

    return skip, limit
