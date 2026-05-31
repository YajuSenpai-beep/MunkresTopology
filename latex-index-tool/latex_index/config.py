"""配置管理 — 加载 YAML/JSON 配置文件，提供默认值。"""

from __future__ import annotations

import copy
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


CONFIG_VERSION = 1

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": CONFIG_VERSION,
    "templates": {
        "l1": "\\index{${key}}",
        "l1Math": "\\index{${sort}@${display}}",
        "l2": "\\index{${parent}!${child}}",
    },
    "file_pattern": "Chapter_${num}_*.tex",
    "aliases": {},
    "math_shortcuts": {},
    "skip_patterns": [],
    "chapter_source_dir": "chapters",
    "index_processor": "makeindex",
    "log_level": "INFO",
    "log_file": "index_tool.log",
}


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件（YAML 或 JSON）。

    Args:
        path: 配置文件路径。如果为 None，返回默认配置。

    Returns:
        合并了默认值的配置字典。
    """
    config = copy.deepcopy(DEFAULT_CONFIG)

    if path is None:
        logger.info("未指定配置文件，使用默认配置")
        return config

    path_obj = Path(path)
    if not path_obj.exists():
        logger.warning("配置文件 %s 不存在，使用默认配置", path)
        return config

    try:
        with open(path_obj, "r", encoding="utf-8") as f:
            if path_obj.suffix in (".yaml", ".yml"):
                if not HAS_YAML:
                    logger.error("需要安装 PyYAML: pip install pyyaml")
                    return config
                user_config = yaml.safe_load(f) or {}
            else:
                user_config = json.load(f)
    except Exception as e:
        logger.error("配置文件读取失败: %s", e)
        return config

    # 深度合并
    _deep_merge(config, user_config)

    # 版本校验
    file_version = config.get("version")
    if file_version is not None and file_version != CONFIG_VERSION:
        logger.warning(
            "配置文件版本 %s 与工具版本 %s 不匹配，可能出现兼容性问题",
            file_version, CONFIG_VERSION,
        )

    logger.info("已加载配置: %s", path)
    return config


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    """递归合并 override 到 base。"""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
