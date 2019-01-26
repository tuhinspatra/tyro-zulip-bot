import unittest

from clarifai.rest.grpc.grpc_json_channel import protobuf_to_dict
from clarifai.rest.grpc.proto.clarifai.api.concept_pb2 import Concept as ConceptPB
from clarifai.rest.grpc.proto.clarifai.api.model_pb2 import \
    MultiModelResponse as MultiModelResponsePB
from clarifai.rest.grpc.proto.clarifai.api.status.status_pb2 import Status as StatusPB
from clarifai.rest.grpc.proto.clarifai.api.workflow_pb2 import \
    MultiWorkflowResponse as MultiWorkflowResponsePB


class TestProtobufToJson(unittest.TestCase):

  def test_concept_with_no_value(self):
    concept = ConceptPB()
    concept.id = 'some-id'
    concept.name = 'Some Name'
    converted = protobuf_to_dict(concept)
    assert converted['value'] == 0.0

  def test_concept_with_value_non_zero(self):
    concept = ConceptPB()
    concept.id = 'some-id'
    concept.name = 'Some Name'
    concept.value = 0.5
    converted = protobuf_to_dict(concept)
    assert converted['value'] == 0.5

  def test_concept_with_value_zero(self):
    concept = ConceptPB()
    concept.id = 'some-id'
    concept.name = 'Some Name'
    concept.value = 0.0
    converted = protobuf_to_dict(concept)
    assert converted['value'] == 0.0

  def test_concept_with_value_one(self):
    concept = ConceptPB()
    concept.id = 'some-id'
    concept.name = 'Some Name'
    concept.value = True
    converted = protobuf_to_dict(concept)
    assert converted['value'] == 1.0

  def test_show_workflows_list_if_empty(self):
    status = StatusPB()
    status.description = 'Some description'

    workflows_response = MultiWorkflowResponsePB()
    workflows_response.status.CopyFrom(status)

    converted = protobuf_to_dict(workflows_response)
    assert (_ordered_json_object(converted) == _ordered_json_object({
        'status': {
            'description': 'Some description'
        },
        'workflows': []
    }))

  def test_show_models_list_if_empty(self):
    status = StatusPB()
    status.description = 'Some description'

    models_response = MultiModelResponsePB()
    models_response.status.CopyFrom(status)

    converted = protobuf_to_dict(models_response)
    assert (_ordered_json_object(converted) == _ordered_json_object({
        'status': {
            'description': 'Some description'
        },
        'models': []
    }))


def _ordered_json_object(obj):
  """ Orders all the keys of the object, recursively. """

  if isinstance(obj, dict):
    return sorted((k, _ordered_json_object(v)) for k, v in obj.items())
  if isinstance(obj, list):
    return sorted(_ordered_json_object(x) for x in obj)
  else:
    return obj
