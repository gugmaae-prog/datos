# Datos Master Lead Database

Working implementation for the Master Real Estate Lead Database system.

Start here:

```bash
python scripts/build_master_db.py --input data/raw --db database/master_leads.db --reports-dir reports
```

See `DATABASE_README.md` for the full schema, phone rules, taxonomy, report guide, and SQL examples.

Generated SQLite/database outputs contain personally identifiable lead data and should be generated locally from raw files rather than committed to the public repository.
