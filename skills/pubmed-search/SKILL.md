---
name: pubmed-search
description: "Use when searching PubMed or biomedical literature, finding papers, recent studies, publications, clinical or scientific evidence, citations, abstracts, PMID records, or research on a health/life-science topic."
---

# PubMed Search

Search NCBI PubMed for scientific literature. This skill supports two approaches:
1. **BioPython Entrez (Recommended)** - Python-based, recommended for most workflows
2. **Direct E-utilities REST API** - For complex queries, systematic reviews, and batch operations

## When to Use

- User asks to find papers on a topic
- User wants recent publications in a field
- User asks for references or citations
- User wants to know the state of research on a topic
- Constructing complex Boolean/MeSH queries
- Systematic literature reviews or meta-analyses

## Approach 1: BioPython Entrez (Recommended)

Use BioPython's Entrez module for a clean Python interface.

### 1. Set up Entrez

```python
from Bio import Entrez
Entrez.email = "medclaw@freedomai.com"
```

### 2. Search PubMed

```python
# Search
handle = Entrez.esearch(db="pubmed", term="CRISPR delivery methods", retmax=20, sort="date")
record = Entrez.read(handle)
handle.close()

id_list = record["IdList"]
print(f"Found {record['Count']} results, showing top {len(id_list)}")
```

### 3. Fetch article details

```python
# Fetch details
handle = Entrez.efetch(db="pubmed", id=id_list, rettype="xml")
records = Entrez.read(handle)
handle.close()

for article in records['PubmedArticle']:
    medline = article['MedlineCitation']
    pmid = str(medline['PMID'])
    title = medline['Article']['ArticleTitle']
    
    # Get authors
    authors = medline['Article'].get('AuthorList', [])
    first_author = f"{authors[0].get('LastName', '')} {authors[0].get('Initials', '')}" if authors else "Unknown"
    
    # Get journal and year
    journal = medline['Article']['Journal']['Title']
    pub_date = medline['Article']['Journal']['JournalIssue'].get('PubDate', {})
    year = pub_date.get('Year', 'N/A')
    
    # Get abstract
    abstract_parts = medline['Article'].get('Abstract', {}).get('AbstractText', [])
    abstract = ' '.join(str(a) for a in abstract_parts)[:300]
    
    print(f"PMID: {pmid}")
    print(f"Title: {title}")
    print(f"Authors: {first_author} et al.")
    print(f"Journal: {journal} ({year})")
    print(f"Abstract: {abstract}...")
    print(f"Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
    print()
```

### 4. Output format for WhatsApp

```
*PubMed Search: "CRISPR delivery methods"*
_Found 1,234 results. Top 5:_

*1.* Lipid nanoparticle-mediated CRISPR delivery...
   _Smith J et al. — Nature (2026)_
   PMID: 12345678
   pubmed.ncbi.nlm.nih.gov/12345678
```

### 5. Advanced searches

Support these query patterns:
- `"CRISPR"[Title] AND "delivery"[Title]` -- title-specific
- `"2026"[Date - Publication]` -- date filter
- `"Nature"[Journal]` -- journal filter
- `review[Publication Type]` -- type filter

### 6. Follow-up suggestions

After showing results, suggest:
- "Want me to summarize any of these papers?"
- "Should I search with different keywords?"
- "Want me to find related papers to any of these?"

## Approach 2: Direct E-utilities REST API

For advanced Boolean queries, MeSH terms, systematic reviews, and batch operations.

### API Endpoints

1. **ESearch** - Search database and retrieve PMIDs
2. **EFetch** - Download full records in various formats
3. **ESummary** - Get document summaries
4. **EPost** - Upload UIDs for batch processing
5. **ELink** - Find related articles and linked data

### Basic Workflow

```python
import requests

# Step 1: Search for articles
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # Optional but recommended
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# Step 2: Fetch article details
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

### Rate Limits
- Without API key: 3 requests/second
- With API key: 10 requests/second
- Always include User-Agent header

### Advanced Search Query Construction

Use Boolean operators, field tags, and MeSH terms for precise searching.

**Example Queries:**
```
# Recent systematic reviews on diabetes treatment
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Clinical trials comparing two drugs
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Author-specific research
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**Field Tags:**
- `[au]` - Author
- `[ti]` - Title
- `[ab]` - Abstract
- `[mh]` - MeSH terms (includes narrower terms)
- `[majr]` - Major MeSH topic
- `[pt]` - Publication type
- `[dp]` - Publication date
- `[la]` - Language
- `[nm]` - Substance name
- `[tiab]` - Title or abstract

**MeSH Subheadings:**
- `/diagnosis` - Diagnostic methods
- `/drug therapy` - Pharmaceutical treatment
- `/epidemiology` - Disease patterns and prevalence
- `/etiology` - Disease causes
- `/prevention & control` - Preventive measures
- `/therapy` - Treatment approaches

**Publication Types** (use `[pt]` field tag):
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Guideline

**Date Filtering:**
- Single year: `2024[dp]`
- Date range: `2020:2024[dp]`
- Specific date: `2024/03/15[dp]`

**Text Availability:**
- Free full text: `AND free full text[sb]`
- Has abstract: `AND hasabstract[text]`

### Citation Matching

```text
# By PMID
12345678[pmid]

# By DOI
10.1056/NEJMoa123456[doi]

# By PMC ID
PMC123456[pmc]
```

### Systematic Literature Reviews

**PICO Framework:**
```
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**Comprehensive Search Strategy:**
```
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND english[la]
```

### Search Refinement
1. Start broad, review results
2. Add specificity with field tags
3. Apply date and publication type filters
4. Use Advanced Search to view query translation
5. Combine search history for complex queries

### Best Practices for API Usage
- Obtain API key for higher rate limits (10 req/sec vs 3 req/sec)
- Use history server for result sets > 500 articles
- Implement exponential backoff for rate limit handling
- Cache results locally to minimize redundant requests
- Always include descriptive User-Agent header

### Export and Citation Management
- .nbib files for reference managers (Zotero, Mendeley, EndNote)
- AMA, MLA, APA, NLM citation styles
- CSV for data analysis
- XML for programmatic processing

## Reference Files

Detailed documentation is available in the `references/` directory:

- **references/api_reference.md** - Complete E-utilities API documentation
- **references/search_syntax.md** - PubMed search syntax including field tags, Boolean operators, wildcards
- **references/common_queries.md** - Example queries for various research scenarios and methodologies

## Limitations

- PubMed provides citations and abstracts (not always full text)
- Full text access depends on publisher or open access status
- Results display limited to 10,000 maximum
- Search history expires after 8 hours of inactivity
- Some content requires subscription or payment
