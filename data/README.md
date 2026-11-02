# Dataset access

Obtain **Cardiovascular Disease dataset** by Svetlana Ulianova from the source:
https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset

The dissertation records its licence as unknown. Source and cleaned datasets are
not redistributed in this portfolio. Review the source's current terms before use.
No patient records are embedded in the website.

Once you have `cardio_train.csv` (semicolon separated), from the project root run:

```bash
python scripts/prepare_data.py --input /path/to/cardio_train.csv
```

The script validates the expected counts and writes the raw and cleaned copies
into this ignored `data/` folder. It removes 1,373 rows from 70,000, leaving 68,627.
