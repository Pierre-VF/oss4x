import pytest


@pytest.mark.skip
def test_import():
    # The most basic test to at least ensure that all dependencies imported work out

    import oss4x_scripts
    from oss4x_scripts import cli, scripts
    from oss4x_scripts.scripts import (
        data_publication,
        discover_new_sources,
        misc,
        repository_scraping,
    )

    # Package
    assert isinstance(oss4x_scripts.__name__, str)

    # Sub-packages
    assert isinstance(cli.__name__, str)
    assert isinstance(scripts.__name__, str)

    assert isinstance(data_publication.__name__, str)
    assert isinstance(discover_new_sources.__name__, str)
    assert isinstance(misc.__name__, str)
    assert isinstance(repository_scraping.__name__, str)
