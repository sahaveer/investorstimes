# Graph Report - C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes  (2026-04-19)

## Corpus Check
- 17 files · ~1,079,440 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 131 nodes · 175 edges · 14 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `search_screener1()` - 19 edges
2. `check_rows()` - 8 edges
3. `scrape_all_listed()` - 8 edges
4. `getedgedriver()` - 7 edges
5. `is_cloud()` - 6 edges
6. `stmt_for_qoq()` - 6 edges
7. `create_image()` - 5 edges
8. `write_tags_to_txt()` - 5 edges
9. `get_reference_data()` - 4 edges
10. `get_all_listed_stocks()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `search_screener1()` --calls--> `create_doc()`  [INFERRED]
  C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\screenerpage.py → C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\create_database.py
- `scrape_all_listed()` --calls--> `insert_dict()`  [INFERRED]
  C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\screenerpage.py → C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\create_database.py
- `search_screener1()` --calls--> `get_tables()`  [INFERRED]
  C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\screenerpage.py → C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\fundamentals.py
- `getedgedriver()` --calls--> `is_cloud()`  [INFERRED]
  C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\processdriver.py → C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\config.py
- `getchromedriver()` --calls--> `is_cloud()`  [INFERRED]
  C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\processdriver.py → C:\Users\Sahaveer\PycharmProjects\webapp\Scripts\investorstimes\config.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (10): create_doc(), get_all_listed_stocks(), get_avoid_list(), insert_dict(), Fetch the list of stocks to avoid (e.g., those that return 404)., Save user insights for a stock in CompMetadata., Fetch all listed stocks from MongoDB, excluding the avoid list., Seed the StocksList collection from a local text file, excluding avoid list. (+2 more)

### Community 1 - "Community 1"
Cohesion: 0.17
Nodes (16): handle_document(), handle_message(), insert_list(), getedgedriver(), df_to_dict(), is_404(), login_screener(), main() (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (11): ami_notes_from_database1(), amibroker_notes_csv_quarterly(), amibroker_notes_csv_yearly(), amibroker_notes_insights(), analyse_df(), analyse_Q_df(), analyse_Y_df(), develop_quarterly() (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (10): get_reference_data(), Save a DataFrame as reference data in MongoDB., Fetch reference data from MongoDB as a DataFrame., save_reference_data(), get_yahoocode(), bsecodenum_bsecodename(), bseSCNAME_SCCODE(), dict_from_bse_csv() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (8): Config, get_mongodb_uri(), is_cloud(), Check if the application is running in Streamlit Cloud., add_to_avoid_list(), Add a stock code to the avoid list and remove it from the all_listed list., write_tags_to_txt(), getchromedriver()

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (2): main(), soup_Statistics()

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (8): bar_line(), both_lines(), check_rows(), go_bar(), group_2_bars(), group_3_bars(), qoq_growth(), Check if all rows exist in the DataFrame index.

### Community 7 - "Community 7"
Cohesion: 0.48
Nodes (5): box_text(), create_image(), create_instaimage(), resize(), wrap_draw_text()

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): getltp(), main()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Returns (email, password) for Screener.in

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Returns (token, chat_name, scraper_chat) for Telegram

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **13 isolated node(s):** `Config`, `Check if the application is running in Streamlit Cloud.`, `Returns (email, password) for Screener.in`, `Returns (token, chat_name, scraper_chat) for Telegram`, `Save a DataFrame as reference data in MongoDB.` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (1 nodes): `Returns (email, password) for Screener.in`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Returns (token, chat_name, scraper_chat) for Telegram`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `variables.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Admin.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `search_screener1()` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `write_tags_to_txt()` connect `Community 4` to `Community 1`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `get_reference_data()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `search_screener1()` (e.g. with `handle_message()` and `handle_document()`) actually correct?**
  _`search_screener1()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `scrape_all_listed()` (e.g. with `getedgedriver()` and `add_to_avoid_list()`) actually correct?**
  _`scrape_all_listed()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `getedgedriver()` (e.g. with `handle_message()` and `handle_document()`) actually correct?**
  _`getedgedriver()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `is_cloud()` (e.g. with `write_tags_to_txt()` and `getedgedriver()`) actually correct?**
  _`is_cloud()` has 3 INFERRED edges - model-reasoned connections that need verification._