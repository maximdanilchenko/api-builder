from parse import compile


def join_paths(paths):
    if not paths:
        raise Exception()
    if len(paths) == 1:
        return paths[0]
    parts = [*(path.strip('/') for path in paths[:-1]), paths[-1].lstrip('/')]
    return '/' + '/'.join([part for part in parts if part])


class PathParser:

    def __init__(self, path):
        # TODO: write query parser instead of using parse lib
        self.compiled = compile(path)
        self._row = self.to_row(path)

    def to_row(self, string):
        result = []
        write_flag = True
        for smb in string:
            if smb == '{':
                write_flag = self.changed_flag(write_flag, False)
            elif smb == '}':
                write_flag = self.changed_flag(write_flag, True)
            elif write_flag is True:
                result.append(smb)
        return ''.join(result)

    @staticmethod
    def changed_flag(flag: bool, value: bool):
        if flag is value:
            raise Exception()
        return value

    def __eq__(self, other):
        return self._row == other._row

    def __hash__(self):
        return hash(self._row)
