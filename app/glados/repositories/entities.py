from glados.models import Entity

def get_entities(filters):
    query = Entity.query

    # @NOTE:
    # `EntitiesRequestSerializer` validate the arguments of get_entities function,
    # perhaps we could iterate over filters.keys() and perform the queries.
    # This will essentially remove one file to edit when we want to add a params and remove a test case as well.

    # @IMPORTANT:
    # If `query.filter` runs the SQL query then,
    # the code below runs in O(n), n being the numbers of params for the `/entities`` route.
    # This is no bueno, in SQL we can improve performances by merging everything in WHERE statement.
    # I.E: SELECT entities.* FROM entities WHERE status == 'on' AND type == 'light'
    for key in filters.keys():
        value = filters.get(key)
        if value:
            query = query.filter(getattr(Entity, key) == value)

    return query
