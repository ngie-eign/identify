from __future__ import annotations

import argparse
try:
    from enum import StrEnum
except ImportError:  # pragma: no cover
    from strenum import StrEnum  # type: ignore
import json
from collections.abc import Sequence

from identify import identify


class TagType(StrEnum):
    FILE = 'file'
    LICENSE = 'license'


TAG_TYPE_CHOICES = [TagType.FILE.value]
try:
    import ukkonen  # noqa: F401
except ImportError:  # pragma: no cover
    pass
else:
    TAG_TYPE_CHOICES.append(TagType.LICENSE.value)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename-only', action='store_true')
    parser.add_argument(
        '--tag-type', choices=TAG_TYPE_CHOICES, default=TAG_TYPE_CHOICES[0],
    )
    parser.add_argument('path')
    args = parser.parse_args(argv)

    if args.tag_type == TagType.FILE.value:
        func = (
            identify.tags_from_filename
            if args.filename_only else identify.tags_from_path
        )
    else:
        func = identify.license_ids

    try:
        tags = sorted(func(args.path))
    except ValueError as e:
        print(e)
        return 1

    if not tags:
        return 1
    print(json.dumps(tags))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
