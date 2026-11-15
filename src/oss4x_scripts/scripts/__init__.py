"""
Module containing methods to be run in scripts
"""

import os

from oss4x.src.log import log_info
from oss4x.src.parsers import (
    ParsingTargets,
    ResourceListing,
    identify_parsing_targets,
)
from oss4x.src.parsers.git_platforms.github_io import GithubScraper
from oss4x_scripts.src.config import (
    FILE_INPUT_INDEX,
    FILE_INPUT_LISTINGS_INDEX,
    FILE_OUTPUT_SUMMARY_TOML,
)


def format_individual_file(file_path: str) -> None:
    os.system(f"black {file_path}")


def format_all_files():
    format_individual_file(FILE_INPUT_INDEX)
    format_individual_file(FILE_OUTPUT_SUMMARY_TOML)


def _add_projects_to_listing_file(
    parsing_targets: ParsingTargets,
    file_path: str = FILE_INPUT_INDEX,
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


def add_projects_to_listing(
    project_urls: list[str],
    file_path: str = FILE_INPUT_INDEX,
) -> None:
    """Adds projects from a list into the index file

    :param project_urls: list of URLs to be added
    :param file_path: TOML file link to be updated, defaults to FILE_INPUT_INDEX
    """
    # Splitting URLs into targets
    new_targets = identify_parsing_targets(project_urls)

    _add_projects_to_listing_file(
        new_targets,
        file_path=file_path,
    )
    log_info("Done!")


def update_listing_of_listings(
    target_output_file: str = FILE_INPUT_LISTINGS_INDEX,
) -> None:
    list_of_listings = ResourceListing.from_json(target_output_file)

    # Add data from listings of listings
    raise NotImplementedError("Listing fetching must be implemented")

    list_of_listings.ensure_sorted_cleaned_and_unique_elements()

    # Fetch licenses
    list_of_listings.fetch_all_licenses()
    list_of_listings.fetch_all_target_counts()

    list_of_listings.to_json(target_output_file)
