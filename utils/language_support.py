from googletrans import Translator

translator = Translator()

def translate(text, lang="en"):
    if lang == "en":
        return text
    try:
        translated = translator.translate(text, dest=lang)
        return translated.text
    except Exception:
        return text + " [Translation Failed]"
