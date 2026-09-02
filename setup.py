"""Package configuration for MemoryGraft."""

from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).resolve().parent


def read_requirements(path: Path) -> list[str]:
    """Read active requirement lines from a pip requirements file."""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

RAG_REQUIREMENTS = [
    "llama-index-core==0.10.15",
    "llama-index-embeddings-azure-openai==0.1.6",
    "llama-index-embeddings-openai==0.1.5",
    "llama-index-embeddings-gemini==0.1.6",
    "llama-index-embeddings-ollama==0.1.2",
    "llama-index-llms-azure-openai==0.1.4",
    "llama-index-readers-file==0.1.4",
    "llama-index-retrievers-bm25==0.1.3",
    "llama-index-vector-stores-faiss==0.1.1",
    "llama-index-vector-stores-elasticsearch==0.1.6",
    "llama-index-vector-stores-chroma==0.1.6",
    "llama-index-postprocessor-cohere-rerank==0.1.4",
    "llama-index-postprocessor-colbert-rerank==0.1.1",
    "llama-index-postprocessor-flag-embedding-reranker==0.1.2",
    "docx2txt==0.8",
]

setup(
    name="memorygraft",
    version="1.0.0",
    description="Persistent compromise of LLM agents through poisoned experience retrieval",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Jacobhhy/MemoryGraft",
    author="Saksham Sahai Srivastava and Haoyu He",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9,<3.12",
    install_requires=read_requirements(ROOT / "requirements.txt"),
    extras_require={"rag": RAG_REQUIREMENTS, "test": [*RAG_REQUIREMENTS, "pytest>=7,<9"]},
    include_package_data=True,
    entry_points={"console_scripts": ["memorygraft=memorygraft.experiment:main"]},
)
