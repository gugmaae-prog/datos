# datos
database
 need you to build a comprehensive Master Real Estate Lead Database system for the datos repository. Here are the requirements:

## PROJECT OVERVIEW
Create a master database that consolidates all lead data with intelligent categorization, normalization, and enrichment.

## CORE REQUIREMENTS

### 1. PHONE NUMBER NORMALIZATION
Create strict rules for standardizing phone numbers:
- Remove all non-numeric characters (spaces, dashes, parentheses)
- Standardize UAE numbers to format: 971XXXXXXXXX (12 digits)
- Standardize China numbers to format: 86XXXXXXXXXXX
- Flag duplicates and invalid numbers
- Create validation rules (min/max length, country code validation)
- Remove test numbers (like 971050000000, sequential patterns)
- Create a phone_normalized field and phone_country_code field

### 2. DEVELOPER GLOSSARY & TAXONOMY
Build a comprehensive developer categorization system:

**Tier 1 - Luxury Developers:**
- Emaar Properties
- Aldar Properties  
- Nakheel
- Dubai Properties
- Meraas

**Tier 2 - Big Developers:**
- Damac Properties
- Azizi Developments
- Sobha Realty
- Ellington Properties
- Binghatti Developers

**Tier 3 - Mid-Size Developers:**
- Danube Properties
- Reportage Properties
- Mag Lifestyle Development
- Tiger Properties
- Gemini Property Developers

**Tier 4 - Small/Boutique Developers:**
- RAK Properties
- ETA Star
- Fakhruddin Properties
- Union Properties
- Others

Create a `developers.json` file with:
- Developer name
- Tier (luxury/big/mid/small)
- Typical price range
- Target market (investor/end-user/both)
- Specialization (villas/apartments/commercial)

### 3. PROJECT TAXONOMY
Categorize all projects by:

**By Target Audience:**
- Investor Projects: High ROI, off-plan, payment plans, rental yield focus
- End-User Projects: Ready/near-ready, lifestyle amenities, owner-occupied
- Mixed: Both investor and end-user appeal

**By Property Type:**
- Apartments/Flats
- Villas/Townhouses
- Penthouses
- Commercial
- Land/Plots

**By Price Category:**
- Entry Level: < 500K AED
- Mid Range: 500K - 1.5M AED
- Premium: 1.5M - 5M AED
- Luxury: > 5M AED

Create a `projects.json` file mapping project names to categories.

### 4. LEAD ENRICHMENT & CATEGORIZATION
Analyze each lead and add:
- Lead quality score (based on engagement: replied > read > delivered > sent)
- Interest level (based on reply type: "want to know more" vs "what are prices")
- Response time (fast responder vs slow)
- Project interest (extract from filename/source)
- Lead source (which campaign/project)
- Lead temperature: Hot (replied within 1 hour), Warm (replied same day), Cold (no reply)

### 5. MASTER DATABASE SCHEMA
Create a SQLite database `master_leads.db` with these tables:

**Table: leads**
- id (primary key)
- name
- phone_original
- phone_normalized
- phone_country_code
- email (if available)
- source_file
- campaign_name
- project_name
- developer_name
- developer_tier
- created_at
- updated_at

**Table: engagements**
- id (primary key)
- lead_id (foreign key)
- sent_at
- delivered_at
- read_at
- replied_at
- reply_type
- reply_text
- response_time_minutes
- lead_temperature

**Table: projects**
- id (primary key)
- project_name
- developer_id
- target_audience (investor/end_user/mixed)
- property_type
- price_category
- location
- launch_date

**Table: developers**
- id (primary key)
- developer_name
- tier (luxury/big/mid/small)
- specialization

### 6. DATA PROCESSING SCRIPTS

Create these Python scripts:

**`scripts/normalize_phones.py`**
- Read all CSV files
- Apply phone normalization rules
- Identify and flag duplicates
- Output cleaned data

**`scripts/build_master_db.py`**
- Consolidate all CSV/Excel files
- Apply normalization and enrichment
- Populate SQLite database
- Generate deduplication report

**`scripts/categorize_leads.py`**
- Extract project names from filenames
- Match to developer glossary
- Calculate lead scores
- Assign temperature ratings

**`scripts/generate_reports.py`**
- Lead statistics by developer
- Lead quality distribution
- Top performing projects
- Phone number quality report
- Duplicate analysis

### 7. CONFIGURATION FILES

**`config/developers.json`** - Complete developer glossary
**`config/projects.json`** - Project taxonomy
**`config/phone_rules.json`** - Phone normalization rules
**`config/interests.json`** - Interest categorization

### 8. DOCUMENTATION

Create comprehensive `DATABASE_README.md` with:
- Database schema documentation
- How to use each script
- Phone normalization rules explained
- Developer tier definitions
- Project categorization logic
- Example queries for common use cases

### 9. DELIVERABLES

1. SQLite database: `master_leads.db`
2. All processing scripts in `scripts/`
3. All config files in `config/`
4. Comprehensive documentation
5. Data quality report showing:
   - Total leads
   - Unique phone numbers
   - Leads by developer tier
   - Leads by temperature
   - Duplicate phone numbers
   - Invalid phone numbers

## EXECUTION STEPS

1. Analyze all existing CSV/Excel files to understand data structure
2. Create developer glossary by extracting developer names from filenames
3. Create phone normalization rules
4. Build database schema
5. Write all processing scripts
6. Process all data and populate database
7. Generate quality reports
8. Create documentation
