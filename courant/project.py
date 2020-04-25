import os.path
from tomlkit import document, table


class Project:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise IOError(f"Couldn't locate the path: {path}")
        self._basepath = path


def create(path: str) -> Project:
    if not os.path.exists(path):
        os.mkdir(path)

    project_conf = document()

    meta = table()
    meta.add("name", os.path.dirname(path))
    meta.add("author", "John Smith")
    meta.add("author_bio", "Just a photographer")

    project_conf.add("meta", meta)

    with open(os.path.join(path, "project.toml"), "w", encoding="utf-8") as f:
        f.write(project_conf.as_string())
    
    return Project(path)
