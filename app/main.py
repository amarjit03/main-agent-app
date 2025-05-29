from utils import groq_client
from langchain_core.messages import HumanMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Initialize logger
logger = logging.getLogger(__name__)

def main():
    """Main function to run the Groq client."""
    try:
        # Initialize the Groq client
        groq_client_instance = groq_client.groqClient()
        
        if not groq_client_instance.llm:
            logger.error("LLM is not initialized. Exiting.")
            return
        
        # Example prompt
        prompt = "What is the capital of France?"
        
        # Create a HumanMessage
        human_message = HumanMessage(content=prompt)
        
        # Get the response from the LLM
        response = groq_client_instance.llm.invoke([human_message])
        
        # Log the response
        logger.info(f"Response: {response.content}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
