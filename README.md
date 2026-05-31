# Japan House Trend Analysis System

This directory contains a complete MLIT (Ministry of Land, Infrastructure, Transport and Tourism) API integration system for Japanese real estate trend analysis, including automated data processing, chart generation, and frontend integration.

## 🚀 Quick Start

### Test the System
```bash
# Test with limited data (Tokyo only, recent data)
python update_pipeline.py
```

### Full Production Update
```bash
# Update all 6 prefectures with complete data (2007-2025)
python run_full_update.py
```

## 📁 Project Structure

```
japan-house-trend/
├── README.md                    # This documentation
├── MLIT_API_INTEGRATION.md     # Technical API documentation
├── api_client.py               # MLIT API client with authentication
├── data_transformer.py         # JSON to CSV data transformation
├── update_pipeline.py          # Main data processing & chart generation pipeline
├── run_full_update.py         # Production batch processing script
├── api_data/                  # Raw API responses (Git ignored)
├── data/                      # Processed CSV files (Git ignored)
└── raw_data/                  # Legacy data files (Git ignored)
```

## 🏗️ System Architecture

```
MLIT API → Data Fetching → Processing → Chart Generation → Frontend Integration
    ↓           ↓            ↓              ↓                   ↓
Raw JSON → Transformed → CSV Files → 3,620 Charts → Website Display
```

## 🌐 Live Frontend Demo

The generated charts are integrated into the live website with interactive modal displays:

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

## 📊 Data Coverage

### Supported Prefectures
| Prefecture | Code | Records | Areas | Status |
|------------|------|---------|-------|---------|
| 東京 (Tokyo) | 13 | 479,508 | 59 | ✅ Complete |
| 千葉 (Chiba) | 12 | 170,573 | 59 | ✅ Complete |
| 埼玉 (Saitama) | 11 | 197,394 | 72 | ✅ Complete |
| 神奈川 (Kanagawa) | 14 | 296,233 | 58 | ✅ Complete |
| 大阪 (Osaka) | 27 | 281,291 | 72 | ✅ Complete |
| 愛知 (Aichi) | 23 | 157,362 | 69 | ✅ Complete |

**Total**: 1,582,361 real estate transactions

### Time Period
- **Data Range**: 2007-2025 (through Q4)
- **Current Status**: 2025 data includes Q1-Q4 records available from the MLIT API
- **Latest Quarter Note**: The latest released quarter can contain fewer records than prior quarters depending on MLIT publication status
- **Update Frequency**: Quarterly (as MLIT releases new data)

### Room Types
- **ALL** - All room types combined
- **４ＬＤＫ** - 4LDK apartments
- **３ＬＤＫ** - 3LDK apartments
- **２ＬＤＫ** - 2LDK apartments
- **１ＬＤＫ** - 1LDK apartments
- **１Ｋ** - 1K apartments

## 📈 Chart Generation System

### Features
- **Dual-axis visualization**: Price trends (line) + Transaction volume (bars)
- **Bilingual support**: Japanese and English versions
- **Clean formatting**: No scientific notation, proper number formatting
- **Japanese localization**: "平均取引価格" and "取引回数" legends

### Chart Output
- **Total Charts Generated**: 3,620 charts
- **Format**: lossless WebP, 12x8 inches, 150 DPI
- **Languages**: Japanese (_jp) and English (_en) versions
- **Location**: `../../frontend/img/trend/house/`
- **Current Size**: 113.7 MB total after WebP conversion (previous PNG set was 331.5 MB)

### Naming Convention
```
{prefecture}_{area}_{room_type}_{language}.webp

Examples:
- aichi_名古屋市千種区_ALL_jp.webp
- aichi_名古屋市千種区_ALL_en.webp
- tokyo_千代田区_３ＬＤＫ_jp.webp
```

## 🔧 Recent Improvements (2026-05-30)

### Batch Processing System
- **Problem Solved**: System crashes from processing large datasets
- **Solution**: 3-area batches with progress tracking
- **Result**: 100% success rate, zero crashes
- **Performance**: Consistent 36 charts per batch

### Chart Formatting Enhancements
- **Number Format**: Eliminated scientific notation (1e8 → 30,000,000)
- **Y-axis Cleanup**: Removed unit clutter "（万円）" from labels
- **Localization**: Japanese legend labels for Japanese charts
- **Consistency**: Uniform formatting across all prefectures

### Data Integration
- **2025 Integration**: Successfully integrated 2025 data through Q4 across all 6 prefectures
- **Saitama Refresh**: Updated Saitama from stale historical coverage to the same 2007-2025 range as other prefectures
- **Coverage Analysis**: Automated reporting of data completeness and chart output counts

### WebP Chart Assets
- **Format Change**: Converted frontend chart assets from PNG to lossless WebP
- **Size Reduction**: Reduced chart image storage from 331.5 MB to 113.7 MB
- **Pipeline Update**: `update_pipeline.py` now renders charts to an in-memory PNG buffer and writes lossless WebP files through Pillow
- **Frontend Sync**: HTML chart references use `.webp`; cards with no corresponding chart asset should be removed to avoid broken images

## 💻 Usage Examples

### Generate Charts for All Prefectures
```python
from update_pipeline import HouseTrendUpdater

# Initialize the system
updater = HouseTrendUpdater()

# Process in manageable batches
prefectures = ['tokyo', 'chiba', 'saitama', 'kanagawa', 'osaka', 'aichi']
for prefecture in prefectures:
    # Load processed data
    df = pd.read_csv(f'data/{prefecture}_api_processed.csv')

    # Generate charts in small batches (prevents crashes)
    areas = df['市区町村名'].unique()
    for i in range(0, len(areas), 3):  # Process 3 areas at a time
        batch_areas = areas[i:i+3]
        charts_count = updater.generate_charts_batch(prefecture, df, batch_areas)
        print(f'Generated {charts_count} charts for {prefecture}')
```

### Check 2025 Data Coverage
```python
import pandas as pd

prefecture = 'tokyo'
df = pd.read_csv(f'data/{prefecture}_api_processed.csv')
df_2025 = df[df['取引時期（年）'] == 2025]

print(f"2025 transactions: {len(df_2025):,}")
print(f"2025 periods: {df_2025['取引時期'].unique()}")
```

## 📋 Performance Metrics

### Latest Complete Run (2026-05-30)
- **Charts Generated**: 3,620 total
- **Success Rate**: 100% (no crashes)
- **Data Processed**: 1,582,361 transactions
- **Prefectures Completed**: 6/6

### Breakdown by Prefecture
| Prefecture | Areas | Charts |
|------------|-------|--------|
| Tokyo | 59 | 610 |
| Chiba | 59 | 386 |
| Saitama | 72 | 628 |
| Kanagawa | 58 | 594 |
| Osaka | 72 | 766 |
| Aichi | 69 | 636 |

## 🛠️ Installation & Setup

### Requirements
```bash
pip install pandas numpy matplotlib japanize-matplotlib requests python-dotenv pillow
```

### Environment Configuration
Copy `.env.example` to `.env` and fill in your MLIT API key:
```bash
cp .env.example .env
```
And set your API key in `.env`:
`Ocp-Apim-Subscription-Key="your_mlit_api_key_here"`

### Directory Structure Setup
Ensure the following directories exist locally (ignored by Git):
```
backend/japan-house-trend/api_data/     # API responses (created automatically)
backend/japan-house-trend/data/         # Processed CSV files (created automatically)
frontend/img/trend/house/               # Chart output location
```


## 🚨 Troubleshooting

### Common Issues

**1. Chart Generation Crashes**
- **Cause**: Processing too many areas simultaneously
- **Solution**: Use batch processing (3 areas per batch)
- **Command**: Use `generate_charts_batch()` method

**2. Scientific Notation in Charts**
- **Status**: ✅ Fixed (2025-09-13)
- **Solution**: Custom FuncFormatter implementation
- **Result**: Clean number display (e.g., "30,000,000")

**3. Japanese Font Issues**
- **Solution**: Ensure `japanize-matplotlib` is installed
- **Note**: Charts generate correctly despite font warnings

**4. 2025 Transaction Counts Look Low**
- **Cause**: The latest MLIT quarter can have fewer available records than earlier quarters, and transformation filters remove records without required fields
- **Check**: Compare CSV counts by quarter with `df[df['取引時期（年）'] == 2025]['取引時期'].value_counts()`
- **Note**: Confirm whether the WebP asset was regenerated after CSV updates if a chart appears inconsistent with CSV counts

**5. Broken Chart Images**
- **Cause**: HTML may reference area/room-type combinations that are absent in current CSV data and therefore do not produce chart files
- **Solution**: Remove cards whose referenced WebP files do not exist, or regenerate the matching chart if data is available
- **Check**: Verify all HTML `img/trend/house/*.webp` references exist in `frontend/img/trend/house/`

## 📝 Data Quality & Validation

### Automated Checks
- **Data Completeness**: Validates all prefecture data loaded
- **Year Coverage**: Confirms 2007-2025 range
- **Chart Generation**: Counts and verifies all output files
- **Error Tracking**: Comprehensive logging of any failures

## 🔄 Maintenance

### Regular Updates
1. **Quarterly Data Refresh**: When MLIT releases new quarterly data
2. **Chart Regeneration**: Run full update to incorporate new data
3. **Frontend Sync**: Ensure HTML files reflect current data status
4. **Performance Monitoring**: Track processing times and success rates

### Quality Assurance
- Review completion reports in `api_data/` directory
- Verify chart counts match expected totals for non-empty area/room-type combinations
- Confirm no stale PNG references remain in frontend HTML
- Confirm no broken chart references remain after removing cards for missing assets
- Spot-check chart visual consistency and formatting
- Monitor system performance during batch processing

## 📚 Documentation

### Technical Documentation
- **`MLIT_API_INTEGRATION.md`**: Complete API integration guide
- **`README.md`**: This overview and usage guide
- **Code Comments**: Inline documentation in all Python files

### Frontend Integration
Charts are automatically integrated into the website:
- **Japanese Pages**: `/frontend/trend/house/{prefecture}.html`
- **English Pages**: `/frontend/en/trend/house/{prefecture}.html`
- **Modal Display**: Charts open in responsive modal windows

## 🏆 Recent Achievements

- ✅ **Complete Data Integration**: 2025 Q4 data across all 6 prefectures
- ✅ **System Stability**: 100% success rate with batch processing
- ✅ **Chart Quality**: Professional formatting with clean numbers and Japanese localization
- ✅ **Bilingual Support**: Full Japanese and English chart generation
- ✅ **User Experience**: Responsive modal display with updated charts
- ✅ **Asset Optimization**: Lossless WebP chart assets reduce image storage and page payload
- ✅ **Performance**: Efficient batch processing preventing system crashes

---

**Last Updated**: 2026-05-30
**System Status**: ✅ Fully Operational
**Data Status**: 2007-2025 Q4 Complete
**Chart Status**: 3,620 charts generated and deployed
