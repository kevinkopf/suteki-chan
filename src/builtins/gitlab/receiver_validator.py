from fastapi import Request


receiver_name = 'GitLab'


def is_valid_module(request: Request) -> bool:
    if request.headers.get('User-Agent')[:7] == 'GitLab/':
        return True
    return False
