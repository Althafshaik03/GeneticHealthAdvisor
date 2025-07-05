from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class IndicTranslator:
    def __init__(self, model_name="ai4bharat/indictrans2-en-indic-dist-200M"):
        # Load tokenizer and model from Hugging Face
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Language codes (ISO 639 + script tag)
        self.lang_map = {
            "hi": "hin_Deva",  # Hindi
            "kn": "kan_Knda",  # Kannada
            "en": "eng_Latn"   # English (for bypass)
        }

    def translate(self, text: str, src_lang="en", tgt_lang="hi") -> str:
        if tgt_lang == "en" or not text.strip():
            return text

        # Convert text into IndicTrans2 input format
        tgt_lang_code = self.lang_map.get(tgt_lang, "hin_Deva")
        formatted_text = f">>{tgt_lang_code}<< {text}"

        # Tokenize input
        inputs = self.tokenizer([formatted_text], return_tensors="pt", padding=True, truncation=True).to(self.device)

        # Generate translation
        with torch.no_grad():
            generated_tokens = self.model.generate(**inputs, max_length=512)

        # Decode result
        translation = self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        return translation
