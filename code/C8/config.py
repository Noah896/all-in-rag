"""
RAG系统配置文件
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = (PROJECT_ROOT / "data" / "C8" / "cook").resolve()
DEFAULT_INDEX_PATH = (PROJECT_ROOT / "code" / "C8" / "vector_index").resolve()


def resolve_local_model(model_name: str) -> str:
    """
    将模型名称解析为本地模型目录（如果存在）

    离线环境下 huggingface_hub 会反复尝试联网校验，最终超时失败。
    只要本地或仓库 models/ 目录中存在同名模型，就直接使用本地路径。

    Args:
        model_name: 模型名称（如 BAAI/bge-small-zh-v1.5）或本地路径

    Returns:
        可用的本地模型路径；若本地不存在则返回原始 model_name
    """
    # 已经是存在的本地目录，直接使用
    if Path(model_name).exists():
        return model_name

    base_dir = Path(__file__).resolve().parent
    short_name = model_name.split("/")[-1]

    candidates = [
        base_dir / ".." / ".." / "models" / short_name,  # 仓库根目录 models/
        base_dir / "models" / short_name,                # 项目内 models/
    ]

    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue
        if (candidate / "config.json").exists() and (
            (candidate / "model.safetensors").exists()
            or (candidate / "pytorch_model.bin").exists()
        ):
            return str(candidate)

    return model_name


@dataclass
class RAGConfig:
    """RAG系统配置类"""

    # 路径配置
    data_path: str = str(DEFAULT_DATA_PATH)
    index_save_path: str = str(DEFAULT_INDEX_PATH)

    # 模型配置
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    llm_model: str = "kimi-k2.6"

    # 检索配置
    top_k: int = 3

    # 生成配置
    temperature: float = 1.0
    max_tokens: int = 2048

    def __post_init__(self):
        # 优先使用本地嵌入模型，避免联网下载/校验失败
        self.embedding_model = resolve_local_model(self.embedding_model)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'RAGConfig':
        """从字典创建配置对象"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

# 默认配置实例
DEFAULT_CONFIG = RAGConfig()
