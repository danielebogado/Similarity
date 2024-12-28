import rapidfuzz.distance.JaroWinkler as _JaroWinkler
import importlib.metadata as _importlib_metadata

try:
    __version__: str = _importlib_metadata.version(__package__ or __name__)
except _importlib_metadata.PackageNotFoundError:
    __version__: str = "0.0.0"

__all__ = [
    "jarowinkler_similarity",
]

def jarowinkler_similarity(s1, s2, *, prefix_weight=0.1, processor=None, score_cutoff=None) -> float:

    return _JaroWinkler.similarity(
        s1,
        s2,
        prefix_weight=prefix_weight,
        processor=processor,
        score_cutoff=score_cutoff,
    )