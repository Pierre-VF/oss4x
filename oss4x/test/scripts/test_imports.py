from oss4x.scripts.scripts import (
    data_publication,
    discover_new_sources,
    discover_projects,
)


def test_import():
    # The most basic test to at least ensure that all dependencies imported work out

    from oss4x.scripts import scripts
    from oss4x.scripts.scripts import (
        repository_scraping,
    )

    # Package
    assert isinstance(scripts.__name__, str)

    # Sub-packages
    assert isinstance(data_publication.__name__, str)
    assert isinstance(discover_new_sources.__name__, str)
    assert isinstance(discover_projects.__name__, str)
    assert isinstance(repository_scraping.__name__, str)
