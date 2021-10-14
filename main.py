import re
import typing
import logging
import argparse

from opensearchpy import OpenSearch
from datetime import datetime

_version = "0.0.1"
_project_name = "opensearch-index-rotate"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"{_project_name}-{_version}")


def build_filter_function(
    unit_count: int,
    timestring_regex: str = r"\d{4}-\d{2}-\d{2}",
    today_timeobj: typing.Any = datetime.now(),
) -> typing.Callable:
    def fn(
        timestring: str,
        unit_count: int = unit_count,
        today_timeobj: typing.Any = today_timeobj,
        timestring_regex: str = timestring_regex,
    ) -> bool:
        pattern = re.compile(timestring_regex)
        match = re.search(pattern, timestring)
        if match is None:
            return False
        date = datetime.strptime(str(match.group()), "%Y-%m-%d")
        return (today_timeobj - date).days > unit_count

    return fn


def filter_by_age(filter_function: typing.Callable, indices: list) -> list:
    return list(filter(filter_function, indices))


def main(host: str, unit_count: int, index: str, port: int = 443):
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        use_ssl=True,
        verify_certs=True,
        ssl_assert_hostname=False,
        ssl_show_warn=True,
    )

    response = client.indices.get(index)
    filter_fn = build_filter_function(unit_count=unit_count)
    indices = filter_by_age(filter_fn, response.keys())

    if not indices:
        logger.info(f"can't find indices from {unit_count} days ago, skip...")
        exit(0)
    response = client.indices.delete(",".join(indices))
    logger.info(f"delete response --> {response}")
    logger.info(f"delete indices {indices} success")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="opensearch index rotate tool")
    parser.add_argument("--host", type=str, required=True, help="opensearch host")
    parser.add_argument(
        "--days-ago", type=int, required=True, help="delete indices from DAYS_AGO"
    )
    parser.add_argument("--index", type=str, required=True, help="index name")
    args = parser.parse_args()

    main(args.host, args.days_ago, args.index)
