"""
Production Script: Full MLIT API Data Update
Run this script to update all house-trend data and regenerate all charts
"""

from update_pipeline import HouseTrendUpdater
import sys

def main():
    """Run the complete production update"""
    
    print("🏠 MLIT Real Estate Data - FULL PRODUCTION UPDATE")
    print("=" * 60)
    print("This will:")
    print("• Fetch data for 6 prefectures (2007-2025, through 2025 Q4)")
    print("• Regenerate all house-trend charts with data through December 2025")
    print("• Take approximately 30-60 minutes")
    print("• Update all frontend images")
    print("=" * 60)
    
    # Confirm before proceeding
    confirm = input("\nProceed with full update? (yes/no): ").lower().strip()
    
    if confirm not in ['yes', 'y']:
        print("❌ Update cancelled by user")
        return
    
    try:
        # Initialize updater
        updater = HouseTrendUpdater()
        
        # Run full update (2007-2025, all prefectures)
        print("\n🚀 Starting FULL production update...")
        updater.run_full_update(
            start_year=2007, 
            end_year=2025, 
            test_mode=False
        )
        
        print("\n✅ FULL UPDATE COMPLETED SUCCESSFULLY!")
        print("All charts have been updated in the frontend directory.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Update interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Update failed: {e}")
        print("Check the error logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
