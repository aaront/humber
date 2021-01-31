from humber.parse import render_str


def test_render_metadata():
    markdown_str = """
---
title: Third test
date: 2020-05-04
---
Post content as **markdown**
    """

    template = """{{ meta.title }}
{{ meta.date }}

{{ content | markdown }}"""

    rendered = render_str(markdown_str, template)
    assert rendered == 'Third test\n2020-05-04\n\n<p>Post content as <strong>markdown</strong></p>\n'
