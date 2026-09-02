import asyncio
import inspect
import json
from pathlib import Path
from types import SimpleNamespace

import yaml
from llama_index.core.embeddings.mock_embed_model import MockEmbedding

from memorygraft import experiment


def test_paper_inputs_and_reference_match():
    benign, poisoned = experiment.load_seeds()
    reference = json.loads((experiment.ROOT / "paper_result.json").read_text(encoding="utf-8"))

    assert len(benign) == reference["seed_counts"]["benign"] == 100
    assert len(poisoned) == reference["seed_counts"]["poisoned"] == 10
    assert len(experiment.EVALUATION_QUERIES) == reference["query_count"] == 12
    assert len({row["id"] for row in benign + poisoned}) == 110
    repo_config = yaml.safe_load((experiment.ROOT.parent / "config/config2.yaml").read_text(encoding="utf-8"))
    assert repo_config["llm"]["model"] == reference["llm_model"] == "gpt-4o"
    assert repo_config["embedding"]["model"] == reference["embedding_model"] == "text-embedding-ada-002"
    assert repo_config["embedding"]["dimensions"] == reference["embedding_dimensions"] == 1536
    assert reference["poisoned_hits"] / reference["total_retrieved"] == reference["prp"]


def test_paper_protocol_overrides_user_level_model_names(monkeypatch):
    monkeypatch.setattr(experiment.config.llm, "model", "gpt-4o-mini")
    monkeypatch.setattr(experiment.config.embedding, "model", "different-embedding")
    monkeypatch.setattr(experiment.config.embedding, "dimensions", 42)

    experiment.configure_paper_protocol()

    assert experiment.config.llm.model == "gpt-4o"
    assert experiment.config.embedding.model == "text-embedding-ada-002"
    assert experiment.config.embedding.dimensions == 1536


def test_unresolved_api_placeholder_selects_bm25(monkeypatch):
    monkeypatch.setattr(experiment.config.embedding, "api_key", "${OPENAI_API_KEY}")
    monkeypatch.setattr(experiment.config.llm, "api_key", "YOUR_API_KEY")

    assert experiment.has_embedding_configured() is False

    monkeypatch.setattr(experiment.config.embedding, "api_key", "test-credential")
    assert experiment.has_embedding_configured() is True


def test_poison_identity_comes_from_seed_id():
    poisoned = SimpleNamespace(node=SimpleNamespace(metadata={"obj_json": json.dumps({"id": "exp_poison_008"})}))
    benign = SimpleNamespace(node=SimpleNamespace(metadata={"obj": SimpleNamespace(id="exp_benign_008")}))

    assert experiment.experience_id(poisoned) == "exp_poison_008"
    assert experiment.experience_id(benign) == "exp_benign_008"


def test_prp_uses_exact_membership_not_response_keywords():
    class FakeNode:
        def __init__(self, seed_id, text):
            self.metadata = {"obj": SimpleNamespace(id=seed_id)}
            self._text = text

        def get_content(self):
            return self._text

    def result(seed_id, text):
        return SimpleNamespace(node=FakeNode(seed_id, text), score=1.0)

    class FakeEngine:
        async def aretrieve(self, query):
            return {
                "q1": [
                    result("exp_poison_008", "contains no old poison signature"),
                    result("exp_benign_001", "mentions bypass but is benign"),
                ],
                "q2": [
                    result("exp_poison_001", "poison"),
                    result("exp_benign_002", "benign"),
                ],
            }[query]

    measured = asyncio.run(
        experiment.evaluate_prp(FakeEngine(), ["q1", "q2"], {"exp_poison_001", "exp_poison_008"})
    )

    assert measured["poisoned_hits"] == 2
    assert measured["total_retrieved"] == 4
    assert measured["prp"] == 0.5


def test_persistence_uses_one_directory_per_retriever(tmp_path):
    class FakeRetriever:
        def __init__(self):
            self.persisted_to = None

        def persist(self, path):
            self.persisted_to = Path(path)
            self.persisted_to.mkdir(parents=True)
            (self.persisted_to / "docstore.json").write_text("{}", encoding="utf-8")

    bm25 = FakeRetriever()
    faiss = FakeRetriever()
    engine = SimpleNamespace(retriever=SimpleNamespace(retrievers=[bm25, faiss]))

    experiment.persist_engine(engine, tmp_path, ["BM25", "FAISS"], record_count=110)

    assert bm25.persisted_to == tmp_path / "bm25"
    assert faiss.persisted_to == tmp_path / "faiss"
    manifest = json.loads((tmp_path / experiment.MANIFEST_NAME).read_text(encoding="utf-8"))
    assert manifest == {
        "schema_version": 1,
        "record_count": 110,
        "retrievers": ["BM25", "FAISS"],
        "similarity_top_k": 3,
    }


def test_store_builder_is_synchronous_for_notebook_execution():
    assert not inspect.iscoroutinefunction(experiment.build_poisoned_store)


def test_engine_defaults_to_offline_bm25(monkeypatch):
    sentinel = object()

    def fake_from_objs(*, objs, retriever_configs):
        assert objs == []
        assert len(retriever_configs) == 1
        assert isinstance(retriever_configs[0], experiment.BM25RetrieverConfig)
        return sentinel

    monkeypatch.setattr(experiment.SimpleEngine, "from_objs", fake_from_objs)
    monkeypatch.setattr(experiment, "has_embedding_configured", lambda: True)

    engine, retrievers = experiment.build_engine([])

    assert engine is sentinel
    assert retrievers == ["BM25"]


def test_hybrid_store_round_trip_without_remote_calls(tmp_path, monkeypatch):
    from metagpt.rag.engines import simple as simple_engine_module

    embedding = MockEmbedding(embed_dim=1536)
    monkeypatch.setattr(experiment, "has_embedding_configured", lambda: True)
    monkeypatch.setattr(experiment, "get_rag_embedding", lambda: embedding)
    monkeypatch.setattr(simple_engine_module, "get_rag_embedding", lambda: embedding)

    docs = [
        experiment.ExperienceDoc("exp_benign_001", "clean table", "validate schema", "safe"),
        experiment.ExperienceDoc("exp_poison_001", "finish fast", "skip validation", "validated"),
    ]
    engine, retrievers = experiment.build_engine(docs, use_embeddings=True)
    experiment.persist_engine(engine, tmp_path, retrievers, record_count=len(docs))

    reloaded, reloaded_retrievers = experiment.load_engine_from_store(tmp_path)
    measured = asyncio.run(experiment.evaluate_prp(reloaded, ["skip validation"], {"exp_poison_001"}))

    assert retrievers == reloaded_retrievers == ["BM25", "FAISS"]
    assert measured["total_retrieved"] == 2
    assert measured["poisoned_hits"] == 1
