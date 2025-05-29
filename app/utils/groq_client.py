from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import logging
import time
# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class groqClient:
    """Class to handle LLM interactions and response processing."""
    def __init__(self):
        """Initialize the LLM processor."""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'llama3-70b-8192')
        self.temperature = float(os.getenv('TEMPERATURE') or 0.7)
        self.max_tokens = int(os.getenv('MAX_TOKENS') or 4096)

        if not self.api_key:
            logger.warning("No GROQ_API_KEY found in environment variables. LLM functionality will not work.")
            self.llm = None
        else:
            self._init_llm()   # Initialize LLM

    def _init_llm(self):
        try:
            self.llm = ChatGroq(
                api_key=self.api_key,
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.info(f"LLM initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Unable to connect LLM error: {e}")
            raise
