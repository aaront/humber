import os.path

from loguru import logger
from tomlkit import document, table

from . import __title__


class Site:
    def __init__(self, config_path: str = None):
        self.config_path = config_path

    def create(self, name: str = None):
        if self.config_path:
            logger.error(
                "Config file already initialized: {config}", config=self.config_path
            )
            return
        _name = name or os.path.basename(os.getcwd())
        config_root = os.path.join(os.getcwd(), name or "")
        self.config_path = os.path.join(config_root, "pyproject.toml")
        if os.path.exists(self.config_path):
            logger.error(
                "Config file already exists at: {config}", config=self.config_path
            )
            return
        logger.info("Creating project: {path}", path=config_root)

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
        logger.info("Created new config: {conf}", conf=self.config_path)
