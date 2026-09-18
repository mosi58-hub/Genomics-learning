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

                                                                                    4. Alignment Quality Assessment

                                                                                    The chromosome 21 BAM file was examined using SAMtools.

                                                                                    Metric| Result
                                                                                    Total alignment records| 21,545,691
                                                                                    Primary alignment records| 21,539,634
                                                                                    Mapped records| 1,221,496
                                                                                    Primary mapped records| 1,215,439
                                                                                    Mean primary mapped MAPQ| 28.50
                                                                                    Primary mapped reads with MAPQ ≥20| 51.45%
                                                                                    Primary mapped reads with MAPQ ≥30| 46.62%

                                                                                    Mapping percentages reflect the chromosome-specific BAM and should not be interpreted as whole-genome alignment rates.

                                                                                    5. Targeted Variant Validation

                                                                                    Twenty predefined chromosome 21 positions were selected for further investigation.

                                                                                    The analysis included:

                                                                                    - Site-specific sequencing depth.
                                                                                    - Reference and alternate allele support.
                                                                                    - Variant allele fraction (VAF).
                                                                                    - Available VCF quality information.
                                                                                    - Read-level evidence assessment.

                                                                                    The validation workflow used minimum base-quality and mapping-quality thresholds of 20 for depth and pileup analyses.

                                                                                    Variant allele fractions were calculated as:

                                                                                    VAF = ALT-supporting reads / (REF-supporting reads + ALT-supporting reads)

                                                                                    These measurements provide technical evidence but do not independently establish variant pathogenicity or clinical significance.

                                                                                    6. Quality Control Considerations

                                                                                    Variant-level assessment considers multiple complementary factors, including sequencing depth, allele balance, mapping quality, base quality, and read support.

                                                                                    Potential technical artifacts require additional investigation, particularly when evidence is inconsistent across different quality metrics.

                                                                                    Read-level validation should be distinguished from independent experimental confirmation.

                                                                                    7. Final Deliverables

                                                                                    Integrated Excel workbook

                                                                                    "chr21_analysis/results/portfolio/ERR297183_chr21_portfolio_integrated_final-1.xlsx"

                                                                                    Contains the integrated results of the selected-variant analysis.

                                                                                    HTML report

                                                                                    "chr21_analysis/results/reports/ERR297183_chr21_portfolio_report.html"

                                                                                    Provides a complementary report for reviewing and presenting the analysis.

                                                                                    8. Tools and Technical Skills

                                                                                    Category| Tools / Skills
                                                                                    Sequencing QC| FastQC, fastp
                                                                                    BAM processing| SAMtools
                                                                                    Variant processing| BCFtools
                                                                                    Data analysis| Python
                                                                                    Automation| Bash
                                                                                    Version control| Git and GitHub
                                                                                    Deliverables| Excel and HTML

                                                                                    9. Limitations

                                                                                    This analysis focuses on a predefined set of 20 variants on chromosome 21 rather than comprehensive genome-wide variant interpretation.

                                                                                    Technical validation is limited by sequencing quality, alignment characteristics, reference compatibility, and the available evidence.

                                                                                    The results are intended for educational and portfolio demonstration purposes and should not be used independently for clinical decision-making.

                                                                                    10. Project Outcome

                                                                                    This project demonstrates the ability to organize and execute a targeted NGS bioinformatics workflow, assess alignment and variant-level quality, integrate sequencing evidence, and communicate technical findings through structured deliverables.

                                                                                    ---

                                                                                    Portfolio project | NGS Bioinformatics | Variant Analysis | Python | Linux
