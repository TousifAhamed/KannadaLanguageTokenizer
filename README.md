# Kannada Language BPE Tokenizer

A specialized Byte Pair Encoding (BPE) tokenizer implementation for the Kannada language, designed to improve natural language processing tasks for Kannada text.

This tokenizer can be utilized in various NLP tasks:
- Machine Translation systems for Kannada
- Text Classification
- Named Entity Recognition
- Language Model pre-training
- Text Generation
- Sentiment Analysis

The tokenizer is compatible with popular deep learning frameworks:
- PyTorch
- TensorFlow
- Hugging Face Transformers

## Overview

This project implements a BPE tokenizer specifically trained on Kannada language text data. The tokenizer is trained on a comprehensive dataset of Kannada Wikipedia articles, making it suitable for various NLP applications involving Kannada text.

## Dataset

The tokenizer is trained using the [Kannada Wikipedia Articles dataset](https://www.kaggle.com/datasets/disisbig/kannada-wikipedia-articles/data) from Kaggle, which provides a rich source of Kannada language text for training.

## Training Results

The tokenizer was successfully trained with the following specifications:

- Final vocabulary size: 5,000 tokens
- Training iterations: 4,772
- Final compression ratio: 3.68
- Training duration: ~22.5 hours

Training progress metrics:
```
At 4,600 iterations:
- Vocabulary size: 4,828
- Data size: 939,235
- Compression ratio: 3.66

At 4,700 iterations:
- Vocabulary size: 4,928
- Data size: 934,595
- Compression ratio: 3.68
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/KanLangTokenizer.git
cd KanLangTokenizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the training data from [Kaggle](https://www.kaggle.com/datasets/disisbig/kannada-wikipedia-articles/data) if you want to retrain the model.

## Usage

### As a Library

```python
from kan_lang_tokenizer import KannadaTokenizer

# Initialize the tokenizer
tokenizer = KannadaTokenizer()

# Tokenize Kannada text
text = "ಕನ್ನಡ ಭಾಷೆ ಒಂದು ದ್ರಾವಿಡ ಭಾಷೆ"
tokens = tokenizer.tokenize(text)

# Decode tokens back to text
decoded_text = tokenizer.decode(tokens)
```

### Training Custom Tokenizer

```python
from kan_lang_tokenizer import KannadaTokenizer

# Initialize with custom vocabulary size
tokenizer = KannadaTokenizer(vocab_size=5000)

# Train on your own data
tokenizer.train(data_path="path/to/your/kannada/texts")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Kannada Wikipedia Articles dataset from Kaggle

