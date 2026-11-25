# Academic Author Intelligence

A starter Streamlit application for academic author discovery and contact-list management.

## Current MVP
- Searches scholarly works and author metadata through OpenAlex.
- Displays author names, affiliations, article titles, years, DOI links, and OpenAlex author IDs.
- Allows manual entry of professional contact details and their source URLs.
- Identifies email-shaped strings in text pasted by a user who is authorised to process that text.
- Exports the author table to CSV and Excel.

## Important limitations
- This is a standalone Streamlit web app, **not a DeepSeek plugin**.
- Scopus and Web of Science integrations are not enabled. They require separately authorised API credentials and must comply with each provider's licence and terms.
- The app does not crawl publisher websites, scrape subscription databases, bypass access controls, or harvest bulk personal contact data.
- Use professional contact information only for relevant communications, keep source/provenance records, comply with applicable privacy and anti-spam laws, and honour opt-out requests.

## Run locally
Python 3.10 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Next steps
1. Test the MVP locally or deploy it to a Streamlit-compatible host.
2. Add Scopus and Web of Science connectors after API access and permitted use are confirmed.
3. Add duplicate detection, email-source verification, suppression lists, and audit logs.
4. Investigate the specific DeepSeek integration interface before packaging this as a plugin.
