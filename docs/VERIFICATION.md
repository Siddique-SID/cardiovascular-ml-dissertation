# Verification record

## Sources and scope

- Historical values: dissertation Table 3.2 / Appendix A, cross-checked against the original working notebook (CA2, master comparison cell).
- Notebook: recovered final analysis notebook; code retained, outputs cleared, and a portfolio provenance note added.
- PDF: a portfolio copy of the latest recovered dissertation. The student identifier was removed; academic text and results were retained.
- Raw and cleaned datasets are not redistributed. The supplied preparation script reproduces the 70,000 → 68,627 row count.

## Primary held-out rerun

All seven final estimator configurations were fitted and evaluated on the 80/20 stratified split in this environment. This is a bounded verification of the primary holdout workflow; full CV, tuning, ablation, threshold analysis and every notebook cell were **not** rerun.

The recovered configurations do not exactly reproduce every published point estimate. The original environment was not locked, and the reason for each difference has not been established. Do not silently replace the reported results or claim bit-for-bit reproducibility.

| Model | Reported accuracy | Rerun accuracy | Reported ROC-AUC | Rerun ROC-AUC |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.7305 | 0.7304 | 0.7943 | 0.7943 |
| Decision Tree | 0.6417 | 0.6388 | 0.6418 | 0.6388 |
| Random Forest (Tuned) | 0.7389 | 0.7385 | 0.8062 | 0.8060 |
| AdaBoost | 0.7309 | 0.7283 | 0.7984 | 0.7967 |
| Linear SVM | 0.7277 | 0.7278 | 0.7943 | 0.7943 |
| KNN (Tuned) | 0.7347 | 0.7350 | 0.7970 | 0.7969 |
| Gaussian Naive Bayes | 0.7111 | 0.7110 | 0.7816 | 0.7816 |

Full rerun outputs, metric deltas and environment versions are in `results/`. The website and README intentionally show the historical dissertation table.

## Website checks

JavaScript syntax checked; local resource paths verified; report figures matched to CSV/JSON. Metric switching, model selectors, methodology details and motion control are checked in the rendered page. No live prediction API or patient-data input is included.
