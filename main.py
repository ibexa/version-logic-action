import os
import requests  # noqa We are just importing this to prove the dependency installed correctly
import semver
import re


def main():
    # cut initial v from input
    current_tag = os.environ["INPUT_CURRENTTAG"][1:]

    major, minor, patch, prerelease, _ = semver.VersionInfo.parse(current_tag)
    if prerelease:
        type, number = re.match('(?P<type>alpha|beta|rc)(?P<number>\d+)', prerelease).groups(['type', 'number'])
        if type == 'beta' and number == '1':
            # compare 3.3.0-beta1 with 3.2.0
            # but if it's patch compare with last released patch
            if not patch:
                previous_tag = semver.format_version(major, minor - 1, 0)
            else:
                previous_tag = semver.format_version(major, minor, patch - 1)
        elif type == 'rc' and number == '1':
            # compare 3.3.0-rc1 with 3.3.0-beta1
            previous_tag = semver.format_version(major, minor, patch, 'beta1')
        else:
            previous_tag = semver.format_version(major, minor, patch, f"{type}{int(number) - 1}")
    elif not patch and not minor:
        previous_tag = semver.format_version(major - 1, 0, 0)
    elif not patch:
        previous_tag = semver.format_version(major, minor - 1, 0)
    else:
        previous_tag = semver.format_version(major, minor, patch - 1)

    print(f"::set-output name=previousTag::v{previous_tag}")


if __name__ == "__main__":
    main()
