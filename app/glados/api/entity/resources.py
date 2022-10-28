from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntityRequestSerializer, EntitiesRequestSerializer, EntityResponseSerializer
from glados.repositories.entities import get_entities, update_entity

# @TODO_CURRENT_PR: REMOVE
# import sys
# print("X", file=sys.stderr)


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200


class EntityAPI(Resource):
    def patch(self, id):
        request_serializer = EntityRequestSerializer()
        data = request_serializer.load(request.json)

        entity = update_entity(id, data)

        if entity:
            serializer = EntityResponseSerializer(many=False)
            return serializer.dump(entity), 200

        # @NOTE:
        # We could be more specific here.
        # e.g: We could use an error handler or error from validation library
        return 'Not Found', 404
