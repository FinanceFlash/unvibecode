import pytest

from unvibecode_graph.resolve import ImportResolver


def resolve(tmp_path, files, source_file, module, symbols=()):
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    imp = {
        "raw": module,
        "module": module,
        "symbols": list(symbols),
        "import_style": "from_import" if symbols else "import",
        "relative_level": 0,
    }
    resolver = ImportResolver(tmp_path, [f for f in files if f.endswith(".py")])
    return resolver.resolve(source_file, "python", imp)["resolved_file"]


SRC_FOO = {"src/foo/__init__.py": "", "tests/test_a.py": "import foo\n"}


@pytest.mark.xfail(strict=True, reason="#425: import falls back to a same-named file")
def test_src_layout_wins_over_a_same_named_fixture(tmp_path):
    files = {**SRC_FOO, "tests/fixtures/foo.py": ""}
    assert resolve(tmp_path, files, "tests/test_a.py", "foo") == "src/foo/__init__.py"


@pytest.mark.xfail(strict=True, reason="#470: src layout package is never found")
def test_src_layout_package_is_found(tmp_path):
    assert resolve(tmp_path, SRC_FOO, "tests/test_a.py", "foo") == "src/foo/__init__.py"


@pytest.mark.xfail(strict=True, reason="#470: src layout package is never found")
def test_from_import_finds_src_layout_package(tmp_path):
    files = {**SRC_FOO, "tests/test_from.py": ""}
    found = resolve(tmp_path, files, "tests/test_from.py", "foo", ["hello"])
    assert found == "src/foo/__init__.py"


@pytest.mark.xfail(strict=True, reason="#933: import links to a test stub")
def test_package_wins_over_a_test_stub_with_the_same_name(tmp_path):
    files = {
        "src/flask/__init__.py": "",
        "tests/test_apps/cliapp/inner1/inner2/flask.py": "",
        "examples/tutorial/flaskr/auth.py": "",
    }
    found = resolve(tmp_path, files, "examples/tutorial/flaskr/auth.py", "flask", ["X"])
    assert found == "src/flask/__init__.py"


@pytest.mark.xfail(strict=True, reason="#425: stdlib import links to a local file")
def test_stdlib_import_inside_a_package_stays_external(tmp_path):
    files = {"app/__init__.py": "", "app/logging.py": "", "app/main.py": ""}
    assert resolve(tmp_path, files, "app/main.py", "logging") is None


@pytest.mark.xfail(strict=True, reason="#425: import falls back to a same-named file")
def test_monorepo_prefers_the_importing_files_own_project(tmp_path):
    adapter = "caspian/adapters/discord/__init__.py"
    files = {
        "packages/python/pyproject.toml": "",
        f"packages/python/src/{adapter}": "",
        "packages/python/src/caspian/adapters/__init__.py": "",
        "python/pyproject.toml": "",
        f"python/src/{adapter}": "",
    }
    source = "packages/python/src/caspian/adapters/__init__.py"
    found = resolve(tmp_path, files, source, "caspian.adapters.discord")
    assert found == f"packages/python/src/{adapter}"


def test_flat_layout_still_works(tmp_path):
    files = {"foo/__init__.py": "", "tests/test_a.py": ""}
    assert resolve(tmp_path, files, "tests/test_a.py", "foo") == "foo/__init__.py"


def test_script_folder_sibling_still_works(tmp_path):
    files = {"tests/helpers.py": "", "tests/test_x.py": ""}
    assert resolve(tmp_path, files, "tests/test_x.py", "helpers") == "tests/helpers.py"
