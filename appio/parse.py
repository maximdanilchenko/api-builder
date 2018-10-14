
def join_paths(paths):
    if not paths:
        raise Exception()
    if len(paths) == 1:
        return paths[0]
    parts = [*(path.strip('/') for path in paths[:-1]), paths[-1].lstrip('/')]
    return '/' + '/'.join([part for part in parts if part])
