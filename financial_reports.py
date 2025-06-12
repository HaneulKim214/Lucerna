import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import PyPDF2
import tempfile
from typing import Optional, Tuple

class FinancialReportDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.temp_dir = tempfile.mkdtemp()

    def _search_sec_edgar(self, company_name: str) -> Optional[str]:
        """Search SEC EDGAR database for company filings."""
        search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={company_name}&owner=exclude&action=getcompany"
        try:
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for 10-K or Annual Report links
            for link in soup.find_all('a'):
                if '10-K' in link.text or 'Annual Report' in link.text:
                    return urljoin('https://www.sec.gov', link['href'])
        except Exception as e:
            print(f"Error searching SEC EDGAR: {e}")
        return None

    def _download_pdf(self, url: str) -> Optional[str]:
        """Download PDF from URL and save to temporary file."""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                temp_file = os.path.join(self.temp_dir, 'financial_report.pdf')
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                return temp_file
        except Exception as e:
            print(f"Error downloading PDF: {e}")
        return None

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return text

    def get_latest_financial_report(self, company_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the latest financial report for a company.
        Returns a tuple of (pdf_path, extracted_text)
        """
        # Search for the report
        report_url = self._search_sec_edgar(company_name)
        if not report_url:
            return None, None

        # Download the PDF
        pdf_path = self._download_pdf(report_url)
        if not pdf_path:
            return None, None

        # Extract text from PDF
        text = self._extract_text_from_pdf(pdf_path)
        
        return pdf_path, text

    def cleanup(self):
        """Clean up temporary files."""
        try:
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}") 