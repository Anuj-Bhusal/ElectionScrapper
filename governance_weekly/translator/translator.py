import logging
from config import Config

logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        self.backend = Config.TRANSLATION_BACKEND
        self.client = None
        self._setup_backend()

    def _setup_backend(self):
        if self.backend == "google":
            try:
                # Assuming credentials are set via env var GOOGLE_APPLICATION_CREDENTIALS
                from google.cloud import translate_v2 as translate
                self.client = translate.Client()
            except Exception as e:
                logger.error(f"Failed to init Google Translate: {e}")
                self.backend = "googletrans" # Fallback to free googletrans
        
        if self.backend == "googletrans":
            try:
                from googletrans import Translator as GoogleTranslator
                self.googletrans = GoogleTranslator()
                logger.info("Googletrans (free) backend initialized")
            except Exception as e:
                logger.error(f"Failed to init Googletrans: {e}")
                self.backend = "gemini"
        
        if self.backend == "gemini":
            try:
                import google.generativeai as genai
                api_key = Config.GEMINI_API_KEY if hasattr(Config, 'GEMINI_API_KEY') else None
                if api_key:
                    genai.configure(api_key=api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                    logger.info("Gemini translation backend initialized")
                else:
                    logger.error("GEMINI_API_KEY not found in config")
                    self.backend = "marian"
            except Exception as e:
                logger.error(f"Failed to init Gemini: {e}")
                self.backend = "marian"
                
        if self.backend == "marian":
            # Lazy load transformers
            try:
                from transformers import MarianMTModel, MarianTokenizer
                model_name = "Helsinki-NLP/opus-mt-ne-en"
                self.tokenizer = MarianTokenizer.from_pretrained(model_name)
                self.model = MarianMTModel.from_pretrained(model_name)
            except Exception as e:
                logger.error(f"Failed to load MarianMT: {e}")
                self.backend = "none"

    def _contains_nepali(self, text):
        for char in text:
            if '\u0900' <= char <= '\u097F':
                return True
        return False

    def translate(self, text, source_lang="ne", target_lang="en"):
        if not text:
            return ""
        
        if source_lang == target_lang:
            return text

        translated_text = text # Default to original
        
        try:
            if self.backend == "google":
                result = self.client.translate(text, target_language=target_lang)
                translated_text = result["translatedText"]
            
            elif self.backend == "googletrans":
                # Googletrans can be flaky, try a few times
                for attempt in range(3):
                    try:
                        result = self.googletrans.translate(text, src=source_lang, dest=target_lang)
                        translated_text = result.text
                        if translated_text and not self._contains_nepali(translated_text):
                            break # Success
                    except Exception as e:
                        logger.warning(f"Googletrans attempt {attempt+1} failed: {e}")
                        # Re-init might help
                        from googletrans import Translator as GoogleTranslator
                        self.googletrans = GoogleTranslator()
            
            elif self.backend == "gemini":
                prompt = f"Translate the following Nepali text to English. Only provide the translation, nothing else:\n\n{text}"
                response = self.gemini_model.generate_content(prompt)
                translated_text = response.text.strip()
            
            elif self.backend == "marian":
                # Chunking might be needed for long text
                inputs = self.tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
                generated = self.model.generate(**inputs)
                translated_text = self.tokenizer.decode(generated[0], skip_special_tokens=True)
                
        except Exception as e:
            logger.error(f"Translation error ({self.backend}): {e}")
            return text # Return original on hard error

        # Post-processing: If translation still contains Nepali, it failed or partial fail
        if self._contains_nepali(translated_text):
            logger.warning(f"Translation result still contains Nepali characters. Backend: {self.backend}")
            # Fallback: Strip Nepali characters to avoid blocks in PDF
            cleaned_text = "".join([c for c in translated_text if not ('\u0900' <= c <= '\u097F')])
            # If cleaning leaves very little, it was mostly Nepali
            if len(cleaned_text.strip()) < len(translated_text) * 0.5:
                 return "[Translation Failed]"
            return cleaned_text

        return translated_text
