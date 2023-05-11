from type_handler import TypeHandler


def test_to_json():
    data_dict = {'key': 'value'}
    assert TypeHandler.to_json(data_dict) == '{"key": "value"}'

    data_list = [1, 2, 3]
    assert TypeHandler.to_json(data_list) == '[1, 2, 3]'

    data_str_json = '{"key": "value"}'
    assert TypeHandler.to_json(data_str_json) == '{"key": "value"}'

    data_str_literal = "{'key': 'value'}"
    assert TypeHandler.to_json(data_str_literal) == '{"key": "value"}'

    data_invalid_str = "this is not a valid json string"
    assert TypeHandler.to_json(data_invalid_str) == ''

    data_object = object()
    assert TypeHandler.to_json(data_object) == ''


def test_to_dict():
    assert TypeHandler.to_dict(None) == {}
    assert TypeHandler.to_dict('{"a": 1, "b": 2}') == {"a": 1, "b": 2}
    assert TypeHandler.to_dict({"a": 1, "b": 2}) == {"a": 1, "b": 2}
    try:
        TypeHandler.to_dict(123)
    except ValueError as ex:
        assert str(ex) == 'Payload must be a string or dictionary'
    try:
        TypeHandler.to_dict('{"a": 1, "b": 2')
    except ValueError as ex:
        assert str(ex) == 'Payload must be a valid JSON string'
