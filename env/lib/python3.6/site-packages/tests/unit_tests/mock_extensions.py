class MockValidator(object):

  def __init__(self, validator):
    # validator is a function that takes a single argument and returns a bool.
    self.validator = validator

  def __eq__(self, other):
    return bool(self.validator(other))


def mock_string_should_end_with(str):
  return MockValidator(lambda x: x.endswith(str))
