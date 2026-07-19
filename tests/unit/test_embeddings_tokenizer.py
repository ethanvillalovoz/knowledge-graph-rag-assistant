from backend.app.handlers import embeddings_handler


def test_existing_tokenizer_resources_do_not_trigger_download(monkeypatch):
    discovered = []

    def find(resource_path):
        discovered.append(resource_path)
        return object()

    def unexpected_download(*_args, **_kwargs):
        raise AssertionError("Existing NLTK resources must not be downloaded again")

    monkeypatch.setattr(embeddings_handler.nltk.data, "find", find)
    monkeypatch.setattr(embeddings_handler.nltk, "download", unexpected_download)

    embeddings_handler.ensure_sentence_tokenizer()

    assert discovered == ["tokenizers/punkt", "tokenizers/punkt_tab"]


def test_missing_tokenizer_resources_are_downloaded_lazily(monkeypatch):
    downloads = []

    def missing(_resource_path):
        raise LookupError

    def download(package_name, *, quiet):
        downloads.append((package_name, quiet))
        return True

    monkeypatch.setattr(embeddings_handler.nltk.data, "find", missing)
    monkeypatch.setattr(embeddings_handler.nltk, "download", download)

    embeddings_handler.ensure_sentence_tokenizer()

    assert downloads == [("punkt", True), ("punkt_tab", True)]
