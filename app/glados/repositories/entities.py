from glados.models import Entity

# @NOTE:
# `EntitiesRequestSerializer` validate the arguments of get_entities function,
# perhaps we could iterate over filters.keys() and perform the queries.
# This will essentially remove one file to edit when we want to add a params and remove a test case as well.

# @IMPORTANT:
# If `query.filter` runs the SQL query then,
# the code below runs in O(n), n being the numbers of params for the `/entities`` route.
# This is no bueno, in SQL we can improve performances by merging everything in WHERE statement.
# I.E: SELECT entities.* FROM entities WHERE status == 'on' AND type == 'light'


def get_entities(filters):

    query = Entity.query

    for key in filters.keys():
        value = filters.get(key)
        if value:
            query = query.filter(getattr(Entity, key) == value)

    return query

# @NOTE:
# I'm not sure about this.
# It seems that from what I've read on the web that this is the way to go...
# I wish I could use an SQL UPDATE, but can't create the function in the model.
# On the project I would ask for help, or maybe, the method will be already coded.


def update_entity(id, data):

    entity = Entity.query.get(id)

    if entity:
        new_entity = Entity(
            id=entity.id,
            name=entity.name,
            type=entity.type,
            status=entity.status,
            value=entity.value,
            room_id=entity.room_id)

        if data.get('name'):
            new_entity.name = data.get('name')
        if data.get('type'):
            new_entity.type = data.get('type')
        if data.get('status'):
            new_entity.status = data.get('status')
        if data.get('value'):
            new_entity.value = data.get('value')

        entity.remove(commit=True)
        new_entity.save(commit=True)

        return new_entity

    return False
