from utils.pdf_loader import PDFLoader


def main():
    """Main function to extract text from a PDF file and save it as .txt in textdata folder."""
    try:
        # Initialize the PDF loader
        loader = PDFLoader()
        
        # Example PDF file path
        pdf_file = "data/239528_1613926124.pdf"  # Replace with your PDF file
        
        # Extract and save the text to textdata folder
        txt_path = loader.save_as_text(pdf_file)
        print(f"Text extracted and saved to: {txt_path}")

        # Optionally, print the first 500 characters
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            print(f"\nFirst 500 characters:\n{text[:500]}")
        
    except FileNotFoundError:
        print("Please provide a valid PDF file path")

if __name__ == "__main__":
    main()
