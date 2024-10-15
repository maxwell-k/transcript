#!/usr/bin/env python3
# src/transcript.py
# Copyright 2022 Keith Maxwell
# SPDX-License-Identifier: MPL-2.0
# /// script
# requires-python = ">=3.11"
# dependencies = [
#  "youtube-transcript-api",
# ]
# ///
"""Download and extract files to `~/.local/bin/`."""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


__version__ = "0.0.2"


class _CustomNamespace(Namespace):
    url: str


PREFIX = "https://www.youtube.com/watch?v="


def _parse_id(url: str) -> str:
    if not url.startswith(PREFIX):
        msg = "URL should start with https://www.youtube.com/watch?v="
        raise RuntimeError(msg)
    return url.removeprefix(PREFIX)


def _format(seconds: float) -> str:
    hours, minutes = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(minutes, 60)
    return f"{hours:0.0f}:{minutes:02.0f}:{seconds:02.0f}"


def main() -> int:
    """Parse command line arguments and download each file."""
    args = _parse_args()

    try:
        video_id = _parse_id(args.url)
    except RuntimeError as e:
        print(e)
        return 1

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    length = len(_format(transcript[-1]["start"]).lstrip("0:"))
    for line in transcript:
        print(_format(line["start"])[-length:] + " " + line["text"])

    return 0


def _parse_args() -> _CustomNamespace:
    parser = ArgumentParser(
        prog=Path(__file__).name,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)
    help_ = "YouTube video URL"
    parser.add_argument("url", help=help_, type=str)
    return parser.parse_args(namespace=_CustomNamespace())


if __name__ == "__main__":
    raise SystemExit(main())
