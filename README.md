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
# Update all 5 prefectures with complete data (2007-2025)
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
├── api_data/                  # Raw API responses and reports
├── data/                      # Processed CSV files
└── raw_data/                  # Legacy data files
```

## 🏗️ System Architecture

```
MLIT API → Data Fetching → Processing → Chart Generation → Frontend Integration
    ↓           ↓            ↓              ↓                   ↓
Raw JSON → Transformed → CSV Files → 3,800+ Charts → Website Display
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
| 東京 (Tokyo) | 13 | 460,456 | 59 | ✅ Complete |
| 千葉 (Chiba) | 12 | 163,861 | 59 | ✅ Complete |
| 神奈川 (Kanagawa) | 14 | 284,638 | 58 | ✅ Complete |
| 大阪 (Osaka) | 27 | 269,015 | 72 | ✅ Complete |
| 愛知 (Aichi) | 23 | 151,936 | 69 | ✅ Complete |

**Total**: 1,329,906 real estate transactions

### Time Period
- **Data Range**: 2007-2025 (Q1)
- **Current Status**: 2025 data includes January-March only
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
- **2025 data notice**: Clear indication of Q1-only data

### Chart Output
- **Total Charts Generated**: 3,804 charts
- **Format**: PNG, 12x8 inches, 150 DPI
- **Languages**: Japanese (_jp) and English (_en) versions
- **Location**: `../../frontend/img/trend/house/`

### Naming Convention
```
{prefecture}_{area}_{room_type}_{language}.png

Examples:
- aichi_名古屋市千種区_ALL_jp.png
- aichi_名古屋市千種区_ALL_en.png
- tokyo_千代田区_３ＬＤＫ_jp.png
```

## 🔧 Recent Improvements (2025-09-13)

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
- **2025 Integration**: Successfully integrated Q1 2025 data across all prefectures
- **Coverage Analysis**: Automated reporting of data limitations
- **User Communication**: Added notices to all HTML files about Q1-only 2025 data

## 💻 Usage Examples

### Generate Charts for All Prefectures
```python
from update_pipeline import HouseTrendUpdater

# Initialize the system
updater = HouseTrendUpdater()

# Process in manageable batches
prefectures = ['tokyo', 'chiba', 'kanagawa', 'osaka', 'aichi']
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

### Latest Complete Run (2025-09-13)
- **Duration**: ~4 hours (batch processing)
- **Charts Generated**: 3,804 total
- **Success Rate**: 100% (no crashes)
- **Data Processed**: 1.3M+ transactions
- **Prefectures Completed**: 5/5

### Breakdown by Prefecture
| Prefecture | Areas | Charts | Processing Time |
|------------|-------|--------|----------------|
| Tokyo | 59 | 708 | ~45 minutes |
| Chiba | 59 | 708 | ~45 minutes |
| Kanagawa | 58 | 696 | ~43 minutes |
| Osaka | 72 | 864 | ~54 minutes |
| Aichi | 69 | 828 | ~52 minutes |

## 🛠️ Installation & Setup

### Requirements
```bash
pip install pandas numpy matplotlib japanize-matplotlib requests python-dotenv
```

### Environment Configuration
Create `.env` file:
```
Ocp-Apim-Subscription-Key="your_mlit_api_key_here"
```

### Directory Structure Setup
Ensure the following directories exist:
```
backend/japan-house-trend/api_data/     # API responses
backend/japan-house-trend/data/         # Processed CSV files
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

**3. 2025 Data Appears Low**
- **Status**: ✅ Expected behavior
- **Explanation**: 2025 includes only Q1 (Jan-Mar) data
- **User Notice**: Added to all HTML files

**4. Japanese Font Issues**
- **Solution**: Ensure `japanize-matplotlib` is installed
- **Note**: Charts generate correctly despite font warnings

## 📝 Data Quality & Validation

### Automated Checks
- **Data Completeness**: Validates all prefecture data loaded
- **Year Coverage**: Confirms 2007-2025 range
- **Chart Generation**: Counts and verifies all output files
- **Error Tracking**: Comprehensive logging of any failures

### 2025 Data Limitations
- **Coverage**: Q1 only (January-March 2025)
- **Impact**: Transaction counts appear lower (10-15% of annual volume)
- **Communication**: Clear notices added to user interface
- **Expected**: Normal due to government data release schedule

## 🔄 Maintenance

### Regular Updates
1. **Quarterly Data Refresh**: When MLIT releases new quarterly data
2. **Chart Regeneration**: Run full update to incorporate new data
3. **Frontend Sync**: Ensure HTML files reflect current data status
4. **Performance Monitoring**: Track processing times and success rates

### Quality Assurance
- Review completion reports in `api_data/` directory
- Verify chart counts match expected totals (317 areas × 6 room types × 2 languages)
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

- ✅ **Complete Data Integration**: 2025 Q1 data across all prefectures
- ✅ **System Stability**: 100% success rate with batch processing
- ✅ **Chart Quality**: Professional formatting with clean numbers and Japanese localization
- ✅ **Bilingual Support**: Full Japanese and English chart generation
- ✅ **User Experience**: Clear data limitation notices and responsive modal display
- ✅ **Performance**: Efficient batch processing preventing system crashes

---

**Last Updated**: 2025-09-14
**System Status**: ✅ Fully Operational
**Data Status**: 2007-2025 Q1 Complete
**Chart Status**: 3,804 charts generated and deployed