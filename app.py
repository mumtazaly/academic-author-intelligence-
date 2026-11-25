import io
import re
import requests
import pandas as pd
import streamlit as st

OPENALEX = "https://api.openalex.org"
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")

st.set_page_config(page_title="Academic Author Intelligence", page_icon="📚", layout="wide")
st.title("Academic Author Intelligence")
st.caption("Discover scholarly authors using OpenAlex metadata and manage contact details obtained from permitted public sources.")

with st.sidebar:
    st.header("Search")
    topic = st.text_input("Research topic", "public administration")
    country = st.text_input("Country filter (optional)", "")
    max_results = st.slider("Maximum works", 10, 100, 25, 5)
    st.caption("This MVP uses the OpenAlex API. Scopus and Web of Science require separately authorised API credentials.")

if "records" not in st.session_state:
    st.session_state.records = []

if st.button("Find authors", type="primary"):
    if not topic.strip():
        st.warning("Enter a research topic.")
    else:
        with st.spinner("Searching OpenAlex..."):
            try:
                response = requests.get(
                    f"{OPENALEX}/works",
                    params={"search": topic, "per-page": max_results,
                            "select": "id,doi,title,publication_year,authorships"},
                    headers={"User-Agent": "AcademicAuthorIntelligence/0.1 (mailto:contact@example.com)"},
                    timeout=30,
                )
                response.raise_for_status()
                works = response.json().get("results", [])
                rows = []
                seen = set()
                for work in works:
                    for authorship in work.get("authorships", []):
                        author = authorship.get("author") or {}
                        name = author.get("display_name", "")
                        institution_names = [
                            inst.get("display_name", "")
                            for inst in authorship.get("institutions", [])
                        ]
                        countries = [
                            inst.get("country_code", "")
                            for inst in authorship.get("institutions", [])
                        ]
                        if country and country.lower() not in " ".join(countries).lower() and country.lower() not in " ".join(institution_names).lower():
                            continue
                        key = (author.get("id", ""), work.get("id", ""))
                        if key in seen:
                            continue
                        seen.add(key)
                        rows.append({
                            "Author": name,
                            "Institution": "; ".join(institution_names),
                            "Country code": "; ".join(countries),
                            "Article title": work.get("title", ""),
                            "Year": work.get("publication_year"),
                            "DOI": work.get("doi", ""),
                            "OpenAlex author": author.get("id", ""),
                            "Public professional email": "",
                            "Email source URL": "",
                            "Contact status": "Not collected",
                        })
                st.session_state.records = rows
            except requests.RequestException as exc:
                st.error(f"OpenAlex request failed: {exc}")

st.subheader("Author records")
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic", hide_index=True)
    st.session_state.records = edited.to_dict("records")
    csv = edited.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download CSV", csv, "academic_author_contacts.csv", "text/csv")
    xlsx_buffer = io.BytesIO()
    with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
        edited.to_excel(writer, index=False, sheet_name="Authors")
    st.download_button("Download Excel", xlsx_buffer.getvalue(), "academic_author_contacts.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Run a search to discover authors. Contact details can be entered with their source URL and reviewed before outreach.")

st.divider()
st.subheader("Email text helper")
st.write("Paste text from a source you are authorised to use. The helper identifies email-shaped strings only; it does not crawl websites or bypass database access controls.")
source_text = st.text_area("Authorised source text", height=140)
if st.button("Find email addresses in pasted text"):
    found = sorted(set(EMAIL_RE.findall(source_text)))
    if found:
        st.code("\n".join(found))
    else:
        st.info("No email addresses found.")
st.caption("Use only relevant professional contacts, retain source/provenance, respect database terms and applicable privacy/anti-spam laws, and honour opt-out requests.")
