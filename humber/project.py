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

    poetry_meta = table()
    poetry_meta.add("name", os.path.dirname(path))
    poetry_meta.add("version", "0.0.1")
    poetry_meta.add("description", "Just an opinionated photo stream site")
    project_conf.add("tool.poetry", poetry_meta)

    poetry_deps = table()
    poetry_deps.add("python", "^3.8")
    poetry_deps.add("humber", "*")
    project_conf.add("tool.poetry.dependencies", poetry_deps)

    build_sys = table()
    build_sys.add("requires", ["poetry>=0.12"])
    build_sys.add("build-backend", "poetry.masonry.api")
    project_conf.add("build-system", build_sys)

    meta = table()
    meta.add("name", os.path.dirname(path))
    meta.add("author", "John Smith")
    meta.add("author_bio", "Just a photographer")
    project_conf.add("tool.humber.meta", meta)

    with open(os.path.join(path, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(project_conf.as_string())

    return Project(path)
