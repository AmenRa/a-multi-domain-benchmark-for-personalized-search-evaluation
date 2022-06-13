# A Multi-domain Benchmark for Personalized Search Evaluation

We provide large-scale multi-domain benchmark datasets for Personalized Search.

The datasets can be found [here](https://zenodo.org/record/6606557).

## Folder structure of each dataset
```
- train:
  - queries.jsonl
  - query_ids.txt
- val:
  - bm25_run.json
  - qrels.json
  - queries.jsonl
  - query_ids.txt
- test:
  - bm25_run.json
  - qrels.json
  - queries.jsonl
  - query_ids.txt
- collection.jsonl
- fos_hierarachies.jsonl
- in_refs.jsonl
- out_refs.jsonl
- has_authors.jsonl
- authors.jsonl
- affiliations.jsonl
- conference_instances.jsonl
- conference_series.jsonl
- journals.jsonl
- bm25_config.json
```

## File descriptions

### `queries.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "text": ...
  "rel_doc_ids": ...      # IDs of the relevant documents
  "user_id": ...          # Same as `author_id` in other files
  "user_doc_ids": ...     # IDs of the associated user documents
  "bm25_doc_ids": ...     # IDs of the documents retrieved by BM25
  "bm25_doc_scores": ...  # Scores assigned by BM25 to the retrieved documents
  "timestamp": ...
}
```

### `collection.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "title": ...
  "text": ...
  "keywords": ...
  "fields_of_study": ...
  "publication_date": ...
  "timestamp": ...
  "conference_instance_id": ...
  "conference_series_id": ...
  "journal_id": ...
  "issue_id": ...
  "volume": ...
  "publisher": ...
  "doi": ...
}
```

### `authors.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "name": ...
  "affiliation_id": ...
  "docs": [{"doc_id": "...", "timestamp": ...}, ...]
}
```

### `has_authors.jsonl`
Each JSON line is as follows:
```python
{
  "doc_id": ...
  "timestamp": ...
  "author_ids": ["123678452", ...]
}
```

### `in_refs.jsonl` (incoming reference)
Each JSON line is as follows:
```python
{
  "doc_id": ...
  "in_refs": [{"doc_id": "...", "timestamp": ...}, ...]
}
```

### `out_refs.jsonl` (outgoing reference)
Each JSON line is as follows:
```python
{
  "doc_id": ...
  "timestamp": ...
  "out_refs": ["2048600620", ...]
}
```

### `affiliations.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "name": ...   # Name of the institution
}
```

### `conference_instances.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "name": ...
  "conference_series_id": ...
}
```

### `conference_series.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "name": ...
}
```

### `journals.jsonl`
Each JSON line is as follows:
```python
{
  "id": ...
  "name": ...
}
```

### `fields_of_study_hierarchies.jsonl`
Fields of studies associated with the documents have a hierarchical tree structure.  
Each JSON line is as follows:
```python
{
  "id": ...
  "hierarchy": ...
}
```

<!-- - Install WGET

- Download MAG data  
  ```bash
  sh download_mag.sh
  ```

- Download Elasticsearch
  ```bash
  sh download_es.sh
  ```

- Follow run.sh, for BM25 stuff you need to start Elasticsearch first `sh start_es.sh` -->
