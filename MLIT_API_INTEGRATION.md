# MLIT API Integration Documentation

## Project Overview

### Current System
The house-trend system currently processes Japanese real estate data from CSV files downloaded from government sources. It generates over 2,000 charts showing price trends and transaction volumes for 6 prefectures across different room types and languages.

**Current Data Flow:**
```
CSV Files → Data Processing → Chart Generation → Frontend Integration
```

**Target Data Flow:**
```
MLIT API → Data Transformation → Chart Generation → Frontend Integration
```

### Integration Goals
- Replace static CSV data with real-time MLIT API data
- Maintain existing chart format and structure
- Update all 2,000+ charts with latest data
- Preserve current frontend integration

## API Specifications

### MLIT Real Estate Transaction API
- **Provider:** Ministry of Land, Infrastructure, Transport and Tourism (MLIT)
- **Documentation:** https://www.reinfolib.mlit.go.jp/help/apiManual/
- **Endpoint:** `https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001`
- **Authentication:** API Key stored in `.env` file as `Ocp-Apim-Subscription-Key`
- **Rate Limits:** None specified
- **Data Format:** JSON

### API Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| year | Transaction year (YYYY) | 2024 |
| quarter | Transaction quarter (1-4) | 1 |
| area | Prefecture code (2-digit) | 13 (Tokyo) |
| city | Municipality code (5-digit) | Optional |
| priceClassification | Price type | 01 (transaction prices) |

### Prefecture Codes
| Prefecture | Code | Current Data File |
|------------|------|-------------------|
| Tokyo | 13 | tokyo_20071_20234_preprocessed.csv |
| Chiba | 12 | chiba_20071_20234_preprocessed.csv |
| Saitama | 11 | saitama_20071_20234_preprocessed.csv |
| Kanagawa | 14 | kanagawa_20071_20234_preprocessed.csv |
| Osaka | 27 | osaka_20071_20234_preprocessed.csv |
| Aichi | 23 | aichi_20071_20234_preprocessed.csv |

## Data Structure Mapping

### Current CSV Structure
```
種類, 都道府県名, 市区町村名, 地区名, 最寄駅：名称, 最寄駅：距離（分）, 
取引価格（総額）, 間取り, 面積（㎡）, 建築年, 取引時期, 取引時期（年）, 築年数
```

### API JSON Response Structure
```json
{
  "TradePrice": "総取引価格",
  "Area": "面積（㎡）", 
  "BuildingYear": "建築年",
  "Structure": "構造",
  "UnitPrice": "単価",
  "Prefecture": "都道府県",
  "Municipality": "市区町村",
  "District": "地区",
  "NearestStation": "最寄駅",
  "TimeToStation": "駅距離",
  "Purpose": "用途",
  "LandShape": "土地形状",
  "TransactionDate": "取引時期"
}
```

### Field Mapping Strategy
| CSV Column | API Field | Transformation Required |
|------------|-----------|------------------------|
| 取引価格（総額） | TradePrice | Direct mapping |
| 面積（㎡） | Area | Direct mapping |
| 市区町村名 | Municipality | Direct mapping |
| 建築年 | BuildingYear | Direct mapping |
| 取引時期（年） | TransactionDate | Extract year |
| 間取り | Purpose/Structure | **Needs extraction logic** |
| 最寄駅：名称 | NearestStation | Direct mapping |
| 最寄駅：距離（分） | TimeToStation | Direct mapping |

### Critical Data Transformation Challenges

#### 1. Room Type Extraction (間取り)
Current CSV has specific room types: `ALL`, `４ＬＤＫ`, `３ＬＤＫ`, `２ＬＤＫ`, `１ＬＤＫ`, `１Ｋ`

API may provide this in `Purpose` or `Structure` fields. **Investigation needed.**

#### 2. Prefecture Name Standardization
- API returns prefecture codes
- Need to map to Japanese names for consistency

#### 3. Date Format Standardization
- API: Various date formats
- Current: Year extraction for grouping

## Implementation Plan

### Phase 1: API Client Development
```python
# File: backend/house-trend/api_client.py
import os
from dotenv import load_dotenv

class MLITAPIClient:
    def __init__(self):
        load_dotenv()  # Load .env file
        self.api_key = os.getenv('Ocp-Apim-Subscription-Key')
        self.base_url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }
    
    def fetch_prefecture_data(self, prefecture_code, start_year, end_year):
        # Fetch data for all quarters across year range
        pass
    
    def fetch_quarter_data(self, prefecture_code, year, quarter):
        # Fetch specific quarter data with proper headers
        pass
```

### Phase 2: Data Transformation Pipeline
```python
# File: backend/house-trend/data_transformer.py
class APIDataTransformer:
    def transform_api_to_csv_format(self, api_data):
        # Transform API JSON to CSV-like structure
        pass
    
    def extract_room_type(self, purpose, structure):
        # Extract room type from API fields
        pass
    
    def standardize_prefecture_names(self, prefecture_code):
        # Map codes to Japanese names
        pass
```

### Phase 3: Updated Chart Generation
```python
# File: backend/house-trend/chart_generator.py
# Update existing notebooks to use API data instead of CSV
```

### Phase 4: Integration Workflow
```python
# File: backend/house-trend/update_pipeline.py
def run_full_update():
    1. Fetch API data for all prefectures (2007-2024)
    2. Transform data to match current structure
    3. Generate all charts (2000+ files)
    4. Save to frontend directory
    5. Generate completion report
```

## Data Fetching Strategy

### Complete Data Collection
```
6 prefectures × 18 years (2007-2024) × 4 quarters = 432 API calls
```

### Request Sequence
1. **Tokyo (13)**: 2007Q1 → 2024Q4
2. **Chiba (12)**: 2007Q1 → 2024Q4  
3. **Saitama (11)**: 2007Q1 → 2024Q4
4. **Kanagawa (14)**: 2007Q1 → 2024Q4
5. **Osaka (27)**: 2007Q1 → 2024Q4
6. **Aichi (23)**: 2007Q1 → 2024Q4

### Error Handling Strategy
- **API Timeout**: Retry with exponential backoff
- **Missing Data**: Log and continue
- **Invalid Response**: Skip quarter and log error
- **Rate Limiting**: Add delays between requests
- **Network Errors**: Retry up to 3 times

## Chart Generation Requirements

### Current Chart Output
- **Total Charts**: ~2,035 files
- **Format**: PNG (12x8 inches, 150 DPI)
- **Languages**: Japanese and English versions
- **Chart Types**: Dual-axis (price line + transaction volume bars)

### Chart Naming Convention
```
{prefecture}_{area}_{room_type}_{language}.png

Examples:
- tokyo_千代田区_ALL_jp.png
- tokyo_千代田区_ALL_en.png
- chiba_千葉市中央区_２ＬＤＫ_jp.png
```

### Chart Generation Workflow
1. **Data Grouping**: By prefecture → area → room type
2. **Time Series**: Group by year for trend analysis
3. **Statistics**: Calculate yearly averages and counts
4. **Visualization**: Generate dual-axis charts
5. **Output**: Save to `/frontend/img/tool/house-trend/`

## Testing and Validation Plan

### Phase 1: API Connection Testing
```python
# Test API connectivity and authentication
def test_api_connection():
    # Verify API key works
    # Test single prefecture/quarter request
    # Validate response format
```

### Phase 2: Data Transformation Testing
```python
# Test data mapping and transformation
def test_data_transformation():
    # Compare API data with current CSV structure
    # Validate room type extraction
    # Check data completeness
```

### Phase 3: Chart Generation Testing
```python
# Test chart generation with API data
def test_chart_generation():
    # Generate sample charts
    # Compare with existing charts
    # Validate visual consistency
```

### Phase 4: End-to-End Testing
```python
# Test complete pipeline
def test_full_pipeline():
    # Fetch small dataset (1 prefecture, 1 year)
    # Transform data
    # Generate charts
    # Verify output quality
```

## Progress Monitoring and Notifications

### Progress Tracking
```python
def track_progress():
    print(f"Fetching data: {current_prefecture} {current_year}Q{current_quarter}")
    print(f"Progress: {completed_calls}/{total_calls} ({percentage}%)")
    print(f"Charts generated: {generated_charts}/2035")
```

### Completion Notification
```python
def generate_completion_report():
    # Data fetching summary
    # Chart generation summary  
    # Error log summary
    # Performance metrics
```

## File Structure

### New Files to Create
```
backend/house-trend/
├── api_client.py           # MLIT API client
├── data_transformer.py    # Data transformation logic
├── chart_generator.py     # Updated chart generation
├── update_pipeline.py     # Main execution script
├── config.py              # Configuration settings
└── tests/
    ├── test_api_client.py
    ├── test_transformer.py
    └── test_pipeline.py
```

### Updated Files
```
backend/house-trend/backend/
├── generate_image.ipynb    # Update to use API data
├── preprocess.ipynb       # Update for API integration
└── generate_code.ipynb    # Update documentation
```

## Risk Assessment and Mitigation

### Technical Risks
1. **API Data Structure Changes**: Monitor API responses for format changes
2. **Room Type Mapping Failure**: Implement fallback logic for unknown types
3. **Large Data Volume**: Implement memory-efficient processing
4. **Chart Generation Performance**: Optimize matplotlib usage

### Data Quality Risks
1. **Missing Data**: Implement data validation and gap reporting
2. **Inconsistent Formatting**: Add data cleaning and standardization
3. **Historical Data Gaps**: Compare with existing CSV data for validation

### Operational Risks
1. **API Downtime**: Implement retry logic with exponential backoff
2. **Long Processing Time**: Add progress indicators and intermediate saves
3. **Frontend Integration**: Verify chart paths and naming conventions

## Success Criteria

### Data Integration Success
- [ ] All 6 prefectures data fetched successfully
- [ ] Data transformation matches current CSV structure
- [ ] Room type extraction accuracy > 95%
- [ ] No missing years in dataset (2007-2024)

### Chart Generation Success
- [ ] All 2,000+ charts regenerated
- [ ] Visual consistency with existing charts
- [ ] Proper Japanese and English versions
- [ ] Charts saved to correct frontend directory

### System Integration Success
- [ ] Frontend displays updated charts correctly
- [ ] No broken image links
- [ ] Performance maintained (chart loading speed)
- [ ] Mobile compatibility preserved

## 🌐 Live Frontend Integration

The system generates charts that are integrated into the live website with interactive displays:

### English Pages
- **Tokyo**: https://heysho.com/en/trend/house/tokyo.html
- **Kanagawa**: https://heysho.com/en/trend/house/kanagawa.html
- **Chiba**: https://heysho.com/en/trend/house/chiba.html
- **Saitama**: https://heysho.com/en/trend/house/saitama.html
- **Osaka**: https://heysho.com/en/trend/house/osaka.html
- **Aichi**: https://heysho.com/en/trend/house/aichi.html

### Japanese Pages
- **東京**: https://heysho.com/trend/house/tokyo.html
- **神奈川**: https://heysho.com/trend/house/kanagawa.html
- **千葉**: https://heysho.com/trend/house/chiba.html
- **埼玉**: https://heysho.com/trend/house/saitama.html
- **大阪**: https://heysho.com/trend/house/osaka.html
- **愛知**: https://heysho.com/trend/house/aichi.html

### Integration Features
- **Responsive Modal Display**: Charts open in full-screen modal windows
- **Bilingual Support**: Complete Japanese and English versions
- **Interactive Navigation**: Easy area and room type selection
- **Mobile Optimization**: Touch-friendly interface for all devices

---

**Document Version**: 1.0
**Created**: 2025-09-13
**Last Updated**: 2025-09-14
**Status**: Ready for Implementation