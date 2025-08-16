# mt/translator.py
import numpy as np
from .loader import assets

def translate(sentence: str) -> str:
    """
    Greedy decoding for seq2seq model without <start>/<end> tokens.
    Removes only <PAD>.
    """
    x = assets.encode_english(sentence)
    y_pred = assets.model.predict(x, verbose=0)        # shape: (1, max_fr, vocab_size)
    token_ids = np.argmax(y_pred[0], axis=-1)          # shape: (max_fr,)
    return assets.postprocess_tokens(token_ids)
