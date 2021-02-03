import os.path

from tomlkit import document, table

from . import __title__


class Site:
    def __init__(self, path: str):
        self.path = path

    def create(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        project_conf = document()

        poetry_meta = table()
        poetry_meta.add("name", os.path.dirname(self.path))
        poetry_meta.add("version", "0.0.1")
        poetry_meta.add("description", "Just an opinionated photo stream site")
        project_conf.add("tool.poetry", poetry_meta)

        poetry_deps = table()
        poetry_deps.add("python", "^3.8")
        poetry_deps.add(__title__, "*")
        project_conf.add("tool.poetry.dependencies", poetry_deps)

        build_sys = table()
        build_sys.add("requires", ["poetry>=0.12"])
        build_sys.add("build-backend", "poetry.masonry.api")
        project_conf.add("build-system", build_sys)

        meta = table()
        meta.add("name", os.path.dirname(self.path))
        meta.add("author", "John Smith")
        meta.add("author_bio", "Just a photographer")
        project_conf.add("tool.humber.meta", meta)

        with open(
            os.path.join(self.path, "pyproject.toml"), "w", encoding="utf-8"
        ) as f:
            f.write(project_conf.as_string())
