import base64

import mock

from clarifai.rest import ClarifaiApp
from .mock_extensions import mock_string_should_end_with

TINY_IMAGE_BASE64 = b'R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='


@mock.patch('clarifai.rest.http_client.HttpClient')
def test_search_by_image_crop_with_url(mock_http_client):
  mock_execute_request = mock_http_client.return_value.execute_request
  mock_execute_request.side_effect = [{
      'app_id': '',
      'models': []
  }, {
      "status": {
          "code": 10000,
          "description": "Ok"
      },
      "id":
          "2844fa805627436c89e93fa8ffb9ecf9",
      "hits": [{
          "score": 1.0,
          "input": {
              "id": "35a63cd065ca4b34bdcadb7b18b93e66",
              "data": {
                  "image": {
                      "url": "https://samples.clarifai.com/dog2.jpeg"
                  }
              },
              "created_at": "2019-01-07T08:49:36.988214Z",
              "modified_at": "2019-01-07T08:49:38.302670Z",
              "status": {
                  "code": 30000,
                  "description": "Download complete"
              }
          }
      }]
  }]

  images = ClarifaiApp().inputs.search_by_image(
      url='https://samples.clarifai.com/puppy.jpeg', crop=[0.0, 0.0, 1.0, 1.0])

  assert len(images) == 1
  assert images[0].score == 1.0

  assert mock_execute_request.mock_calls == [
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/models')),
      mock.call(
          'POST', {
              'query': {
                  'ands': [{
                      'output': {
                          'input': {
                              'data': {
                                  'image': {
                                      'url': u'https://samples.clarifai.com/puppy.jpeg',
                                      'crop': [0.0, 0.0, 1.0, 1.0]
                                  }
                              }
                          }
                      }
                  }]
              },
              'pagination': {
                  'per_page': 20,
                  'page': 1
              }
          }, mock_string_should_end_with(u'/v2/searches')),
  ]


@mock.patch('clarifai.rest.http_client.HttpClient')
def test_search_by_image_crop_with_base64(mock_http_client):
  mock_execute_request = mock_http_client.return_value.execute_request
  mock_execute_request.side_effect = [{
      'app_id': '',
      'models': []
  }, {
      "status": {
          "code": 10000,
          "description": "Ok"
      },
      "id":
          "2844fa805627436c89e93fa8ffb9ecf9",
      "hits": [{
          "score": 1.0,
          "input": {
              "id": "35a63cd065ca4b34bdcadb7b18b93e66",
              "data": {
                  "image": {
                      "url": "https://samples.clarifai.com/dog2.jpeg"
                  }
              },
              "created_at": "2019-01-07T08:49:36.988214Z",
              "modified_at": "2019-01-07T08:49:38.302670Z",
              "status": {
                  "code": 30000,
                  "description": "Download complete"
              }
          }
      }]
  }]

  images = ClarifaiApp().inputs.search_by_image(
      base64bytes=TINY_IMAGE_BASE64, crop=[0.0, 0.0, 1.0, 1.0])

  assert len(images) == 1
  assert images[0].score == 1.0

  assert mock_execute_request.mock_calls == [
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/models')),
      mock.call(
          'POST', {
              'query': {
                  'ands': [{
                      'output': {
                          'input': {
                              'data': {
                                  'image': {
                                      'base64': TINY_IMAGE_BASE64.decode(),
                                      'crop': [0.0, 0.0, 1.0, 1.0]
                                  }
                              }
                          }
                      }
                  }]
              },
              'pagination': {
                  'per_page': 20,
                  'page': 1
              }
          }, mock_string_should_end_with(u'/v2/searches')),
  ]


@mock.patch('clarifai.rest.http_client.HttpClient')
def test_search_by_image_crop_with_filename(mock_http_client):
  mock_execute_request = mock_http_client.return_value.execute_request
  mock_execute_request.side_effect = [{
      'app_id': '',
      'models': []
  }, {
      "status": {
          "code": 10000,
          "description": "Ok"
      },
      "id":
          "2844fa805627436c89e93fa8ffb9ecf9",
      "hits": [{
          "score": 1.0,
          "input": {
              "id": "35a63cd065ca4b34bdcadb7b18b93e66",
              "data": {
                  "image": {
                      "url": "https://samples.clarifai.com/dog2.jpeg"
                  }
              },
              "created_at": "2019-01-07T08:49:36.988214Z",
              "modified_at": "2019-01-07T08:49:38.302670Z",
              "status": {
                  "code": 30000,
                  "description": "Download complete"
              }
          }
      }]
  }]

  images = ClarifaiApp().inputs.search_by_image(
      filename='tests/rest_tests/data/tiny_image.gif', crop=[0.0, 0.0, 1.0, 1.0])

  assert len(images) == 1
  assert images[0].score == 1.0

  assert mock_execute_request.mock_calls == [
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/models')),
      mock.call(
          'POST', {
              'query': {
                  'ands': [{
                      'output': {
                          'input': {
                              'data': {
                                  'image': {
                                      'base64': TINY_IMAGE_BASE64.decode(),
                                      'crop': [0.0, 0.0, 1.0, 1.0]
                                  }
                              }
                          }
                      }
                  }]
              },
              'pagination': {
                  'per_page': 20,
                  'page': 1
              }
          }, mock_string_should_end_with(u'/v2/searches')),
  ]


@mock.patch('clarifai.rest.http_client.HttpClient')
def test_search_by_image_crop_with_bytes(mock_http_client):
  mock_execute_request = mock_http_client.return_value.execute_request
  mock_execute_request.side_effect = [{
      'app_id': '',
      'models': []
  }, {
      "status": {
          "code": 10000,
          "description": "Ok"
      },
      "id":
          "2844fa805627436c89e93fa8ffb9ecf9",
      "hits": [{
          "score": 1.0,
          "input": {
              "id": "35a63cd065ca4b34bdcadb7b18b93e66",
              "data": {
                  "image": {
                      "url": "https://samples.clarifai.com/dog2.jpeg"
                  }
              },
              "created_at": "2019-01-07T08:49:36.988214Z",
              "modified_at": "2019-01-07T08:49:38.302670Z",
              "status": {
                  "code": 30000,
                  "description": "Download complete"
              }
          }
      }]
  }]

  images = ClarifaiApp().inputs.search_by_image(
      imgbytes=base64.b64decode(TINY_IMAGE_BASE64), crop=[0.0, 0.0, 1.0, 1.0])

  assert len(images) == 1
  assert images[0].score == 1.0

  assert mock_execute_request.mock_calls == [
      mock.call('GET', {
          'per_page': 20,
          'page': 1
      }, mock_string_should_end_with(u'/v2/models')),
      mock.call(
          'POST', {
              'query': {
                  'ands': [{
                      'output': {
                          'input': {
                              'data': {
                                  'image': {
                                      'base64': TINY_IMAGE_BASE64.decode(),
                                      'crop': [0.0, 0.0, 1.0, 1.0]
                                  }
                              }
                          }
                      }
                  }]
              },
              'pagination': {
                  'per_page': 20,
                  'page': 1
              }
          }, mock_string_should_end_with(u'/v2/searches')),
  ]
