import logging
import time
from config import Config

logger = logging.getLogger(__name__)

class Translator:
    """
    Multi-backend translator with robust retry mechanism
    Backends: Google Cloud > Googletrans (free) > Gemini > MarianMT
    """
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAYS = [2, 4, 8]  # Exponential backoff: 2s, 4s, 8s
    REQUEST_TIMEOUT = 10  # seconds
    
    def __init__(self):
        self.backend = Config.TRANSLATION_BACKEND
        self.client = None
        self._setup_backend()
        
        # Validate at least one backend is working
        if self.backend == "none":
            logger.critical("=" * 80)
            logger.critical("NO TRANSLATION BACKEND AVAILABLE!")
            logger.critical("Translation will fail. Please configure one of these:")
            logger.critical("1. GEMINI_API_KEY (recommended - free from https://makersuite.google.com)")
            logger.critical("2. GOOGLE_APPLICATION_CREDENTIALS (Google Cloud Translate)")
            logger.critical("3. Install googletrans: pip install googletrans==4.0.0rc1")
            logger.critical("4. Install MarianMT: pip install transformers torch")
            logger.critical("=" * 80)
        else:
            logger.info(f"Translation backend active: {self.backend}")

    def _setup_backend(self):
        if self.backend == "google":
            try:
                from google.cloud import translate_v2 as translate
                self.client = translate.Client()
            except Exception as e:
                logger.error(f"Failed to init Google Translate: {e}")
                self.backend = "googletrans"
        
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
                if api_key and api_key.strip():  # Check for non-empty key
                    genai.configure(api_key=api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                    logger.info("Gemini translation backend initialized")
                else:
                    logger.error("GEMINI_API_KEY not found or empty in .env file")
                    logger.error("Get a free key from: https://makersuite.google.com/app/apikey")
                    self.backend = "marian"
            except Exception as e:
                logger.error(f"Failed to init Gemini: {e}")
                self.backend = "marian"
                
        if self.backend == "marian":
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

    def _translate_with_googletrans(self, text, source_lang, target_lang):
        """
        Googletrans with robust retry mechanism
        """
        from googletrans import Translator as GoogleTranslator
        
        for attempt in range(self.MAX_RETRIES):
            try:
                # Exponential backoff delay (except first attempt)
                if attempt > 0:
                    delay = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                    logger.info(f"Retry {attempt+1}/{self.MAX_RETRIES} after {delay}s delay...")
                    time.sleep(delay)
                    # Re-initialize translator for fresh connection
                    self.googletrans = GoogleTranslator()
                
                # Attempt translation
                result = self.googletrans.translate(text, src=source_lang, dest=target_lang)
                
                if result and result.text:
                    translated = result.text
                    # Check if translation succeeded (no Nepali in output)
                    if not self._contains_nepali(translated):
                        return translated
                    else:
                        logger.warning(f"Attempt {attempt+1}: Translation still contains Nepali")
                        
            except Exception as e:
                logger.warning(f"Googletrans attempt {attempt+1}/{self.MAX_RETRIES} failed: {type(e).__name__}: {e}")
                # Small delay before re-init
                time.sleep(1)
                try:
                    self.googletrans = GoogleTranslator()
                except:
                    pass
        
        # All retries failed
        logger.error(f"All {self.MAX_RETRIES} googletrans attempts failed")
        return None

    def translate(self, text, source_lang="ne", target_lang="en"):
        """
        Translate text with robust retry mechanism
        Falls back to next backend if current fails
        """
        if not text:
            return ""
        
        if source_lang == target_lang:
            return text

        translated_text = None
        
        try:
            if self.backend == "google":
                result = self.client.translate(text, target_language=target_lang)
                translated_text = result["translatedText"]
            
            elif self.backend == "googletrans":
                translated_text = self._translate_with_googletrans(text, source_lang, target_lang)
                
                # If googletrans completely failed, try gemini fallback
                if translated_text is None:
                    logger.info("Trying Gemini fallback...")
                    try:
                        import google.generativeai as genai
                        api_key = Config.GEMINI_API_KEY if hasattr(Config, 'GEMINI_API_KEY') else None
                        if api_key:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel('gemini-2.5-flash')
                            prompt = f"Translate the following Nepali text to English. Only provide the translation, nothing else:\n\n{text}"
                            response = model.generate_content(prompt)
                            translated_text = response.text.strip()
                            logger.info("Gemini fallback succeeded")
                    except Exception as e:
                        logger.warning(f"Gemini fallback failed: {e}")
            
            elif self.backend == "gemini":
                for attempt in range(self.MAX_RETRIES):
                    try:
                        if attempt > 0:
                            time.sleep(self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)])
                        
                        prompt = f"Translate the following Nepali text to English. Only provide the translation, nothing else:\n\n{text}"
                        response = self.gemini_model.generate_content(prompt)
                        translated_text = response.text.strip()
                        break
                    except Exception as e:
                        logger.warning(f"Gemini attempt {attempt+1} failed: {e}")
            
            elif self.backend == "marian":
                inputs = self.tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
                generated = self.model.generate(**inputs)
                translated_text = self.tokenizer.decode(generated[0], skip_special_tokens=True)
                
        except Exception as e:
            logger.error(f"Translation error ({self.backend}): {e}")
            return text  # Return original on hard error

        # If no translation result, return original
        if translated_text is None:
            logger.warning("Translation returned None, using original text")
            return text

        # Post-processing: Clean up if still contains Nepali
        if self._contains_nepali(translated_text):
            logger.warning(f"Translation result still contains Nepali. Backend: {self.backend}")
            cleaned_text = "".join([c for c in translated_text if not ('\u0900' <= c <= '\u097F')])
            if len(cleaned_text.strip()) < len(translated_text) * 0.5:
                return "[Translation Pending]"  # Changed from "Failed" to "Pending"
            return cleaned_text

        return translated_text
