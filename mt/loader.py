# mt/loader.py
import json
import pickle
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "models" / "artifacts"
MODELS = ROOT / "models"

class MTAssets:
    def __init__(self):
        self.model = None
        self.eng_tok = None
        self.fra_tok = None
        self.config = None
        self.index2word_fr = {}
        self.pad_token = "<PAD>"  # only PAD to remove

    def load_all(self):
        # 1) Load config.json
        with open(ARTIFACTS / "config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)  # {"max_en": X, "max_fr": Y}

        # 2) Load tokenizers
        with open(ARTIFACTS / "eng_tokenizer.pkl", "rb") as f:
            self.eng_tok = pickle.load(f)
        with open(ARTIFACTS / "fra_tokenizer.pkl", "rb") as f:
            self.fra_tok = pickle.load(f)

        # 3) Reverse mapping for FR tokens
        self.index2word_fr = {idx: w for w, idx in self.fra_tok.word_index.items()}
        self.index2word_fr[0] = self.pad_token  # Ensure index 0 is PAD

        # 4) Load model
        self.model = tf.keras.models.load_model(
            MODELS / "eng_fr_seq2seq.keras",
            compile=False
        )

        return self

    def encode_english(self, sentence: str):
        sent = (sentence or "").lower().strip()
        seq = self.eng_tok.texts_to_sequences([sent])
        seq = pad_sequences(
            seq,
            maxlen=self.config["max_en"],
            padding="post",
            truncating="post"
        )
        return seq

    def postprocess_tokens(self, token_ids):
        words = []
        for idx in token_ids:
            w = self.index2word_fr.get(int(idx), "")
            if not w or w == self.pad_token:
                continue
            words.append(w)
        return " ".join(words)

assets = MTAssets().load_all()
