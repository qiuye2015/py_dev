import requests


def upload_file(url, file_path):
    with open(file_path, 'rb') as file:
        form_data = {'file': file}
        response = requests.post(
            url,
            files=form_data,
            # headers={
            #     'Accept': '*/*',
            #     'Host': '127.0.0.1:5000',
            # },
            # data={},
        )

        if response.status_code == 200:
            print('File uploaded successfully, resp=', response.content.decode('utf-8'))
        else:
            print('Failed to upload file')


upload_file('http://localhost:5000/upload', '/Users/leo.fu1/Desktop/fjp.txt')
