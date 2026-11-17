"""
Module containing methods to be run in scripts
"""

import subprocess
from datetime import timedelta

from oss4x.src.log import log_info, log_warning
from oss4x.src.parsers import (
    ParsingTargets,
    ResourceListing,
    identify_parsing_targets,
)
from oss4x.src.parsers.git_platforms.github_io import GithubScraper


def format_individual_file(file_path: str) -> None:
    subprocess.run(["black", str(file_path)], check=True)


def format_all_files(files: list[str]):
    for file_path in files:
        try:
            format_individual_file(file_path)
        except Exception as e:
            log_warning(f"Failed to reprocess the file {file_path} : {e}")


def _add_projects_to_listing_file(
    parsing_targets: ParsingTargets,
    file_path: str,
) -> None:
    log_info(f"Adding projects to {file_path}")
    existing_targets = ParsingTargets.from_toml(file_path)
    new_targets = existing_targets + parsing_targets

    # Cleaning Github repositories links
    ghs = GithubScraper()
    new_targets.github_repositories = {
        ghs.minimalise_resource_url(i) for i in new_targets.github_repositories
    }

    # Ensuring uniqueness in new targets and cleaning up redundancies
    new_targets.cleanup()

    # Outputting to a new TOML
    log_info(f"Exporting new index to {file_path}")
    new_targets.to_toml(file_path)

    if file_path.endswith(".toml"):
        # Format the file for human readability
        format_individual_file(file_path)


def discover_projects(
    file_path: str,
    listings_file_path: str,
    cache_lifetime: timedelta | None = None,
):
    log_info("Indexing LF Energy projects")

    # From webpage
    new_targets = ParsingTargets()
    dropped_urls = []

    raise NotImplementedError("Add your discovery code here")

    [log_info(f"DROPPING {i} (target is unclear)") for i in dropped_urls]

    _add_projects_to_listing_file(
        new_targets,
        file_path=file_path,
    )
    log_info("Done!")


def add_projects_to_listing(
    project_urls: list[str],
    file_path: str,
) -> None:
    """Adds projects from a list into the index file

    :param project_urls: list of URLs to be added
    :param file_path: TOML file link to be updated
    """
    # Splitting URLs into targets
    new_targets = identify_parsing_targets(project_urls)

    _add_projects_to_listing_file(
        new_targets,
        file_path=file_path,
    )
    log_info("Done!")


def update_listing_of_listings(
    target_output_file: str,
) -> None:
    list_of_listings = ResourceListing.from_json(target_output_file)

    # Add data from listings of listings
    raise NotImplementedError("Add your discovery code here")
    list_of_listings.ensure_sorted_cleaned_and_unique_elements()

    # Fetch licences
    list_of_listings.fetch_all_licences()
    list_of_listings.fetch_all_target_counts()

    list_of_listings.to_json(target_output_file)
