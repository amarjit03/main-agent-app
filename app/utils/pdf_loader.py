import os
import logging
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract
import pdf2image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFLoader:
    """Class to handle PDF loading and text extraction."""
    
    def __init__(self, ocr_language: str = 'eng'):
        """Initialize the PDF loader.
        
        Args:
            ocr_language: Language for OCR (default: English)
        """
        self.ocr_language = ocr_language
    
    def load_pdf(self, pdf_path: Union[str, Path]) -> str:
        """Load PDF and extract text.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from the PDF
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        logger.info(f"Loading PDF: {pdf_path}")
        
        # Try regular text extraction first
        text = self._extract_with_pdfplumber(pdf_path)
        
        # If no text extracted, use OCR
        if not text.strip():
            logger.info("No text found, attempting OCR extraction")
            text = self._extract_with_ocr(pdf_path)
        
        return text
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber for regular PDFs.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {i+1} ---\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Failed to extract page {i+1}: {e}")
            
            if text.strip():
                logger.info("Successfully extracted text using pdfplumber")
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
        
        return text
    
    def _extract_with_ocr(self, pdf_path: Path, dpi: int = 300) -> str:
        """Extract text using OCR for scanned PDFs.
        
        Args:
            pdf_path: Path to the PDF file
            dpi: DPI for image conversion
            
        Returns:
            Extracted text
        """
        text = ""
        
        try:
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
            
            # Extract text from each image
            for i, image in enumerate(images):
                try:
                    page_text = pytesseract.image_to_string(image, lang=self.ocr_language)
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n"
                        text += page_text
                except Exception as e:
                    logger.warning(f"Failed to OCR page {i+1}: {e}")
            
            if text.strip():
                logger.info("Successfully extracted text using OCR")
            else:
                logger.warning("No text could be extracted from the PDF")
                
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
        
        return text
    
    # def save_as_text(self, pdf_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Path:
    #     """Load PDF and save extracted text to a file.
        
    #     Args:
    #         pdf_path: Path to the PDF file
    #         output_path: Path for output text file (optional)
            
    #     Returns:
    #         Path to the saved text file
    #     """
    #     pdf_path = Path(pdf_path)
        
    #     # Generate output path if not provided
    #     if output_path is None:
    #         output_path = pdf_path.with_suffix('.txt')
    #     else:
    #         output_path = Path(output_path)
        
    #     # Extract text
    #     text = self.load_pdf(pdf_path)
        
    #     # Save to file
    #     with open(output_path, 'w', encoding='utf-8') as f:
    #         f.write(text)
        
    #     logger.info(f"Text saved to: {output_path}")
    #     return output_path
    
    # def batch_convert(self, pdf_folder: Union[str, Path], output_folder: Optional[Union[str, Path]] = None) -> List[Path]:
    #     """Convert multiple PDFs in a folder to text files.
        
    #     Args:
    #         pdf_folder: Folder containing PDF files
    #         output_folder: Folder for output text files (optional)
            
    #     Returns:
    #         List of paths to created text files
    #     """
    #     pdf_folder = Path(pdf_folder)
        
    #     if not pdf_folder.is_dir():
    #         raise ValueError(f"Not a directory: {pdf_folder}")
        
    #     # Create output folder if needed
    #     if output_folder is None:
    #         output_folder = pdf_folder / "extracted_text"
    #     else:
    #         output_folder = Path(output_folder)
        
    #     output_folder.mkdir(exist_ok=True)
        
    #     # Process all PDFs
    #     converted_files = []
    #     pdf_files = list(pdf_folder.glob("*.pdf"))
        
    #     logger.info(f"Found {len(pdf_files)} PDF files to process")
        
    #     for i, pdf_file in enumerate(pdf_files, 1):
    #         logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
    #         try:
    #             output_path = output_folder / pdf_file.with_suffix('.txt').name
    #             self.save_as_text(pdf_file, output_path)
    #             converted_files.append(output_path)
    #         except Exception as e:
    #             logger.error(f"Failed to convert {pdf_file.name}: {e}")
        
    #     logger.info(f"Successfully converted {len(converted_files)} files")
    #     return converted_files

    # ...existing code...
    def save_as_text(self, pdf_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Path:
        """Load PDF and save extracted text to a file.
           Args:
                pdf_path: Path to the PDF file
                output_path: Path for output text file (optional)

            Returns: 
                   Path to the saved text file
        """
        pdf_path = Path(pdf_path)

        # Always save in 'textdata' folder
        textdata_folder = pdf_path.parent / "textdata"
        textdata_folder.mkdir(exist_ok=True)

        # Generate output path in 'textdata' folder
        if output_path is None:
            output_path = textdata_folder / pdf_path.with_suffix('.txt').name
        else:
            output_path = Path(output_path)
        # If output_path is not in 'textdata', move it there
        if output_path.parent != textdata_folder:
            output_path = textdata_folder / output_path.name

        # Extract text
        text = self.load_pdf(pdf_path)

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        logger.info(f"Text saved to: {output_path}")
        return output_path

    def batch_convert(self, pdf_folder: Union[str, Path], output_folder: Optional[Union[str, Path]] = None) -> List[Path]:
        """Convert multiple PDFs in a folder to text files.

        Args:
            pdf_folder: Folder containing PDF files
           output_folder: Folder for output text files (optional)

    Returns:
        List of paths to created text files
    """
        pdf_folder = Path(pdf_folder)

        if not pdf_folder.is_dir():
            raise ValueError(f"Not a directory: {pdf_folder}")

        # Always use 'textdata' folder inside pdf_folder
        output_folder = pdf_folder / "textdata"
        output_folder.mkdir(exist_ok=True)
    
        # Process all PDFs
        converted_files = []
        pdf_files = list(pdf_folder.glob("*.pdf"))
    
        logger.info(f"Found {len(pdf_files)} PDF files to process")
    
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")

            try:
                output_path = output_folder / pdf_file.with_suffix('.txt').name
                self.save_as_text(pdf_file, output_path)
                converted_files.append(output_path)
            except Exception as e:
                logger.error(f"Failed to convert {pdf_file.name}: {e}")

        logger.info(f"Successfully converted {len(converted_files)} files")
        return converted_files



