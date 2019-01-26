import mock

from clarifai.rest import ClarifaiApp
from .mock_extensions import mock_string_should_end_with


@mock.patch('clarifai.rest.http_client.HttpClient')
def test_get_all_concepts(mock_http_client):
  mock_execute_request = mock_http_client.return_value.execute_request
  mock_execute_request.side_effect = [{
      'app_id': '',
      'models': []
  }, {
      'app_id':
          '',
      'concepts': [
          {
              'id': '1',
              'name': '1',
              'value': 1,
              'app_id': 'app',
              'created_at': '2010-01-01T00:00:00Z',
          },
          {
              'id': '2',
              'name': '2',
              'value': 1,
              'app_id': 'app',
              'created_at': '2010-01-01T00:00:00Z',
          },
      ],
  }, {
      'app_id': '',
      'concepts': [],
  }]

  concepts = list(ClarifaiApp().concepts.get_all())

  assert len(concepts) == 2
  assert mock_execute_request.mock_calls == [
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/models')),
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/concepts')),
      mock.call('GET', {
          'per_page': 20,
          'page': 2
      }, mock_string_should_end_with(u'/v2/concepts'))
  ]
