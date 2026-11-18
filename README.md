# PAP Partners

Private directory of PAP's partners: ODMs and suppliers, logistics, and the service network. English and Chinese, switched in the header.

- Update supplier figures: `python3 tools/build_odm.py AAP_Critical_Report_YYYYMMDDhhmmss.csv`, then commit `data/odm.json`.
- Add notes, contacts or new logistics / service partners in `data/partners.json` (both `en` and `zh`).
- Add a company description in `data/profiles.json` (both languages, with its source).
