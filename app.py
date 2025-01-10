import gradio as gr
import json

# Load the tokenizer vocabulary
def load_tokenizer():
    with open('kannada_tokenizer.json', 'r', encoding='utf-8') as f:
        tokenizer = json.load(f)
        # Reconstruct itos from stoi
        tokenizer['itos'] = {str(v): k for k, v in tokenizer['stoi'].items()}
    return tokenizer

def encode_text(text: str) -> str:
    """Convert text to token indices"""
    tokenizer = load_tokenizer()
    try:
        # Convert text to tokens using the stoi (string to integer) mapping
        tokens = []
        current_pos = 0
        while current_pos < len(text):
            # Try to match the longest possible token
            found = False
            for token_length in range(min(tokenizer['max_token_length'], len(text) - current_pos), 0, -1):
                substr = text[current_pos:current_pos + token_length]
                if substr in tokenizer['stoi']:
                    tokens.append(tokenizer['stoi'][substr])
                    current_pos += token_length
                    found = True
                    break
            if not found:
                return f"Error: Unable to encode character at position {current_pos}"
        
        return str(tokens)
    except Exception as e:
        return f"Error encoding text: {str(e)}"

def decode_tokens(token_string: str) -> str:
    """Convert token indices back to text"""
    tokenizer = load_tokenizer()
    try:
        # Clean the input string and convert to list of integers
        token_string = token_string.strip('[]').replace(' ', '')
        if not token_string:
            return "Error: Empty input"
            
        tokens = [int(t) for t in token_string.split(',') if t]
        
        # Convert tokens back to text using the itos (integer to string) mapping
        result = ""
        for token in tokens:
            token_str = str(token)
            if token_str not in tokenizer['itos']:
                return f"Error: Invalid token {token}"
            result += tokenizer['itos'][token_str]
        
        return result
    except ValueError:
        return "Error: Invalid input format. Please enter numbers separated by commas"
    except Exception as e:
        return f"Error decoding tokens: {str(e)}"

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Kannada Text Tokenizer") as interface:
        gr.Markdown("# Kannada Text Tokenizer")
        
        with gr.Tab("Encode"):
            with gr.Row():
                input_text = gr.Textbox(label="Enter Kannada Text", lines=5)
                encode_button = gr.Button("Encode")
                encoded_output = gr.Textbox(label="Encoded Tokens", lines=5)
            encode_button.click(fn=encode_text, inputs=input_text, outputs=encoded_output)
        
        with gr.Tab("Decode"):
            with gr.Row():
                input_tokens = gr.Textbox(label="Enter Token List (e.g., [120, 135, 171])", lines=5)
                decode_button = gr.Button("Decode")
                decoded_output = gr.Textbox(label="Decoded Text", lines=5)
            decode_button.click(fn=decode_tokens, inputs=input_tokens, outputs=decoded_output)
        
        gr.Markdown("""
        ### Instructions:
        - **Encode**: Enter Kannada text in the input box and click 'Encode' to get token indices
        - **Decode**: Enter a list of token indices and click 'Decode' to get back the original text
        - Token indices must be in the format: [123, 456, 789]
        """)
    
    return interface

if __name__ == "__main__": 
    interface = create_interface()
    interface.launch(share=False)
