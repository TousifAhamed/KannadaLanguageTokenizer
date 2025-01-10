from tqdm import tqdm
from collections import Counter
from typing import Tuple, List
import json


class BytePairEncoding:
  def __init__(self, txt: str):

    #getting all characters in list in sorted order
    self.chars = sorted(list(set(txt)))

    #dictionary for strings to integers
    self.stoi = {ch: i for i, ch in enumerate(self.chars)}

    #dictionary for integers to strings
    self.itos = {i: ch for i, ch in enumerate(self.chars)}

    # inital form of text to integers in terms of list
    self.data = [self.stoi[c] for c in txt]

    # Statistics tracking
    self.stats = {
        "vocab_sizes": [len(self.chars)],
        "data_sizes": [len(self.data)],
        "compression_ratios": [1.0],
        "merge_counts": [],
        "tokens_created": [],
        "max_token_lengths": [1],
    }

    #length of characters of input txt
    self.max_token_length = 0
    self.orginal_txt_length = len(self.data)

  def get_stats(self):
    "counting pair of characters"
    counts = Counter()
    for pair in zip(self.data, self.data[1:]):
      pair = (int(pair[0]), int(pair[1]))
      counts[pair] += 1
    return counts

  def merge_pair_encoding(self, pair, idx):
    "replace tokens into newly defined token"
    newids = []
    i = 0
    while i < len(self.data):
      if i < len(self.data) - 1 and self.data[i] == pair[0] and self.data[i+1] == pair[1]:
        newids.append(idx)
        i += 2
      else:
        newids.append(self.data[i])
        i += 1
    return newids

  def add_new_encode_pair(self, pair: Tuple[int, int]) -> int:
      """Add a new token to vocabulary dictionary"""
      pair_str = self.itos[pair[0]] + self.itos[pair[1]]
      next_idx = len(self.itos)
      self.stoi[pair_str] = next_idx
      self.itos[next_idx] = pair_str

      # Update max token length
      self.max_token_length = max(self.max_token_length, len(pair_str))
      return next_idx

  def update_stats(self, merge_count: int, new_token: str):
    """Record statistics after each merge operation"""
    self.stats["vocab_sizes"].append(len(self.itos))
    self.stats["data_sizes"].append(len(self.data))
    self.stats["compression_ratios"].append(self.orginal_txt_length / len(self.data))
    self.stats["merge_counts"].append(merge_count)
    self.stats["tokens_created"].append(new_token)


  def merge_byte_pair(self) -> Tuple[int, str, int]:
      """
      Merge the top byte pair

      Returns:
          Tuple[int, str, int]: (new_token_id, new_token_str, merge_count) or None if no more pairs to merge
      """
      # Get pair frequencies
      stats = self.get_stats()
      if not stats:  # No more pairs to merge
          return None

      # Find most frequent pair
      (top_pair, count) = max(stats.items(), key=lambda x: x[1])

      # Add new token to vocabulary
      new_idx = self.add_new_encode_pair(top_pair)

      # Replace pairs in data
      self.data = self.merge_pair_encoding(top_pair, new_idx)

      # Update statistics
      self.update_stats(count, self.itos[new_idx])

      return new_idx, self.itos[new_idx], count

  def print_progress(self, iteration: int, new_token: str, merge_count: int):
    """
    Print training progress in text format

    Args:
        iteration: Current iteration number
        new_token: Newly created token
        merge_count: Number of merges for this token
    """
    print(f"\nIteration {iteration:,}")
    print(f"Current vocabulary size: {len(self.itos):,}")
    print(f"Current data size: {len(self.data):,}")
    print(f"Current compression ratio: {self.stats['compression_ratios'][-1]:.2f}")
    print("-" * 80)

  def encode_to_vocab_size(
        self,
        target_vocab_size: int,
        print_interval: int = 100,
    ) -> None:
        """
        Perform BPE encoding until reaching target vocabulary size

        Args:
            target_vocab_size: Maximum vocabulary size to reach
            print_interval: How often to print progress (None for no printing)
        """
        pbar = tqdm(
            total=target_vocab_size,
            desc=f"Encoding byte pairs",
            initial=len(self.chars),
            position=0,
            leave=True,
        )

        iteration = 0
        while len(self.itos) < target_vocab_size:
            # Train one iteration
            result = self.merge_byte_pair()
            if result is None:  # No more pairs to merge
                break

            new_idx, new_token, merge_count = result
            iteration += 1

            # Update progress bar
            pbar.update(1)

            # Print progress at intervals if requested
            if print_interval and iteration % print_interval == 0:
                self.print_progress(iteration, new_token, merge_count)

        pbar.close()

        # Final statistics
        print(f"\nTraining completed after {iteration:,} iterations")
        print(f"Final vocabulary size: {len(self.itos):,}")

  def encode(self, text: str) -> List[int]:
    """Convert text to token indices"""
    return [self.stoi[c] for c in text]

  def decode(self, token_ids: List[int]) -> str:
    """Convert token indices back to text"""
    return "".join(self.itos[idx] for idx in token_ids)

  def save_to_file(self, filepath: str) -> None:
      """
      Save encoder state to a JSON file.

      Args:
          filepath: Path where to save the encoder state
      """
      state = {
          "chars": self.chars,
          "stoi": self.stoi,  # Only save stoi, we can reconstruct itos
          "max_token_length": self.max_token_length,
          "stats": self.stats,
      }

      with open(filepath, "w", encoding="utf-8") as f:
          json.dump(state, f, ensure_ascii=False, indent=2)

      print(f"Encoder saved to {filepath}")