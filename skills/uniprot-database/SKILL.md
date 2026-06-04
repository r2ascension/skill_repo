---
name: uniprot-database
description: "Use when working on direct REST API access to UniProt. Protein searches, FASTA retrieval, ID mapping, Swiss-Prot/TrEMBL. For Python workflows with multiple databases, prefer bioservices (unified interface to 40+ services). Use this for direct HTTP/REST work or UniProt-specific control."
---

# UniProt Database

## Overview

UniProt is the world's leading comprehensive protein sequence and functional information resource. Search proteins by name, gene, or accession, retrieve sequences in FASTA format, perform ID mapping across databases, access Swiss-Prot/TrEMBL annotations via REST API for protein analysis.

## When to Use This Skill

This skill should be used when:
- Searching for protein entries by name, gene symbol, accession, or organism
- Retrieving protein sequences in FASTA or other formats
- Mapping identifiers between UniProt and external databases (Ensembl, RefSeq, PDB, etc.)
- Accessing protein annotations including GO terms, domains, and functional descriptions
- Batch retrieving multiple protein entries efficiently
- Querying reviewed (Swiss-Prot) vs. unreviewed (TrEMBL) protein data
- Streaming large protein datasets
- Building custom queries with field-specific search syntax

## Core Capabilities

### 1. Searching for Proteins

Search UniProt using natural language queries or structured search syntax.

**Common search patterns:**
```python
# Search by protein name
query = "insulin AND organism_name:\"Homo sapiens\""

# Search by gene name
query = "gene:BRCA1 AND reviewed:true"

# Search by accession
query = "accession:P12345"

# Search by sequence length
query = "length:[100 TO 500]"

# Search by taxonomy
query = "taxonomy_id:9606"  # Human proteins

# Search by GO term
query = "go:0005515"  # Protein binding
```

Use the API search endpoint: `https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**Supported formats:** JSON, TSV, Excel, XML, FASTA, RDF, TXT

**Python search function:**

```python
import requests

def search_uniprot(query, format='json', size=25):
    """Search UniProt with structured query syntax."""
    url = 'https://rest.uniprot.org/uniprotkb/search'
    params = {'query': query, 'format': format, 'size': size}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json() if format == 'json' else response.text

# Example: human kinases with structures
results = search_uniprot('organism_id:9606 AND keyword:kinase AND database:pdb AND reviewed:true')
for entry in results['results']:
    print(entry['primaryAccession'], entry['proteinDescription']['recommendedName']['fullName']['value'])
```

**Fetch a single entry by accession:**

```python
def fetch_uniprot(accession, format='fasta'):
    """Fetch a single UniProt entry. Formats: fasta, json, txt, xml, gff."""
    url = f'https://rest.uniprot.org/uniprotkb/{accession}.{format}'
    response = requests.get(url)
    response.raise_for_status()
    return response.text

sequence = fetch_uniprot('P53_HUMAN', 'fasta')
entry_json = fetch_uniprot('P04637', 'json')
```

### 2. Retrieving Individual Protein Entries

Retrieve specific protein entries by accession number.

**Accession number formats:**
- Classic: P12345, Q1AAA9, O15530 (6 characters: letter + 5 alphanumeric)
- Extended: A0A022YWF9 (10 characters for newer entries)

**Retrieve endpoint:** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

Example: `https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. Batch Retrieval and ID Mapping

Map protein identifiers between different database systems and retrieve multiple entries efficiently.

**Batch fetch by accessions:**

```python
def batch_fetch(accessions, format='fasta'):
    """Fetch multiple entries by accession list."""
    url = 'https://rest.uniprot.org/uniprotkb/accessions'
    params = {'accessions': ','.join(accessions), 'format': format}
    response = requests.get(url, params=params)
    return response.text

accessions = ['P04637', 'P53_HUMAN', 'Q9Y6K9']
sequences = batch_fetch(accessions)
```

**Stream large results with field selection:**

```python
def search_all(query, format='tsv', fields=None):
    """Stream all results for large queries (no pagination)."""
    url = 'https://rest.uniprot.org/uniprotkb/stream'
    params = {'query': query, 'format': format}
    if fields:
        params['fields'] = ','.join(fields)
    response = requests.get(url, params=params, stream=True)
    return response.text

# Get all human reviewed proteins with selected fields
all_human = search_all('organism_id:9606 AND reviewed:true',
                       fields=['accession', 'gene_names', 'protein_name'])
```

**ID Mapping workflow:**

```python
import time

def map_ids(ids, from_db, to_db):
    """Map identifiers between databases via UniProt ID mapping."""
    url = 'https://rest.uniprot.org/idmapping/run'
    response = requests.post(url, data={'ids': ','.join(ids), 'from': from_db, 'to': to_db})
    job_id = response.json()['jobId']

    # Poll for results
    while True:
        status = requests.get(f'https://rest.uniprot.org/idmapping/status/{job_id}')
        if 'results' in status.json() or 'failedIds' in status.json():
            break
        time.sleep(1)

    results = requests.get(f'https://rest.uniprot.org/idmapping/results/{job_id}')
    return results.json()

# Example: Ensembl gene IDs to UniProt
mapping = map_ids(['ENSG00000141510', 'ENSG00000171862'], 'Ensembl', 'UniProtKB')
for result in mapping['results']:
    print(result['from'], '->', result['to']['primaryAccession'])
```

**Common database codes for ID mapping:**

| Code | Database |
|------|----------|
| `UniProtKB` | UniProt accessions |
| `UniProtKB_AC-ID` | UniProt AC or ID |
| `Ensembl` | Ensembl gene ID |
| `RefSeq_Protein` | RefSeq protein |
| `PDB` | PDB ID |
| `GeneID` | NCBI Gene ID |
| `Gene_Name` | Gene symbols |

**ID Mapping workflow:**
1. Submit mapping job to: `https://rest.uniprot.org/idmapping/run`
2. Check job status: `https://rest.uniprot.org/idmapping/status/{jobId}`
3. Retrieve results: `https://rest.uniprot.org/idmapping/results/{jobId}`

**Supported databases for mapping:**
- UniProtKB AC/ID
- Gene names
- Ensembl, RefSeq, EMBL
- PDB, AlphaFoldDB
- KEGG, GO terms
- And many more (see `/references/id_mapping_databases.md`)

**Limitations:**
- Maximum 100,000 IDs per job
- Results stored for 7 days

### 4. Streaming Large Result Sets

For large queries that exceed pagination limits, use the stream endpoint:

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

The stream endpoint returns all results without pagination, suitable for downloading complete datasets.

### 5. Customizing Retrieved Fields

Specify exactly which fields to retrieve for efficient data transfer.

**Common fields:**
- `accession` - UniProt accession number
- `id` - Entry name
- `gene_names` - Gene name(s)
- `organism_name` - Organism
- `protein_name` - Protein names
- `sequence` - Amino acid sequence
- `length` - Sequence length
- `go_*` - Gene Ontology annotations
- `cc_*` - Comment fields (function, interaction, etc.)
- `ft_*` - Feature annotations (domains, sites, etc.)

**Example:** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

See `/references/api_fields.md` for complete field list.

### 6. Parsing and Extracting Data

**Extract annotations from JSON entry:**

```python
import json

# Fetch and parse a JSON entry
entry = json.loads(fetch_uniprot('P04637', 'json'))

accession = entry['primaryAccession']
gene_name = entry['genes'][0]['geneName']['value']
protein_name = entry['proteinDescription']['recommendedName']['fullName']['value']
sequence = entry['sequence']['value']
length = entry['sequence']['length']

# GO terms, domains, and PDB references
go_terms = [ref for ref in entry.get('uniProtKBCrossReferences', [])
            if ref['database'] == 'GO']
domains = [ref for ref in entry.get('uniProtKBCrossReferences', [])
           if ref['database'] == 'InterPro']
pdb_refs = [ref for ref in entry.get('uniProtKBCrossReferences', [])
            if ref['database'] == 'PDB']
```

**Retrieve specific fields as a DataFrame:**

```python
import pandas as pd
from io import StringIO

def get_fields(query, fields):
    """Get specific fields as a pandas DataFrame."""
    url = 'https://rest.uniprot.org/uniprotkb/search'
    params = {'query': query, 'format': 'tsv', 'fields': ','.join(fields), 'size': 500}
    response = requests.get(url, params=params)
    return pd.read_csv(StringIO(response.text), sep='\t')

# Example: get human kinases with specific fields
df = get_fields('organism_id:9606 AND keyword:kinase AND reviewed:true',
                ['accession', 'gene_names', 'protein_name', 'length', 'go_p'])
print(df.head())
```

**BioPython / SeqIO integration:**

```python
from Bio import SeqIO
from io import StringIO

fasta_text = fetch_uniprot('P04637', 'fasta')
record = SeqIO.read(StringIO(fasta_text), 'fasta')
print(record.id, len(record.seq))
```

## Python Implementation

For programmatic access, use the provided helper script `scripts/uniprot_client.py` which implements:

- `search_proteins(query, format)` - Search UniProt with any query
- `get_protein(accession, format)` - Retrieve single protein entry
- `map_ids(ids, from_db, to_db)` - Map between identifier types
- `batch_retrieve(accessions, format)` - Retrieve multiple entries
- `stream_results(query, format)` - Stream large result sets

**Alternative Python packages:**
- **Unipressed**: Modern, typed Python client for UniProt REST API
- **bioservices**: Comprehensive bioinformatics web services client

## Query Syntax Examples

**Boolean operators:**
```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

**Field-specific searches:**
```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

**Range queries:**
```
length:[100 TO 500]
mass:[50000 TO 100000]
```

**Wildcards:**
```
gene:BRCA*
protein_name:kinase*
```

See `/references/query_syntax.md` for comprehensive syntax documentation.

## Best Practices

1. **Use reviewed entries when possible**: Filter with `reviewed:true` for Swiss-Prot (manually curated) entries
2. **Specify format explicitly**: Choose the most appropriate format (FASTA for sequences, TSV for tabular data, JSON for programmatic parsing)
3. **Use field selection**: Only request fields you need to reduce bandwidth and processing time
4. **Handle pagination**: For large result sets, implement proper pagination or use the stream endpoint
5. **Cache results**: Store frequently accessed data locally to minimize API calls
6. **Rate limiting**: Be respectful of API resources; implement delays for large batch operations
7. **Check data quality**: TrEMBL entries are computational predictions; Swiss-Prot entries are manually reviewed

## Resources

### scripts/
`uniprot_client.py` - Python client with helper functions for common UniProt operations including search, retrieval, ID mapping, and streaming.

### references/
- `api_fields.md` - Complete list of available fields for customizing queries
- `id_mapping_databases.md` - Supported databases for ID mapping operations
- `query_syntax.md` - Comprehensive query syntax with advanced examples
- `api_examples.md` - Code examples in multiple languages (Python, curl, R)

## Additional Resources

- **API Documentation**: https://www.uniprot.org/help/api
- **Interactive API Explorer**: https://www.uniprot.org/api-documentation
- **REST Tutorial**: https://www.uniprot.org/help/uniprot_rest_tutorial
- **Query Syntax Help**: https://www.uniprot.org/help/query-fields
- **SPARQL Endpoint**: https://sparql.uniprot.org/ (for advanced graph queries)
