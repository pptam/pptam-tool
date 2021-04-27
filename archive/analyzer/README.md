# Analyzer

This is a set of R scripts to reproduce the analysis of the paper "Alberto Avritzer, Vincenzo Ferme, Andrea Janes, Barbara Russo, André van Hoorn, Henning Schulz, Daniel Menasch, Vilc Rufino, "Scalability Assessment of Microservice Architectural Configurations:A Domain-based Approach Leveraging Operational Profiles and Load Tests"

Execute the script start.R to run the analysis.

The tool performe the following steps:

- Compute the operational profile of a system either from frequency counts or from accesses
- Compute the baseline threshold
- Compute the domain metric for each configuration and each load
- Rank configurations by the total domain metric summed over loads
- Plot polygons
- Compute the sensitivity analysis on the threshold variation
- Plot the the sensitivity analysis over threshold variation and compute the gap to operational profile
