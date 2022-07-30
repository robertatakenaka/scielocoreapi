from http import HTTPStatus

from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
# from scielocore.api.schemas import DocumentSchema
# from scielocore.models import Document
# from scielocore.extensions import db
# from scielocore.commons.pagination import paginate

from scielo_core.id_provider import lib
from scielo_core.id_provider import exceptions

from scielocore.config import SCIELO_CORE_ID_PROVIDER_DB_URI


# request_document_id(pkg_file_path, username)

class DocumentResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a document
      description: Get a single document by ID
      parameters:
        - in: path
          name: document_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  document: DocumentSchema
        404:
          description: document does not exists
    put:
      tags:
        - api
      summary: Update a document
      description: Update a single document by ID
      parameters:
        - in: path
          name: document_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              DocumentSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: document updated
                  document: DocumentSchema
        404:
          description: document does not exists
    delete:
      tags:
        - api
      summary: Delete a document
      description: Delete a single document by ID
      parameters:
        - in: path
          name: document_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: document deleted
        404:
          description: document does not exists
    """

    method_decorators = [jwt_required()]

    def _db_connect(self):
        if not hasattr(self, '_db_connected'):
            self._db_connected = lib.connect(SCIELO_CORE_ID_PROVIDER_DB_URI)

    def get(self, document_id):
        self._db_connect()
        try:
            return lib.get_xml(document_id)
        except exceptions.DocumentDoesNotExistError:
            abort(HTTPStatus.NOT_FOUND)
        except exceptions.InvalidSizeOfPid:
            abort(HTTPStatus.BAD_REQUEST)

    # def put(self, document_id):
    #     schema = DocumentSchema(partial=True)
    #     document = Document.query.get_or_404(document_id)
    #     document = schema.load(request.json, instance=document)

    #     db.session.commit()

    #     return {"msg": "document updated", "document": schema.dump(document)}

    # def delete(self, document_id):
    #     document = Document.query.get_or_404(document_id)
    #     db.session.delete(document)
    #     db.session.commit()

    #     return {"msg": "document deleted"}
