from api import ApiResponse


def test_api_response():
    # Test new_success
    data = {'name': 'John', 'age': 25}
    response = ApiResponse.new_success(data)
    assert response.is_success() == True
    assert response.code == 0
    assert response.message == 'success'
    assert response.data == data

    # Test new_fail
    code = 1001
    message = 'error'
    response = ApiResponse.new_fail(code, message)
    assert response.is_success() == False
    assert response.code == code
    assert response.message == message
    assert response.data == None
