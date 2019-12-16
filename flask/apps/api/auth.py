def auth_parameters(**params):
    if 'token' not in params or params['token'] != 'nuance.mix.hackz':
        return False
    else:
        return True

def page_unauth(**params):
    if 'token' not in params:
        return "<html><title>Unauthorized</title><body>Must provide valid token</body></html>"
    elif params['token'] != 'nuance.mix.hackz':
        return "<html><title>Unauthorized</title><body>Must provide valid token</body></html>"
    else:
        return None
