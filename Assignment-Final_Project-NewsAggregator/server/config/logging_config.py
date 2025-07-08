import logging
import os

log_dir = "server/logs"
os.makedirs(log_dir, exist_ok=True)

_news_agg_logger = logging.getLogger("news_aggregator")
_news_agg_logger.setLevel(logging.INFO)

if not any(
    isinstance(h, logging.FileHandler)
    and h.baseFilename.endswith("news_aggregator.log")
    for h in _news_agg_logger.handlers
):
    handler = logging.FileHandler(os.path.join(log_dir, "news_aggregator.log"))
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    _news_agg_logger.addHandler(handler)


def news_agg_logger(level, message):
    _news_agg_logger.log(level, message)
