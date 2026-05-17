"""
MLIT API Data Update Pipeline
Complete pipeline to fetch data from MLIT API and generate updated charts
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.ticker import MaxNLocator, FuncFormatter
from datetime import datetime
import json

from api_client import MLITAPIClient
from data_transformer import APIDataTransformer

class HouseTrendUpdater:
    def __init__(self):
        """Initialize the house trend updater"""
        self.client = MLITAPIClient()
        self.transformer = APIDataTransformer()
        
        # Room types for chart generation (matching original system)
        self.room_types = ["ALL", "４ＬＤＫ", "３ＬＤＫ", "２ＬＤＫ", "１ＬＤＫ", "１Ｋ"]
        
        # Output directories
        self.api_data_dir = "api_data"
        self.processed_data_dir = "data"
        self.chart_output_dir = "../../../heysho/frontend/img/trend/house"
        
        # Ensure directories exist
        os.makedirs(self.api_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
        # Progress tracking
        self.progress = {
            'start_time': None,
            'prefectures_completed': 0,
            'total_records': 0,
            'charts_generated': 0,
            'errors': []
        }
    
    def run_full_update(self, start_year: int = 2007, end_year: int = 2024, 
                       test_mode: bool = False):
        """
        Run the complete data update pipeline
        
        Args:
            start_year: Starting year for data fetch
            end_year: Ending year for data fetch  
            test_mode: If True, only process Tokyo with limited data
        """
        self.progress['start_time'] = datetime.now()
        
        print("🚀 MLIT API Data Update Pipeline Started")
        print(f"Time range: {start_year}-{end_year}")
        print(f"Test mode: {test_mode}")
        print("=" * 60)
        
        try:
            # Step 1: Fetch data from API
            if test_mode:
                print(f"\n📡 STEP 1: Fetching TEST data (Tokyo only, {start_year}-{end_year})")
                api_data = {'tokyo': self.client.fetch_prefecture_data('13', start_year, end_year)}
            else:
                print(f"\n📡 STEP 1: Fetching data from MLIT API")
                api_data = self.client.fetch_all_prefectures(start_year, end_year)
            
            # Step 2: Transform and save data
            print(f"\n🔄 STEP 2: Transforming data")
            prefecture_dataframes = self.transform_and_save_data(api_data)
            
            # Step 3: Generate charts
            print(f"\n📊 STEP 3: Generating charts")
            self.generate_all_charts(prefecture_dataframes, test_mode)
            
            # Step 4: Generate completion report
            print(f"\n📋 STEP 4: Generating completion report")
            self.generate_completion_report()
            
            print(f"\n✅ PIPELINE COMPLETE!")
            
        except Exception as e:
            print(f"\n❌ PIPELINE FAILED: {e}")
            self.progress['errors'].append(str(e))
            raise
    
    def transform_and_save_data(self, api_data: dict) -> dict:
        """
        Transform API data and save to CSV files
        
        Args:
            api_data: Dictionary of prefecture data from API
            
        Returns:
            Dictionary of prefecture DataFrames
        """
        prefecture_dataframes = {}
        
        for prefecture, records in api_data.items():
            if records:
                print(f"\nProcessing {prefecture}...")
                
                # Transform data
                df = self.transformer.transform_api_data(records)
                
                if not df.empty:
                    # Save to CSV
                    csv_filename = f"{self.processed_data_dir}/{prefecture}_api_processed.csv"
                    df.to_csv(csv_filename, index=False, encoding='utf-8')
                    print(f"💾 Saved {len(df)} records to {csv_filename}")
                    
                    prefecture_dataframes[prefecture] = df
                    self.progress['total_records'] += len(df)
                else:
                    print(f"⚠️ No valid data for {prefecture}")
                    prefecture_dataframes[prefecture] = pd.DataFrame()
            else:
                print(f"⚠️ No API data for {prefecture}")
                prefecture_dataframes[prefecture] = pd.DataFrame()
            
            self.progress['prefectures_completed'] += 1
        
        return prefecture_dataframes
    
    def generate_charts_for_prefecture(self, prefecture: str, df: pd.DataFrame, 
                                     test_mode: bool = False):
        """
        Generate all charts for a single prefecture
        
        Args:
            prefecture: Prefecture name (english)
            df: DataFrame with transaction data
            test_mode: If True, limit chart generation for testing
            
        Returns:
            Number of charts generated
        """
        if df.empty:
            print(f"  ⚠️ No data for {prefecture}, skipping charts")
            return 0
        
        areas = df['市区町村名'].unique()
        charts_generated = 0
        
        # In test mode, limit to first 3 areas
        if test_mode:
            areas = areas[:3]
            print(f"  🧪 Test mode: Processing {len(areas)} areas for {prefecture}")
        
        print(f"  📊 Generating charts for {len(areas)} areas in {prefecture}")
        
        for area in areas:
            for room_type in self.room_types:
                try:
                    self.generate_single_chart(
                        prefecture, area, room_type, df, language='jp'
                    )
                    self.generate_single_chart(
                        prefecture, area, room_type, df, language='en'
                    )
                    charts_generated += 2
                    self.progress['charts_generated'] += 2
                    
                except Exception as e:
                    error_msg = f"Chart generation failed: {prefecture}_{area}_{room_type} - {e}"
                    self.progress['errors'].append(error_msg)
                    print(f"    ❌ {error_msg}")
        
        return charts_generated

    def generate_charts_batch(self, prefecture: str, df: pd.DataFrame,
                             areas_batch: list, batch_id: str = ""):
        """
        Generate charts for a specific batch of areas in a prefecture

        Args:
            prefecture: Prefecture name (english)
            df: DataFrame with transaction data
            areas_batch: List of specific areas to process
            batch_id: Identifier for this batch (for logging)

        Returns:
            Number of charts generated
        """
        if df.empty:
            print(f"  ⚠️ No data for {prefecture}, skipping charts")
            return 0

        charts_generated = 0
        batch_info = f"batch {batch_id}" if batch_id else f"{len(areas_batch)} areas"
        print(f"  📊 Processing {batch_info} for {prefecture}")

        for area in areas_batch:
            print(f"    🏠 Generating charts for {area}")
            for room_type in self.room_types:
                try:
                    # Generate both Japanese and English versions
                    self.generate_single_chart(
                        prefecture, area, room_type, df, language='jp'
                    )
                    self.generate_single_chart(
                        prefecture, area, room_type, df, language='en'
                    )
                    charts_generated += 2

                except Exception as e:
                    error_msg = f"Chart generation failed: {prefecture}_{area}_{room_type} - {e}"
                    print(f"    ❌ {error_msg}")

        print(f"  ✅ Batch complete: {charts_generated} charts generated for {prefecture}")
        return charts_generated

    def generate_single_chart(self, prefecture: str, area: str, room_type: str,
                            df: pd.DataFrame, language: str = 'jp'):
        """
        Generate a single chart for specific area and room type
        
        Args:
            prefecture: Prefecture name
            area: Area name  
            room_type: Room type
            df: DataFrame with data
            language: 'jp' or 'en'
        """
        # Filter data by area and room type
        if room_type != "ALL":
            df_filtered = df[(df['市区町村名'] == area) & (df['間取り'] == room_type)]
        else:
            df_filtered = df[df['市区町村名'] == area]
        
        if len(df_filtered) == 0:
            return  # Skip if no data
        
        # Group by year to calculate average price and count
        yearly_avg_price = df_filtered.groupby('取引時期（年）')['取引価格（総額）'].mean()
        yearly_count = df_filtered.groupby('取引時期（年）')['取引価格（総額）'].count()
        
        # Create chart
        plt.figure(figsize=(12, 8))
        ax1 = plt.gca()
        
        # Set legend labels based on language
        price_label = 'Average Price' if language == 'en' else '平均取引価格'
        
        ax1.plot(yearly_avg_price.index, yearly_avg_price.values, 
                color='red', label=price_label, linewidth=2, marker='o')
        ax1.set_xlabel('Year' if language == 'en' else 'Year')
        
        if language == 'jp':
            ax1.set_ylabel('平均取引価格', color='darkred')
            title = f'{area} - {room_type}の平均取引価格と取引件数の推移'
        else:
            ax1.set_ylabel('Average Transaction Price', color='darkred')
            title = f'{area} - The trend of the average transaction price and the number of transactions for {room_type}'
        
        ax1.tick_params(axis='y', labelcolor='darkred')
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Set y-axis limits dynamically based on actual data
        price_max = max(yearly_avg_price.values) * 1.1  # Add 10% padding
        count_max = max(yearly_count.values) * 1.2      # Add 20% padding
        
        ax1.set_ylim(0, price_max)
        ax2_ylim = count_max
        
        # Format y-axis to show full numbers (no scientific notation)
        def format_func(value, tick_number):
            return f'{int(value):,}'
        
        ax1.yaxis.set_major_formatter(FuncFormatter(format_func))
        
        # Secondary axis for transaction count
        ax2 = ax1.twinx()
        
        # Set transaction count label based on language
        count_label = 'Transaction Count' if language == 'en' else '取引回数'
        
        ax2.bar(yearly_count.index, yearly_count.values, 
               color='lightblue', label=count_label, width=0.4, alpha=0.5)
        
        if language == 'jp':
            ax2.set_ylabel('取引回数', color='darkblue')
        else:
            ax2.set_ylabel('Number of transactions', color='darkblue')
            
        ax2.tick_params(axis='y', labelcolor='darkblue')
        ax2.set_ylim(0, ax2_ylim)
        
        plt.title(title, fontsize=14, pad=20)
        plt.grid(True, alpha=0.3)
        
        # Legend
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        
        # Save chart
        filename = f'{prefecture}_{area}_{room_type}_{language}.png'
        filepath = os.path.join(self.chart_output_dir, filename)
        
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def generate_all_charts(self, prefecture_dataframes: dict, test_mode: bool = False):
        """
        Generate all charts for all prefectures
        
        Args:
            prefecture_dataframes: Dictionary of prefecture DataFrames
            test_mode: If True, limit chart generation for testing
        """
        total_prefectures = len(prefecture_dataframes)
        
        for i, (prefecture, df) in enumerate(prefecture_dataframes.items(), 1):
            print(f"\n📊 Charts {i}/{total_prefectures}: {prefecture.upper()}")
            self.generate_charts_for_prefecture(prefecture, df, test_mode)
    
    def generate_completion_report(self):
        """Generate a completion report"""
        end_time = datetime.now()
        duration = end_time - self.progress['start_time']
        
        report = {
            'completion_time': end_time.isoformat(),
            'duration_minutes': duration.total_seconds() / 60,
            'prefectures_completed': self.progress['prefectures_completed'],
            'total_records_processed': self.progress['total_records'],
            'charts_generated': self.progress['charts_generated'],
            'errors_count': len(self.progress['errors']),
            'errors': self.progress['errors']
        }
        
        # Save report
        report_filename = f"api_data/completion_report_{end_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Print summary
        print(f"\n📋 COMPLETION REPORT")
        print(f"Duration: {duration.total_seconds()/60:.1f} minutes")
        print(f"Total records: {self.progress['total_records']:,}")
        print(f"Charts generated: {self.progress['charts_generated']:,}")
        print(f"Errors: {len(self.progress['errors'])}")
        print(f"Report saved: {report_filename}")
        
        if self.progress['errors']:
            print(f"\n⚠️ ERRORS ENCOUNTERED:")
            for error in self.progress['errors'][:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.progress['errors']) > 10:
                print(f"  ... and {len(self.progress['errors']) - 10} more errors")

if __name__ == "__main__":
    # Run the pipeline
    updater = HouseTrendUpdater()
    
    # Test with limited data first
    print("Running in TEST mode (Tokyo only, 2024 data)")
    updater.run_full_update(start_year=2024, end_year=2024, test_mode=True)