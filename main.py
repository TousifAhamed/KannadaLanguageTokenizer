from pathlib import Path
from tqdm import tqdm
from Preprocess import clean_kannada_text
from Byte_Pair_Encoding import BytePairEncoding

def load_kannada_text(directory: str, max_files: int = None) -> str:
    """
    Load and Preprocess Kannada text from files in directory
    
    Args:
        directory: Path to directory containing text files
        max_files: Maximum number of files to load (None for all files)
    """
    all_text = []
    
    # Convert to Path object for easier handling
    dir_path = Path(directory)
    
    # Get list of files and limit if specified
    files = list(dir_path.glob('*.txt'))
    if max_files:
        files = files[:max_files]
    
    # Process each file
    for file_path in tqdm(files, desc="Loading files"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                cleaned_text = clean_kannada_text(text)
                if cleaned_text:  # Only add non-empty texts
                    all_text.append(cleaned_text)
        except UnicodeDecodeError:
            print(f"Warning: Skipping file {file_path} due to encoding issues")
    
    # Join all texts with space
    combined_text = ' '.join(all_text)
    
    print(f"Loaded {len(all_text):,} files")
    print(f"Total text length: {len(combined_text):,} characters")
    
    return combined_text

def main():
    # Configuration
    data_dir = "train/train"
    vocab_size = 5000
    output_file = "kannada_tokenizer.json"
    
    # Load and clean text
    print("Loading and Preprocessing text...")
    text = load_kannada_text(data_dir, 1000)
    
    
    
    # Create and train encoder
    print("\nTraining BPE encoder...")
    encoder = BytePairEncoding(text)
    encoder.encode_to_vocab_size(vocab_size, print_interval=100)
    
    # Save the encoder
    print("\nSaving encoder...")
    encoder.save_to_file(output_file)

main()