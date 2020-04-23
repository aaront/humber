from courant.renderer import render_str


def test_render_metadata():
    toml = """
[meta]
title = "somepost"
tags = ["some", "tags"]
description = \"\"\"
Some *markdown* content.
\"\"\"

[[photo]]
src = "some/path.jpg"
type = "grouped"
    """

    template = """
    {{ meta.title }}

    {{ meta.description | markdown }}
    """

    rendered = render_str(toml, template)
    assert rendered
