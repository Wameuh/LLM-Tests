# LLM Tests

This repository contains Python scripts that interact with different language models (LLMs) for analyzing and annotating text data. The primary focus is on using the Gemini and Mistral models to process reviews and provide sentiment analysis.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Files Overview](#files-overview)
- [Environment Variables](#environment-variables)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Wameuh/LLM-Tests.git
   cd LLM-Tests
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables for the API keys (see [Environment Variables](#environment-variables)).

## Usage

1. Download the dataset from Kaggle: [Sentiment Analysis Python YouTube Tutorial](https://www.kaggle.com/code/robikscube/sentiment-analysis-python-youtube-tutorial?select=Reviews.csv).

2. Save the `Reviews.csv` file in the `assets/` folder of your project.

3. Run the main script:

   ```bash
   python AmazonReview.py
   ```

4. The annotated reviews will be saved in `assets/Reviews_annotated.csv`.

## Files Overview

- `AmazonReview.py`: Main script that loads reviews, processes them in batches, and writes the annotated results to a CSV file.
- `LLM_Gemini.py`: Contains functions to interact with the Gemini language model.
- `LLM_Mistral.py`: Contains functions to interact with the Mistral language model.
- `assets/Reviews.csv`: Input file containing Amazon reviews (downloaded from Kaggle).
- `assets/Reviews_annotated.csv`: Output file where annotated reviews will be saved.

## Environment Variables

To use the application, you need to set the following environment variables:

- `GEMINI_API_KEY`: Your API key for the Gemini language model.
- `MISTRALAI_API_KEY`: Your API key for the Mistral language model.

### Setting Environment Variables on Windows

1. Open the Start menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. In the System Properties window, click on "Environment Variables".
4. Under "User variables", click "New" and add the variable name and value.
5. Click OK to save.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
