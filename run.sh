# Create raw_data folder
# mkdir -p raw_data

# Create datasets folder
# mkdir -p datasets

# PARSING ----------------------------------------------------------------------
# python -m parsing.abstracts
# python -m parsing.affiliations
# python -m parsing.authors
# python -m parsing.conference_instances
# python -m parsing.conference_series
# python -m parsing.field_of_study_children
# python -m parsing.fields_of_study
# python -m parsing.journals
# python -m parsing.paper_authors
# python -m parsing.paper_field_of_study
# python -m parsing.paper_languages
# python -m parsing.paper_references
# python -m parsing.paper_tags
# python -m parsing.papers
# python -m parsing.citation_contexts

# PROCESSING -------------------------------------------------------------------
# python -m processing.0_fos
# python -m processing.1_paper_ids_by_lang
# python -m processing.2_paper_ids_by_fos
# python -m processing.3_paper_ids_has_abstract
# python -m processing.4_paper_ids_has_date
# python -m processing.6_paper_ids_has_author
# python -m processing.7_paper_ids_has_tags
python -m processing.8_paper_ids_is_referenced

# python -m processing.9_papers
# python -m processing.10_abstracts
# python -m processing.11_paper_author_affiliations
# python -m processing.12_tags
# python -m processing.13_conference_instances
# python -m processing.14_conference_series
# python -m processing.15_journals
# python -m processing.16_paper_references
# python -m processing.17_authors

# python -m processing.18_add_abstracts_to_papers
# python -m processing.19_add_tags_to_papers

# python -m processing.20_generate_queries
# python -m processing.21_split_queries

# python -m processing.20_generate_queries --kind=keywords
# python -m processing.21_split_queries




# BM25 -------------------------------------------------------------------------
fos="computer_science"

for FOS in $fos;
do
    python -m bm25.1_prepare_collection_for_indexing --fos=$FOS
    python -m bm25.2_index_collection --fos=$FOS
    python -m bm25.3_search_bm_25_config --fos=$FOS
    python -m bm25.4_compute_bm25_results --fos=$FOS
done

# Finalize dataset -------------------------------------------------------------
fos="computer_science"

for FOS in $fos;
do
    python -m finalize_data.1_split_queries --fos=$FOS
    python -m finalize_data.2_extract_qrels --fos=$FOS
    python -m finalize_data.3_extract_bm25_runs --fos=$FOS
    python -m finalize_data.4_extract_query_ids --fos=$FOS
done
