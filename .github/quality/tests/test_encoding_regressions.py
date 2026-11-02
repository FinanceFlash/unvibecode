import pytest

from test_repository_quality import (
    test_markdown_has_no_common_encoding_corruption as check_markdown_encoding,
)


@pytest.mark.parametrize(
    "text",
    [
        "The result \u00e2\u20ac\u201d is ready",
        "It\u00e2\u20ac\u2122s ready",
        "caf\u00c3\u00a9",
        "\u00e2\u201d",
        "invalid \ufffd",
    ],
    ids=["em-dash", "apostrophe", "accent-marker", "box-marker", "replacement"],
)
def test_encoding_check_rejects_known_corruption(tmp_path, text):
    sample = tmp_path / "broken.md"
    sample.write_text(text, encoding="utf-8")

    with pytest.raises(AssertionError, match=r"broken\.md"):
        check_markdown_encoding(sample)


@pytest.mark.parametrize(
    "text",
    [
        "Plain ASCII documentation.",
        "The result \u2014 is ready.",
        "It\u2019s ready.",
        (
            "caf\u00e9, S\u00e3o Paulo, \u65e5\u672c\u8a9e, "
            "\u0928\u092e\u0938\u094d\u0924\u0947"
        ),
        "A valid character: \u00e2",
        "Price: 10 \u20ac",
    ],
    ids=["ascii", "em-dash", "apostrophe", "multilingual", "a-circumflex", "euro"],
)
def test_encoding_check_accepts_valid_unicode(tmp_path, text):
    sample = tmp_path / "valid.md"
    sample.write_text(text, encoding="utf-8")

    check_markdown_encoding(sample)
