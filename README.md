# 尝尝咸淡 RAG：菜谱知识库问答

这是一个可独立运行的食谱 RAG 示例项目，代码来自
[All-in-RAG 第八章](https://github.com/datawhalechina/all-in-rag/tree/main/code/C8)，
知识库来自 [HowToCook](https://github.com/Anduin2017/HowToCook)。

系统会读取 Markdown 菜谱，按标题建立父子文本块，使用 BGE 向量和 BM25 做混合检索，
再通过 Moonshot/Kimi 生成列表、详细步骤或一般性回答。

## 功能

- 将 300 多份 Markdown 菜谱切分为结构化子块。
- 使用 `bge-small-zh-v1.5` 构建 FAISS 向量索引。
- 将向量检索与 BM25 检索通过 RRF 融合。
- 支持按菜品分类和难度进行元数据过滤。
- 支持列表、详细步骤、一般问答三种生成模式。
- 自动缓存向量索引，后续启动无需重复构建。

## 项目结构

```text
.
├── code/C8/
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── rag_modules/
│       ├── data_preparation.py
│       ├── generation_integration.py
│       ├── index_construction.py
│       └── retrieval_optimization.py
├── data/C8/cook/
│   └── dishes/                 # 323 份 Markdown 菜谱
├── tests/
├── .env.example
└── NOTICE.md
```

RAG 只读取 `data/C8/cook` 中的 Markdown 文件。上游仓库里的配图是 Git LFS
占位对象，但 LFS 原文件已无法从远端取得，因此本仓库不包含这些无效图片，
不影响知识库构建和问答。

## 环境要求

- Python 3.10 或更高版本，推荐 Python 3.12
- 可访问 Moonshot API 的网络环境
- 首次构建向量索引时需要下载嵌入模型，或提前准备本地模型

## 快速开始

```bash
git clone https://github.com/Noah896/all-in-rag.git
cd all-in-rag/code/C8

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

在仓库根目录创建 `.env`，并填写自己的 API Key：

```bash
cp ../../.env.example ../../.env
```

Windows PowerShell 也可以直接执行：

```powershell
Copy-Item ..\..\.env.example ..\..\.env
```

编辑仓库根目录的 `.env`：

```dotenv
MOONSHOT_API_KEY=your_moonshot_api_key
```

运行：

```bash
python main.py
```

也可以从仓库根目录运行：

```bash
python code/C8/main.py
```

程序会从 `code/C8` 所在位置解析数据和索引路径，因此不依赖当前工作目录。

## 嵌入模型

默认模型是 `BAAI/bge-small-zh-v1.5`。第一次运行时，Hugging Face 会自动下载模型；
如果已经下载到以下任意目录，程序会自动优先使用本地文件：

```text
models/bge-small-zh-v1.5/
code/C8/models/bge-small-zh-v1.5/
```

本地模型目录至少应包含 `config.json`，以及 `model.safetensors` 或
`pytorch_model.bin`。完全离线运行时，可在 `.env` 中加入：

```dotenv
HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
```

如需使用 Hugging Face 镜像，可设置：

```dotenv
HF_ENDPOINT=https://hf-mirror.com
```

## 示例问题

- 宫保鸡丁怎么做？
- 红烧肉需要哪些食材？
- 推荐几道简单的素菜。
- 今天有什么容易做的汤？

## 配置

主要配置位于 `code/C8/config.py`：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `data_path` | `data/C8/cook` | 菜谱 Markdown 数据目录 |
| `index_save_path` | `code/C8/vector_index` | FAISS 索引缓存目录 |
| `embedding_model` | `BAAI/bge-small-zh-v1.5` | 向量嵌入模型 |
| `llm_model` | `kimi-k2.6` | 生成模型 |
| `top_k` | `3` | 最终返回的检索结果数 |
| `temperature` | `1.0` | `kimi-k2.6` 支持的生成温度 |

## 本地检查

以下检查不调用外部 API，也不需要安装项目依赖：

```bash
python -m compileall -q code/C8
python -m unittest discover -s tests -v
```

## 安全说明

- `.env` 已被 `.gitignore` 排除，不要提交真实 API Key。
- `vector_index`、模型文件、虚拟环境和 Python 缓存不会进入 Git。
- 如果密钥曾经进入 Git 历史，应立即在服务商控制台撤销并重新生成。

## 数据与来源

菜谱数据来自 HowToCook，该项目使用 Unlicense。代码来自 All-in-RAG 教程的第八章。
上游 All-in-RAG 仓库目前没有根目录许可证文件，因此本仓库不擅自追加开源许可证；
详细来源和复用说明见 [NOTICE.md](NOTICE.md)。
