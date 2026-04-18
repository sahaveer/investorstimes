import streamlit as st
import os
import pandas as pd
import time
import create_database
import config
import main # To access shared functions like save_screener1

st.set_page_config(page_title="iTimes Admin", page_icon="🔐", layout="wide")

st.title("🔐 Administrator Portal")

if config.is_cloud():
    st.warning("⚠️ Most Admin tools are disabled in Cloud mode.")
    # Only CSV uploads are allowed in cloud
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BSE Reference Update")
        bse_file = st.file_uploader("Upload Select.csv", type=['csv'], key="cloud_bse")
        if bse_file:
            bse_df = pd.read_csv(bse_file)
            if create_database.save_reference_data('bse_select', bse_df):
                st.success("BSE Data Updated!")
    with col2:
        st.subheader("NSE Reference Update")
        nse_file = st.file_uploader("Upload NSE Bhavcopy", type=['csv'], key="cloud_nse")
        if nse_file:
            nse_df = pd.read_csv(nse_file)
            if create_database.save_reference_data('nse_bhav', nse_df):
                st.success("NSE Data Updated!")
        
        st.subheader("BSE Names Update")
        sccode_file = st.file_uploader("Upload sccodenames.CSV", type=['csv'], key="cloud_sccode")
        if sccode_file:
            sccode_df = pd.read_csv(sccode_file)
            if create_database.save_reference_data('sccodenames', sccode_df):
                st.success("BSE Names Updated!")
else:
    st.info("💻 Running in Local/Admin Mode")
    
    # 1. Sync Section
    st.subheader("📦 Master Data Sync")
    col1, col2 = st.columns([2,1])
    with col1:
        st.write("Push your master watchlist to the Cloud Database.")
        uploaded_master = st.file_uploader("Upload New Master List (.txt)", type=['txt'], key="master_upload")
    with col2:
        if st.button("🔄 Sync Local File", use_container_width=True, help="Syncs the local alllisted.txt from your server"):
            local_file = './watchlist/alllisted.txt'
            if os.path.exists(local_file):
                new_stocks = create_database.seed_stocks_from_file(local_file)
                st.session_state['listed_stocks'] = new_stocks
                st.success("Synced Local File!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Local file missing!")
        
        if uploaded_master:
            if st.button("⬆️ Upload & Sync", use_container_width=True, type="primary"):
                content = uploaded_master.read().decode("utf-8")
                # Parse, sanitize, and filter
                raw_stocks = [line.strip().upper() for line in content.splitlines() if line.strip()]
                avoid_list = create_database.get_avoid_list()
                stocks = [s for s in raw_stocks if s not in avoid_list]
                
                create_database.stocks_list_col.update_one({"_id": "all_listed"}, {"$set": {"stocks": stocks}}, upsert=True)
                st.session_state['listed_stocks'] = stocks
                st.success(f"Uploaded and Synced {len(stocks)} stocks! (Filtered out {len(raw_stocks) - len(stocks)} avoided stocks)")
                time.sleep(1)
                st.rerun()

    st.divider()

    # 2. Scraper Section
    st.subheader("🚀 Targeted Scraper")
    st.write("Scrape specific stocks on-demand without adding them to your permanent watchlist.")
    
    scrape_input = st.text_area("Option 1: Paste Symbols", placeholder="RELIANCE, TCS, 500325", help="Comma separated NSE symbols or BSE codes.")
    scrape_file = st.file_uploader("Option 2: Upload symbols.txt", type=['txt'])
    
    if st.button("🔥 Start Scrape Process", type="primary", use_container_width=True):
        all_codes = []
        if scrape_input:
            all_codes.extend([c.strip().upper() for c in scrape_input.split(",") if c.strip()])
        if scrape_file:
            content = scrape_file.read().decode("utf-8")
            for line in content.splitlines():
                parts = line.split(",")
                all_codes.extend([c.strip().upper() for c in parts if c.strip()])
        
        # Preserve Order & Unique
        seen = set()
        unique_codes = [x for x in all_codes if not (x in seen or seen.add(x))]

        if unique_codes:
            st.info(f"Scraping {len(unique_codes)} stocks in order...")
            # Note: We use main.main_status if defined, or just st.empty()
            status_p = st.empty()
            main.save_screener1(unique_codes, force=True, status_placeholder=status_p)
            st.success("Batch completed! Clearing cache...")
            st.cache_resource.clear()
            time.sleep(1)
            st.rerun()
        else:
            st.warning("No symbols found.")
    
    st.divider()
    
    # 3. Avoid List Management
    st.subheader("🚫 Avoid List (Invalid/No-Data Stocks)")
    avoid_list = create_database.get_avoid_list()
    if avoid_list:
        st.info(f"The following {len(avoid_list)} stocks are being skipped because they return 404 errors or have no fundamental data (e.g., ETFs).")
        st.write(", ".join(avoid_list))
        if st.button("🗑️ Clear Avoid List", use_container_width=True):
            create_database.stocks_list_col.update_one({"_id": "avoid_list"}, {"$set": {"stocks": []}})
            st.success("Avoid list cleared!")
            time.sleep(1)
            st.rerun()
    else:
        st.success("Avoid list is empty. No stocks are currently blacklisted.")

    st.divider()
    st.session_state.path_download = st.text_input("Local Download Path", value='C:/Users/Sahaveer/Downloads/')
