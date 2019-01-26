import unittest

from clarifai.rest.grpc.grpc_json_channel import dict_to_protobuf
from clarifai.rest.grpc.proto.clarifai.api.concept_pb2 import Concept as ConceptPB


class TestJsonToProtobuf(unittest.TestCase):

  def test_concept_with_no_value(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name'})
    assert converted.value == 1.0

  def test_concept_with_value_non_zero(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 0.5})
    assert converted.value == 0.5

  def test_concept_with_value_zero(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 0.0})
    assert converted.value == 0.0

  def test_concept_with_value_one(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 1.0})
    assert converted.value == 1.0

  def test_concept_with_new_field(self):
    converted = dict_to_protobuf(
        ConceptPB, {
            'id': 'some-id',
            'name': 'Some Name',
            'value': 1.0,
            'new_field': 'new_value'
        },
        ignore_unknown_fields=True)
    assert not hasattr(converted, 'new_field')
