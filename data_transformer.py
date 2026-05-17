"""
Data Transformer for MLIT API to CSV Format
Maps API JSON response to match current CSV structure for chart generation
"""

import pandas as pd
import re
from typing import List, Dict, Optional
from datetime import datetime

class APIDataTransformer:
    def __init__(self):
        """Initialize transformer with mapping configurations"""
        
        # Room type standardization mapping
        self.room_type_mapping = {
            '１Ｒ': '１Ｒ',
            '１Ｋ': '１Ｋ', 
            '１ＤＫ': '１Ｋ',  # Map 1DK to 1K for simplification
            '１ＬＤＫ': '１ＬＤＫ',
            '２Ｋ': '１Ｋ',  # Map 2K to 1K for simplification  
            '２ＤＫ': '２ＬＤＫ',  # Map 2DK to 2LDK for simplification
            '２ＬＤＫ': '２ＬＤＫ',
            '３Ｋ': '３ＬＤＫ',  # Map 3K to 3LDK for simplification
            '３ＤＫ': '３ＬＤＫ',  # Map 3DK to 3LDK for simplification
            '３ＬＤＫ': '３ＬＤＫ',
            '４Ｋ': '４ＬＤＫ',  # Map 4K to 4LDK for simplification
            '４ＤＫ': '４ＬＤＫ',  # Map 4DK to 4LDK for simplification
            '４ＬＤＫ': '４ＬＤＫ',
            '５Ｋ以上': '４ＬＤＫ',  # Map 5K+ to 4LDK for simplification
            '５ＤＫ以上': '４ＬＤＫ',  # Map 5DK+ to 4LDK for simplification
            '５ＬＤＫ以上': '４ＬＤＫ',  # Map 5LDK+ to 4LDK for simplification
        }
        
        # Prefecture name standardization
        self.prefecture_name_mapping = {
            '東京都': '東京都',
            '千葉県': '千葉県',
            '埼玉県': '埼玉県', 
            '神奈川県': '神奈川県',
            '大阪府': '大阪府',
            '愛知県': '愛知県'
        }
        
        # Property type filter (focus on residential condominiums)
        self.valid_property_types = [
            '中古マンション等',
            '宅地(土地と建物)',
            '土地',
            '建物'
        ]
    
    def extract_year_from_period(self, period: str) -> Optional[int]:
        """
        Extract year from period string like '2024年第1四半期'
        
        Args:
            period: Period string from API
            
        Returns:
            Year as integer or None if parsing fails
        """
        try:
            match = re.search(r'(\d{4})年', period)
            if match:
                return int(match.group(1))
        except:
            pass
        return None
    
    def extract_building_age(self, building_year: str, transaction_year: int) -> Optional[int]:
        """
        Calculate building age from building year and transaction year
        
        Args:
            building_year: Building year string like '2003年'
            transaction_year: Transaction year
            
        Returns:
            Building age in years or None if calculation fails
        """
        try:
            if building_year and '年' in building_year:
                built_year = int(building_year.replace('年', ''))
                age = transaction_year - built_year
                return max(0, age)  # Age cannot be negative
        except:
            pass
        return None
    
    def standardize_room_type(self, floor_plan: str) -> str:
        """
        Standardize room type to match current chart categories
        
        Args:
            floor_plan: FloorPlan from API
            
        Returns:
            Standardized room type
        """
        if not floor_plan:
            return 'その他'
        
        # Clean the input
        clean_plan = floor_plan.strip()
        
        # Direct mapping first
        if clean_plan in self.room_type_mapping:
            return self.room_type_mapping[clean_plan]
        
        # Pattern-based matching for edge cases
        if '１Ｒ' in clean_plan or '1R' in clean_plan:
            return '１Ｒ'
        elif '１Ｋ' in clean_plan or '1K' in clean_plan:
            return '１Ｋ'
        elif '１ＬＤＫ' in clean_plan or '1LDK' in clean_plan:
            return '１ＬＤＫ'
        elif '２ＬＤＫ' in clean_plan or '2LDK' in clean_plan:
            return '２ＬＤＫ'
        elif '３ＬＤＫ' in clean_plan or '3LDK' in clean_plan:
            return '３ＬＤＫ'
        elif '４ＬＤＫ' in clean_plan or '4LDK' in clean_plan:
            return '４ＬＤＫ'
        else:
            return 'その他'
    
    def clean_price(self, trade_price: str) -> Optional[int]:
        """
        Clean and convert trade price to integer
        
        Args:
            trade_price: TradePrice from API (string)
            
        Returns:
            Price as integer or None if conversion fails
        """
        try:
            if trade_price:
                # Remove any non-digit characters and convert
                clean_price = re.sub(r'[^\d]', '', str(trade_price))
                return int(clean_price) if clean_price else None
        except:
            pass
        return None
    
    def clean_area(self, area: str) -> Optional[float]:
        """
        Clean and convert area to float
        
        Args:
            area: Area from API (string)
            
        Returns:
            Area as float or None if conversion fails
        """
        try:
            if area:
                # Remove any non-numeric characters except decimal point
                clean_area = re.sub(r'[^\d.]', '', str(area))
                return float(clean_area) if clean_area else None
        except:
            pass
        return None
    
    def transform_api_record(self, api_record: Dict) -> Dict:
        """
        Transform a single API record to CSV format
        
        Args:
            api_record: Single record from API response
            
        Returns:
            Dictionary matching CSV structure
        """
        # Extract transaction year
        transaction_year = self.extract_year_from_period(api_record.get('Period', ''))
        
        # Transform the record
        transformed = {
            '種類': api_record.get('Type', ''),
            '都道府県名': api_record.get('Prefecture', ''),
            '市区町村名': api_record.get('Municipality', ''),
            '地区名': api_record.get('DistrictName', ''),
            '最寄駅：名称': '',  # Not available in API
            '最寄駅：距離（分）': '',  # Not available in API
            '取引価格（総額）': self.clean_price(api_record.get('TradePrice', '')),
            '間取り': self.standardize_room_type(api_record.get('FloorPlan', '')),
            '面積（㎡）': self.clean_area(api_record.get('Area', '')),
            '建築年': api_record.get('BuildingYear', ''),
            '取引時期': api_record.get('Period', ''),
            '取引時期（年）': transaction_year,
            '築年数': self.extract_building_age(
                api_record.get('BuildingYear', ''), 
                transaction_year or 2024
            )
        }
        
        return transformed
    
    def transform_api_data(self, api_data: List[Dict]) -> pd.DataFrame:
        """
        Transform list of API records to pandas DataFrame matching CSV structure
        
        Args:
            api_data: List of records from API
            
        Returns:
            DataFrame with CSV-compatible structure
        """
        if not api_data:
            return pd.DataFrame()
        
        print(f"Transforming {len(api_data)} API records...")
        
        # Transform each record
        transformed_records = []
        for record in api_data:
            # Filter for residential properties only
            if record.get('Type') in self.valid_property_types:
                transformed = self.transform_api_record(record)
                # Only include records with valid price and year
                if transformed['取引価格（総額）'] and transformed['取引時期（年）']:
                    transformed_records.append(transformed)
        
        if not transformed_records:
            print("⚠️ No valid records after transformation")
            return pd.DataFrame()
        
        # Create DataFrame
        df = pd.DataFrame(transformed_records)
        
        # Data quality report
        print(f"✅ Transformation complete:")
        print(f"  Input records: {len(api_data)}")
        print(f"  Valid records: {len(df)}")
        print(f"  Years covered: {df['取引時期（年）'].min()}-{df['取引時期（年）'].max()}")
        print(f"  Room types: {df['間取り'].unique().tolist()}")
        print(f"  Areas: {df['市区町村名'].nunique()} unique areas")
        
        return df
    
    def validate_transformed_data(self, df: pd.DataFrame) -> Dict:
        """
        Validate transformed data quality
        
        Args:
            df: Transformed DataFrame
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'total_records': len(df),
            'missing_prices': df['取引価格（総額）'].isna().sum(),
            'missing_areas': df['面積（㎡）'].isna().sum(),
            'missing_room_types': df['間取り'].isna().sum(),
            'valid_years': df['取引時期（年）'].notna().sum(),
            'year_range': (df['取引時期（年）'].min(), df['取引時期（年）'].max()) if len(df) > 0 else (None, None),
            'unique_areas': df['市区町村名'].nunique(),
            'room_type_distribution': df['間取り'].value_counts().to_dict()
        }
        
        return validation

if __name__ == "__main__":
    # Test the transformer
    from api_client import MLITAPIClient
    
    client = MLITAPIClient()
    transformer = APIDataTransformer()
    
    # Get sample data
    print("Testing data transformation...")
    sample_data = client.fetch_quarter_data('13', '2024', '1')
    
    if sample_data:
        # Transform the data
        df = transformer.transform_api_data(sample_data)
        
        if not df.empty:
            print(f"\nSample transformed data:")
            print(df.head())
            print(f"\nColumns: {list(df.columns)}")
            
            # Validation
            validation = transformer.validate_transformed_data(df)
            print(f"\nValidation results:")
            for key, value in validation.items():
                print(f"  {key}: {value}")
        else:
            print("No data after transformation")
    else:
        print("No sample data retrieved")