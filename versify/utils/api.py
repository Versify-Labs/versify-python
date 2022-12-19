import requests


def call_external_api(method: str, url: str, account: str, body: dict = {}, params: dict = {}):
    headers = {
        'Versify-Signature': 'Not Implemented',
        'Versify-Account': account,
    }
    print({
        'method': method,
        'headers': headers,
        'json': body,
        'params': params,
        'url': url,
    })

    response = requests.request(
        headers=headers,
        json=body,
        method=method,
        params=params,
        url=url
    )
    return response
