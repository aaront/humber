import os.path

from tomlkit import document, table

from . import __title__


class Site:
    def __init__(self, config_path: str = None):
        self.config_path = config_path

    def create(self, name: str = None):
        if self.config_path:
            raise Exception("Config already created")
        _name = name or os.path.basename(os.getcwd())
        config_root = os.path.join(os.getcwd(), _name)
        self.config_path = os.path.join(config_root, "pyproject.toml")

        if not os.path.exists(config_root):
            os.mkdir(config_root)

        project_conf = document()

        poetry_meta = table()
        poetry_meta.add("name", _name)
        poetry_meta.add("version", "0.0.1")
        poetry_meta.add("description", "Just an opinionated photo stream site")
        project_conf.add("tool.poetry", poetry_meta)

        poetry_deps = table()
        poetry_deps.add("python", "^3.8")
        poetry_deps.add(__title__, "*")
        project_conf.add("tool.poetry.dependencies", poetry_deps)

        build_sys = table()
        build_sys.add("requires", ["poetry-core>=1.0.0"])
        build_sys.add("build-backend", "poetry.masonry.api")
        project_conf.add("build-system", build_sys)

        meta = table()
        meta.add("name", _name)
        meta.add("author", "John Smith")
        meta.add("author_bio", "Just a photographer")
        project_conf.add("tool.humber.meta", meta)

        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(project_conf.as_string())
