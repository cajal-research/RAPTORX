# Replicating Benchmark Results: Roadmap and Checklist

## Step 1: Obtain and Prepare Datasets
- [x] Acquire datasets: NarrativeQA, QASPER, QuALITY
  - [x] NarrativeQA
  - [x] QASPER
  - [x] QuALITY

## Step 2: Understand Data Formats and Structure
### NarrativeQA (`narrative.csv`)
- **Format**: CSV
- **Columns**:
  - `id`: Unique identifier for each entry
  - `context`: Text context of the narrative
  - `question`: Question related to the narrative
  - `answer`: Answer to the question

### QASPER (`qasper.json`)
- **Format**: JSON
- **Structure**:
  - Each entry is identified by a unique paper ID
  - Fields include:
    - `title`: Title of the paper
    - `abstract`: Abstract of the paper
    - `full_text`: List of sections, each containing:
      - `section_name`: Name of the section
      - `paragraphs`: List of paragraphs in the section
    - `qas`: List of question-answer sets, each containing:
      - `question`: The question text
      - `answers`: List of answers, each with:
        - `answer`: The answer text
        - `evidence`: Text evidence supporting the answer

### QuALITY (`quality.json`)
- **Format**: JSON
- **Structure**:
  - List of articles, each with fields:
    - `article_id`: Unique identifier for the article
    - `set_unique_id`: Unique identifier for the set
    - `batch_num`: Batch number
    - `writer_id`: Writer's identifier
    - `source`: Source of the article
    - `title`: Title of the article
    - `year`: Year of publication
    - `author`: Author of the article
    - `topic`: Topics covered in the article
    - `article`: Full text of the article


## Step 3: Standardize Data Formats
- [ ] Define a common schema for all datasets:
  - Common Columns: `id`, `context`, `question`, `answer`
- [ ] Write scripts to convert datasets to the common schema:
  - [ ] **NarrativeQA conversion script**:
    - Read CSV
    - Map `id`, `context`, `question`, and `answer` to the common schema
  - [ ] **QASPER conversion script**:
    - Read JSON
    - Extract `title`, `abstract`, `full_text`, and `qas`
    - Combine `title`, `abstract`, and `full_text` into `context`
    - Map `question` and `answers` to the common schema
  - [ ] **QuALITY conversion script**:
    - Read JSON
    - Extract `article_id`, `title`, and `article`
    - Use `article_id` as `id`
    - Combine `title` and `article` into `context`
    - Generate synthetic questions and answers based on the text (if necessary)

## Step 4: Preprocessing
- [ ] Clean and preprocess the text data:
  - [ ] Remove special characters and HTML tags
  - [ ] Tokenization
  - [ ] Lowercasing
  - [ ] Normalize whitespace

### 4.1 NarrativeQA Preprocessing
- [ ] Tokenize `context` and `question`
- [ ] Convert `context`, `question`, and `answer` to lowercase

### 4.2 QASPER Preprocessing
- [ ] Concatenate `title`, `abstract`, and `full_text` into `context`
- [ ] Tokenize `context` and `question`
- [ ] Convert `context`, `question`, and `answer` to lowercase

### 4.3 QuALITY Preprocessing
- [ ] Concatenate `title` and `article` into `context`
- [ ] Tokenize `context` and synthetic questions (if generated)
- [ ] Convert `context`, `question`, and `answer` to lowercase

## Step 5: Data Augmentation (if needed)
- [ ] Generate additional training data through augmentation techniques
  - [ ] Paraphrasing
  - [ ] Synonym replacement
  - [ ] Back-translation

## Step 6: Split Data into Training, Validation, and Test Sets
- [ ] Define split ratios (e.g., 70% training, 15% validation, 15% test)
- [ ] Implement data splitting logic
  - [ ] NarrativeQA split
  - [ ] QASPER split
  - [ ] QuALITY split

## Step 7: Feature Engineering
- [ ] Extract relevant features for model training
  - [ ] Token counts
  - [ ] Named entities
  - [ ] Part-of-speech tags

## Step 8: Model Training
- [ ] Select and configure model architecture
  - [ ] UnifiedQA
  - [ ] GPT-3 / GPT-4
- [ ] Train models on each dataset
  - [ ] NarrativeQA model training
  - [ ] QASPER model training
  - [ ] QuALITY model training

## Step 9: Evaluation
- [ ] Evaluate model performance on test sets
  - [ ] NarrativeQA evaluation metrics: BLEU, ROUGE, METEOR
  - [ ] QASPER evaluation metrics: F1
  - [ ] QuALITY evaluation metrics: Accuracy
- [ ] Compare results with benchmark

## Step 10: Fine-Tuning and Optimization
- [ ] Perform hyperparameter tuning
- [ ] Implement model optimization techniques
  - [ ] Learning rate adjustment
  - [ ] Batch size adjustment
  - [ ] Regularization methods

## Step 11: Documenting and Reporting Results
- [ ] Document all steps, decisions, and observations
- [ ] Create visualizations of performance metrics
  - [ ] Training and validation loss curves
  - [ ] Performance comparison charts
- [ ] Compile final report and share findings

## Additional Steps for Reproducibility
- [ ] Ensure all code and scripts are version-controlled
- [ ] Create a README file with setup instructions
- [ ] Package datasets and scripts for easy distribution
- [ ] Publish code and documentation on a public repository (e.g., GitHub)

---
