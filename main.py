import os
import requests  # noqa We are just importing this to prove the dependency installed correctly
import semver


def main():
    # cut initial v from input
    current_tag = os.environ["INPUT_CURRENTTAG"][1:]

    major, minor, patch, _, _ = semver.VersionInfo.parse(current_tag)
    if not patch and not minor:
        previous_tag = semver.format_version(major - 1, 0, 0)
    elif not patch:
        previous_tag = semver.format_version(major, minor - 1, 0)
    else:
        previous_tag = semver.format_version(major, minor, patch - 1)

    print(f"::set-output name=previousTag::v{previous_tag}")


if __name__ == "__main__":
    main()
