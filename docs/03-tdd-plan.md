# TDD-Plan — GlassesScraper MVP

## Philosophie
Tests zuerst, Code danach. Red → Green → Refactor.
Bauen von innen nach außen: Logik zuerst, Browser zuletzt.

## Test-Pyramide

```
         ╱╲
        ╱  ╲          E2E (3 Tests)
       ╱ E2E╲         Live SBG + CAPTCHA
      ╱──────╲
     ╱        ╲        Integration (13 Tests)
    ╱Integration╲     Fixtures, Pipeline, Pagination, Multivariant
   ╱──────────────╲
  ╱                ╲    Unit Tests (70 Tests)
 ╱   Unit Tests     ╲  Config, Models, Filters, Parser, Retry,
╱────────────────────╲  RateLimiter, Validators, State, Exporter

Gesamt: ~103 Tests | Laufzeit: < 1 min (ohne E2E)
```

## Layer-Reihenfolge

### Tag 1: Fundament
**AM — Layer 1: Config + Models + Validators (~15 Tests)**
- test_config_loads_valid_yaml
- test_config_rejects_min_greater_max
- test_config_rejects_negative_values
- test_config_default_values
- test_frame_creation, test_frame_pd_calculation
- test_frame_category_ideal/larger/out
- test_frame_to_dict, test_frame_equality
- test_validate_plausible/implausible_a/b/dbl
- test_validate_price, test_validate_url
- test_validate_decimal_formats

**PM — Layer 2: Filters (~15 Tests)**
- test_perfect_match, test_larger_match
- test_reject_a_too_large/small
- test_reject_b_too_large
- test_reject_dbl_too_small/large
- test_reject_frame_pd_too_low/high
- test_missing_b_still_passes
- test_missing_a/dbl_fails
- test_edge_case_exact_boundaries

### Tag 2: Intelligenz
**AM — Layer 3: Dimension Parser (~20 Tests)**
- test_parse_standard_format (50-21-145)
- test_parse_with_spaces, test_parse_in_text
- test_parse_labeled_english/german
- test_parse_html_table
- test_parse_aliases_a/b/dbl
- test_parse_no_dimensions, test_parse_partial
- test_parse_ignores_irrelevant_numbers
- test_parse_multiple_sizes (Multivariant!)
- test_parse_mm_unit_variations

**PM — Layer 3b: Errors + Retry + RateLimiter (~15 Tests)**
- test_retry_succeeds_on_second_attempt
- test_retry_respects_max_retries
- test_retry_exponential_backoff_timing
- test_retry_only_retries_retryable_errors
- test_retry_rate_limit_uses_retry_after
- test_rate_limiter_adaptive_slow/fast_server
- test_rate_limiter_hard_limit
- test_rate_limiter_resets_after_pause
- test_robots_allowed/disallowed

### Tag 3: Shop-Logik
**Vormittag: Fixtures sammeln (manuell, ~1h)**

**AM — Layer 4: SBG Extraktion + Multivariant (~15 Tests)**
- test_build_catalog_url
- test_extract_product_links_from_catalog
- test_detect_next_page, test_detect_last_page
- test_extract_dimensions_from_product
- test_extract_product_info
- test_product_missing_dimensions
- test_extract_product_type
- test_selector_not_found_raises_error
- test_fallback_selectors
- test_extract_all_size_variants
- test_full_pipeline_match/reject

**PM — Layer 4b: Pagination + State (~10 Tests)**
- test_pagination_numbered, test_pagination_empty
- test_pagination_loop_detection
- test_url_deduplication
- test_state_save, test_state_resume
- test_state_handles_corruption
- test_total_count_mismatch_warning

### Tag 4: Zusammenbau
**AM — Layer 5: Orchestrator (~10 Tests)**
- test_orchestrator_processes_all_pages
- test_orchestrator_retries_on_timeout
- test_orchestrator_stops_on_bot_detection
- test_orchestrator_respects_robots_txt
- test_orchestrator_recovery_after_error
- test_orchestrator_stats_tracking
- test_orchestrator_progress_callback
- test_orchestrator_respects_max_pages
- test_orchestrator_deduplicates

**PM — Layer 6: Exporter (~8 Tests)**
- test_export_csv, test_export_csv_empty
- test_export_csv_umlauts
- test_export_json
- test_export_timestamp_in_filename
- test_export_grouped_by_model
- test_export_summary

### Tag 5: Live
**AM — Layer 7: Browser + E2E (~5 Tests)**
- test_browser_launches
- test_browser_stealth_active
- test_browser_cookie_banner_dismissed
- test_captcha_detection
- test_e2e_live_sbg (1 Seite, echte Daten)

**PM: Bugfixes, Refactoring, Dokumentation**
