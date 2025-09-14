"""
MLIT Real Estate Transaction API Client
Handles authentication and data fetching from MLIT API
"""

import os
import requests
import json
import time
from typing import Dict, List, Optional
from dotenv import load_dotenv
import pandas as pd

class MLITAPIClient:
    def __init__(self):
        """Initialize API client with authentication from .env file"""
        load_dotenv()
        self.api_key = os.getenv('Ocp-Apim-Subscription-Key')
        if not self.api_key:
            raise ValueError("API key not found in .env file. Please set Ocp-Apim-Subscription-Key")
        
        self.base_url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Prefecture mapping
        self.prefecture_codes = {
            'tokyo': '13',
            'chiba': '12', 
            'saitama': '11',
            'kanagawa': '14',
            'osaka': '27',
            'aichi': '23'
        }
        
        # Prefecture name mapping (code to Japanese name)
        self.prefecture_names = {
            '13': '東京都',
            '12': '千葉県',
            '11': '埼玉県', 
            '14': '神奈川県',
            '27': '大阪府',
            '23': '愛知県'
        }
    
    def test_connection(self) -> bool:
        """Test API connection with a simple request"""
        try:
            print("Testing API connection...")
            response = self.fetch_quarter_data('13', '2024', '1')  # Tokyo, 2024 Q1
            if response and len(response) > 0:
                print(f"✅ API connection successful. Retrieved {len(response)} records.")
                return True
            else:
                print("⚠️ API connection successful but no data returned")
                return True
        except Exception as e:
            print(f"❌ API connection failed: {e}")
            return False
    
    def fetch_quarter_data(self, prefecture_code: str, year: str, quarter: str, 
                          city: Optional[str] = None) -> List[Dict]:
        """
        Fetch real estate data for a specific prefecture, year, and quarter
        
        Args:
            prefecture_code: 2-digit prefecture code
            year: Year in YYYY format
            quarter: Quarter (1-4)
            city: Optional 5-digit city code
            
        Returns:
            List of transaction records
        """
        params = {
            'year': year,
            'quarter': quarter,
            'area': prefecture_code,
            'priceClassification': '01'  # Transaction prices
        }
        
        if city:
            params['city'] = city
            
        try:
            print(f"Fetching: Prefecture {prefecture_code}, {year}Q{quarter}")
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('status') == 'OK' and 'data' in response_data:
                    data = response_data['data']
                    print(f"  ✅ Retrieved {len(data)} records")
                    return data
                else:
                    print(f"  ⚠️ API returned status: {response_data.get('status', 'Unknown')}")
                    return []
            else:
                print(f"  ❌ HTTP {response.status_code}: {response.text}")
                return []
                
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout for {prefecture_code} {year}Q{quarter}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request error: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON decode error: {e}")
            return []
    
    def fetch_prefecture_data(self, prefecture_code: str, start_year: int, 
                             end_year: int, delay: float = 0.1) -> List[Dict]:
        """
        Fetch all data for a prefecture across multiple years and quarters
        
        Args:
            prefecture_code: 2-digit prefecture code
            start_year: Starting year
            end_year: Ending year (inclusive)
            delay: Delay between requests to be respectful to API
            
        Returns:
            Combined list of all transaction records
        """
        all_data = []
        total_quarters = (end_year - start_year + 1) * 4
        current_quarter = 0
        
        prefecture_name = self.prefecture_names.get(prefecture_code, prefecture_code)
        print(f"\n📊 Fetching data for {prefecture_name} ({start_year}-{end_year})")
        print(f"Expected quarters: {total_quarters}")
        
        for year in range(start_year, end_year + 1):
            for quarter in range(1, 5):
                current_quarter += 1
                progress = (current_quarter / total_quarters) * 100
                
                quarter_data = self.fetch_quarter_data(
                    prefecture_code, str(year), str(quarter)
                )
                
                if quarter_data:
                    # Add metadata to each record
                    for record in quarter_data:
                        record['prefecture_code'] = prefecture_code
                        record['prefecture_name'] = prefecture_name
                        record['fetch_year'] = year
                        record['fetch_quarter'] = quarter
                    
                    all_data.extend(quarter_data)
                
                print(f"  Progress: {progress:.1f}% ({current_quarter}/{total_quarters})")
                
                # Be respectful to the API
                if delay > 0:
                    time.sleep(delay)
        
        print(f"✅ {prefecture_name} complete: {len(all_data)} total records")
        return all_data
    
    def fetch_all_prefectures(self, start_year: int = 2007, end_year: int = 2024) -> Dict[str, List[Dict]]:
        """
        Fetch data for all 6 prefectures
        
        Args:
            start_year: Starting year (default: 2007)
            end_year: Ending year (default: 2024)
            
        Returns:
            Dictionary with prefecture names as keys and data lists as values
        """
        all_prefecture_data = {}
        total_prefectures = len(self.prefecture_codes)
        
        print(f"\n🚀 Starting full data fetch for {total_prefectures} prefectures")
        print(f"Time range: {start_year}-{end_year}")
        print(f"Estimated API calls: {total_prefectures * (end_year - start_year + 1) * 4}")
        
        for i, (prefecture_name, prefecture_code) in enumerate(self.prefecture_codes.items(), 1):
            print(f"\n{'='*60}")
            print(f"Prefecture {i}/{total_prefectures}: {prefecture_name.upper()}")
            print(f"{'='*60}")
            
            try:
                prefecture_data = self.fetch_prefecture_data(
                    prefecture_code, start_year, end_year
                )
                all_prefecture_data[prefecture_name] = prefecture_data
                
            except Exception as e:
                print(f"❌ Failed to fetch data for {prefecture_name}: {e}")
                all_prefecture_data[prefecture_name] = []
        
        # Summary
        total_records = sum(len(data) for data in all_prefecture_data.values())
        print(f"\n📈 FETCH COMPLETE")
        print(f"Total records retrieved: {total_records:,}")
        
        for prefecture, data in all_prefecture_data.items():
            print(f"  {prefecture}: {len(data):,} records")
        
        return all_prefecture_data
    
    def save_raw_data(self, data: Dict[str, List[Dict]], output_dir: str = "api_data"):
        """
        Save raw API data to JSON files for backup and analysis
        
        Args:
            data: Prefecture data dictionary
            output_dir: Output directory for JSON files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for prefecture, records in data.items():
            if records:
                filename = f"{output_dir}/{prefecture}_api_raw.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
                print(f"💾 Saved {len(records)} records to {filename}")
            else:
                print(f"⚠️ No data to save for {prefecture}")

if __name__ == "__main__":
    # Test the API client
    client = MLITAPIClient()
    
    # Test connection
    if client.test_connection():
        print("API client is ready to use!")
    else:
        print("API client setup failed.")