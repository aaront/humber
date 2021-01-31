import jinja2
import mistune
import frontmatter


markdown = mistune.create_markdown(escape=True, renderer="html")


env = jinja2.Environment(autoescape=True)
env.filters["markdown"] = lambda text: jinja2.Markup(markdown.parse(text))
env.trim_blocks = True
env.lstrip_blocks = True


def read(fp: str):
    with open(fp, "r") as f:
        post = frontmatter.loads(f.read())
    return post


def render_str(post_str: str, template: str):
    metadata, content = frontmatter.parse(post_str)
    return env.from_string(template).render(meta=metadata, content=content)


# def render_str(toml_str: str, template: str):
#     toml_doc: TOMLDocument = parse(toml_str)
#     return env.from_string(template).render(
#         meta=toml_doc["meta"], photo=toml_doc["photo"]
#     )
