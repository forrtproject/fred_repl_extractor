# FReD Replication Extractor

## Overview
The FReD Replication Extractor is a tool designed to support the Federal Reserve Database (FReD) in processing and analyzing replication studies in economics. This semi-automated tool helps keep pace with the expanding replication literature by extracting key metadata from published replication studies.

## Purpose
The tool serves two primary objectives:
1. **Original Study Identification**: Identify which original study a replication paper targets
2. **Replication Outcome Analysis**: Determine the reported replication outcome (success/mixed/failure)

## Features
- Combines text matching and LLM-based inference techniques
- Stores transparent justifications for conclusions
- Facilitates simple and auditable validation of outputs

## Architecture Overview
The system consists of three main components:
1. **Text Preprocessor**: Handles document parsing and text normalization
2. **Inference Engine**: 
   - Uses LLM for context understanding
   - Applies text matching algorithms
   - Generates confidence scores
3. **Output Generator**: Creates structured output with justifications

## Installation
1. Clone the repository:
```bash
git clone https://github.com/ebel-frank/fred_repl_extractor.git
cd fred_repl_extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Basic usage:
```bash
python main.py
```

### Example Output
```txt
DOI_r: 10.1177/0956797617734315
Title_r: Does Smile Intensity in Photographs Really Predict Longevity? A Replication and Extension of Abel and Kruger (2010)
Reference_r: Dufner Michael, Brümmer Martin, Chung Joanne M. et al. (2017). Does Smile Intensity in Photographs Really Predict Longevity? A Replication and Extension of Abel and Kruger (2010). Psychological Science, 29(1), 147-153.

DOI_o: 10.1177/0956797610363775
Title_o: Smile Intensity in Photographs Predicts Longevity
Reference_o: Abel Ernest L., Kruger Michael L. (2010). Smile Intensity in Photographs Predicts Longevity. Psychological Science, 21(4), 542-544.

Abstract: <jats:p> Abel and Kruger (2010) found that the smile intensity of professional baseball players who were active in 1952, as coded from photographs, predicted these players’ longevity. In the current investigation, we sought to replicate this result and to extend the initial analyses. We analyzed (a) a sample that was almost identical to the one from Abel and Kruger’s study using the same database and inclusion criteria ( N = 224), (b) a considerably larger nonoverlapping sample consisting of other players from the same cohort ( N = 527), and (c) all players in the database ( N = 13,530 valid cases). Like Abel and Kruger, we relied on categorical smile codings as indicators of positive affectivity, yet we supplemented these codings with subjective ratings of joy intensity and automatic codings of positive affectivity made by computer programs. In both samples and for all three indicators, we found that positive affectivity did not predict mortality once birth year was controlled as a covariate. </jats:p>  

Confidence: high

Outcome: failed

Proof: In both samples and for all three indicators, we found that positive affectivity did not predict mortality once birth year was controlled as a covariate.

Similarity: 100%
```

## API Key Configuration
1. Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_api_key_here
```

2. Or set environment variables:
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your_api_key_here"

# Linux/Mac
export GOOGLE_API_KEY="your_api_key_here"
```

## Confidence Scoring
The system employs a multi-factor confidence scoring mechanism:

- **Text Matching Score** (0-100): Based on abstract and proof similarity
- **Context Score** (high, medium, low): LLM evaluation of contextual references

