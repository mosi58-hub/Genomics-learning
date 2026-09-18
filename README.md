Chromosome 21 Variant Analysis and Validation

A Reproducible NGS Bioinformatics Portfolio Project

Project type: Whole-genome sequencing data analysis (chromosome 21 subset)
Dataset: ERR297183
Platform: Linux / GitHub Codespaces
Tools: FastQC, fastp, SAMtools, BCFtools, Python

---

1. Project Overview

This project demonstrates a practical next-generation sequencing (NGS) bioinformatics workflow focused on chromosome 21.

The workflow covers sequencing quality control, read alignment assessment, variant processing, and targeted validation of 20 selected variants.

The project emphasizes reproducibility, transparent quality assessment, and integration of multiple sources of variant-level evidence.

Project scope: A technical bioinformatics demonstration using a selected chromosome and a predefined set of variants. It is not a clinical diagnostic analysis.

2. Project Objectives

- Assess sequencing data quality.
- Evaluate alignment quality and mapping statistics.
- Process and inspect variant call files.
- Examine sequencing depth at 20 selected genomic positions.
- Calculate variant allele fractions using available allele-support evidence.
- Identify variants requiring further technical investigation.
- Produce an integrated Excel workbook and an HTML report.

3. Bioinformatics Workflow

Sequencing Data
      |
            v
            Quality Control
            FastQC / fastp
                  |
                        v
                        Alignment Assessment
                        SAMtools
                              |
                                    v
                                    Variant Processing
                                    BCFtools
                                          |
                                                v
                                                Selection of 20 Variants
                                                      |
                                                            v
                                                            Depth and Allele Support
                                                            SAMtools depth / mpileup
                                                                  |
                                                                        v
                                                                        Evidence Integration
                                                                        Python
                                                                              |
                                                                                    v
                                                                                    Final Excel Workbook
                                                                                    and HTML Report

## 3. Bioinformatics Workflow

```text
Sequencing Data (ERR297183)
          |
          v
Quality Control (FastQC / fastp)
          |
          v
Alignment Assessment (SAMtools)
          |
          v
Variant Processing (BCFtools)
          |
          v
Selection of 20 Variants
          |
          v
Depth and Allele Support Validation
          |
          v
Evidence Integration (Python)
          |
          v
Final Excel Workbook and HTML Report
```

4. Repository Structure

The project is organized into the following directories:

Directory| Description
"scripts/"| Python scripts for variant annotation and Excel report generation
"results/qc/"| Sequencing quality control reports
"results/variants/"| Variant call files (VCF)
"results/validation/"| Depth, pileup, and variant-level evidence
"results/reports/"| Analysis reports
"results/portfolio/"| Portfolio deliverables

5. Variant Validation

Twenty selected variants were investigated using available sequencing evidence.

The validation workflow includes:

- Examination of sequencing depth.
- Inspection of read-level allele support.
- Calculation of variant allele fraction (VAF), where sufficient evidence is available.
- Integration of evidence into structured tables.
- Identification of variants requiring further investigation.

These analyses provide technical evidence and do not constitute independent clinical validation.

6. Project Deliverables

The repository contains:

- Sequencing quality control reports.
- Processed variant call files.
- Variant validation tables.
- Python scripts for annotation and report generation.
- Analysis reports and portfolio materials.

7. Limitations

This project is a technical bioinformatics demonstration using publicly available sequencing data.

The analysis focuses on chromosome 21 and a predefined set of 20 variants.

The findings should not be interpreted as clinical diagnoses. Additional validation would be required before any clinical application.

8. Author

Bioinformatics Portfolio Project

Focus: Next-Generation Sequencing, Variant Analysis, Python, and Linux.
