import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Search & RAG Portal", page_icon="🧠", layout="wide")

st.title("🧠 AI Knowledge Portal")
st.caption("Powered by FastAPI, ChromaDB, all-MiniLM-L6-v2, and Gemini")

# Sidebar health check status
try:
    health = requests.get(f"{API_URL}/health").json()
    st.sidebar.success(f"API Online | DB Records: {health.get('database_items', 0)}")
except Exception:
    st.sidebar.error("API Offline! Start backend: `uvicorn app.main:app --reload`")

# Three distinct tabs
tab1, tab2, tab3 = st.tabs(["💬 Ask AI (RAG)", "🔍 Raw Vector Search", "➕ Ingest New Data"])

# TAB 1: ASK AI (RAG)
with tab1:
    st.header("Ask the Knowledge Base")
    st.markdown("The AI will read the vector database and write a custom answer based *only* on the ingested data.")
    
    rag_query = st.text_input("Ask a question:", placeholder="e.g., What kind of developer roles are available?")
    
    if st.button("Generate Answer", type="primary"):
        if rag_query.strip():
            with st.spinner("Searching DB and generating answer..."):
                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={"query_text": rag_query, "limit": 3}
                    ).json()
                    
                    if "ai_answer" in response:
                        st.success("Answer Generated!")
                        st.write(response["ai_answer"])
                        
                        with st.expander("View Source Documents Used by AI"):
                            for idx, doc in enumerate(response.get("retrieved_sources", []), 1):
                                st.caption(f"**Source {idx}:** {doc}")
                    else:
                        st.error(response.get("detail", "Error generating response."))
                except Exception as e:
                    st.error(f"Failed to reach API: {e}")
        else:
            st.warning("Please enter a question.")

# TAB 2: RAW SEARCH
with tab2:
    st.header("Search by Meaning")
    query_text = st.text_input("Enter natural language query:", placeholder="e.g., someone skilled in python")
    limit = st.slider("Max Results:", min_value=1, max_value=10, value=3)
    
    if st.button("Run Vector Search"):
        if query_text.strip():
            with st.spinner("Executing vector search..."):
                try:
                    response = requests.post(
                        f"{API_URL}/search",
                        json={"query_text": query_text, "limit": limit}
                    ).json()
                    
                    matches = response.get("matches", [])
                    if matches:
                        st.subheader(f"Results for: '{query_text}'")
                        for idx, match in enumerate(matches, 1):
                            with st.container():
                                st.markdown(f"### {idx}. ID: `{match['id']}`")
                                st.write(f"**Content:** {match['content']}")
                                if match.get("metadata"):
                                    st.caption(f"**Metadata:** {match['metadata']}")
                                st.caption(f"**Distance Score:** {round(match.get('distance', 0), 4)}")
                                st.divider()
                    else:
                        st.info("No matching items found.")
                except Exception as e:
                    st.error(f"Failed to reach API: {e}")
        else:
            st.warning("Please enter a search query.")

# TAB 3: INGESTION
with tab3:
    st.header("Add New Document")
    doc_id = st.text_input("Document ID", placeholder="doc_101")
    content = st.text_area("Document Content", placeholder="Enter text description to store in vector DB...")
    category = st.selectbox("Category Metadata", ["Movies", "Jobs", "Lost & Found", "Other"])
    
    if st.button("Ingest Document"):
        if doc_id and content:
            payload = {
                "id": doc_id,
                "content": content,
                "metadata": {"category": category}
            }
            try:
                res = requests.post(f"{API_URL}/ingest", json=payload).json()
                st.success(res.get("message", "Item successfully ingested!"))
            except Exception as e:
                st.error(f"Failed to ingest item: {e}")
        else:
            st.warning("Please complete both ID and Content fields.")