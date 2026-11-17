"""
This module contains methods to discover new sources of code
"""

import os

from tqdm import tqdm

from oss4x.src.database.projects import project_dataframe_loader
from oss4x.src.log import (
    log_info,
)
from oss4x.src.models import EnumDocumentationFileType
from oss4x.src.parsers import (
    ParsingTargets,
    fetch_all_project_urls_from_markdown_str,
    fetch_all_project_urls_from_rst_str,
    url_qualifies,
)
from oss4x.src.parsers.git_platforms.github_io import GithubScraper


def discover_repositories_in_existing_organisations(
    output_file: str,
    input_index: str,
) -> None:
    """
    Discover repositories in existing organisations from the input index.

    Extracts organisation names from existing GitHub repositories and creates
    a new target list with these organisations for further discovery.

    :param output_file: Path to the output TOML file where extended targets will be saved
    :param input_index: Path to the input TOML file containing the repository index
    """
    log_info("Loading organisations and repositories to be indexed")
    targets = ParsingTargets.from_toml(input_index)

    # Extract organisation to screen for new repositories
    ghs = GithubScraper()
    orgs = {ghs.extract_repository_organisation(i) for i in targets.github_repositories}

    extended_targets = ParsingTargets(
        github_organisations=orgs,
    )

    # Cleaning up and exporting to TOML file
    log_info("Cleaning up targets")
    extended_targets.cleanup()
    log_info(f"Exporting to {output_file}")
    extended_targets.to_toml(output_file)


def discover_repositories_in_existing_readmes(
    output_file: str,
    input_index: str,
) -> None:
    """
    Discover repositories by extracting URLs from README files of known repositories.

    Scans README content (Markdown and RST) from the feather dataset to find
    additional project URLs that should be indexed.

    :param output_file: Path to the output TOML file where extended targets will be saved
    :param input_index: Path to the input TOML file containing the repository index
    """
    # Importing locally as that's not an absolute file-level requirement (and the file isn't easily available anymore)
    from oss4x.app.src.config import (
        get_file_output_listing_feather,
    )

    feather_path = get_file_output_listing_feather()
    log_info("Searching for relevant resource URLs in READMEs of known repositories")
    if not os.path.exists(feather_path):
        raise RuntimeError(
            "The dataset is not available locally - make sure to download it prior to running this"
        )

    dfs = project_dataframe_loader(feather_path)

    full_targets = ParsingTargets.from_toml(input_index)
    for i, r in tqdm(dfs.iterrows()):
        try:
            if isinstance(r["readme"], str):
                readme_type = r["readme_type"]
                if readme_type == EnumDocumentationFileType.MARKDOWN:
                    full_targets += fetch_all_project_urls_from_markdown_str(
                        r["readme"]
                    )
                elif readme_type == EnumDocumentationFileType.RESTRUCTURED_TEXT:
                    full_targets += fetch_all_project_urls_from_rst_str(r["readme"])
        except Exception as e:
            log_info(f"Error with {r} // e={e}")

    def _url_cleanup(x: str) -> str:
        x = x.split("?")[0]
        x = x.split("#")[0]
        x = x.removesuffix("/")
        return x

    # Removing problematic resources
    full_targets.github_organisations = {
        i for i in full_targets.github_organisations if "?" not in i
    }
    full_targets.github_repositories = {
        _url_cleanup(i) for i in full_targets.github_repositories if url_qualifies(i)
    }
    full_targets.gitlab_projects = {
        _url_cleanup(i) for i in full_targets.gitlab_projects if url_qualifies(i)
    }
    full_targets.unknown = {
        _url_cleanup(i) for i in full_targets.unknown if url_qualifies(i)
    }
    full_targets.invalid = {
        _url_cleanup(i) for i in full_targets.invalid if url_qualifies(i)
    }

    # Cleaning up and exporting to TOML file
    log_info("Cleaning up targets")
    full_targets.cleanup()
    log_info(f"Exporting to {output_file}")
    full_targets.to_toml(output_file)
