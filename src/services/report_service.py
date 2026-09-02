"""
Report Service

Generates comprehensive reports and statements.
"""

from typing import Dict, List, Tuple, Any
from datetime import datetime, date, timedelta
from src.database.connection import get_db
from src.logger import setup_logger

logger = setup_logger(__name__)


class ReportService:
    """
    Report generation service.

    Generates:
        - Daily collection reports
        - Monthly summaries
        - Farmer statements
        - Customer statements
        - Outstanding reports
    """

    @staticmethod
    def get_daily_report(report_date: str) -> Tuple[bool, str, Dict]:
        """
        Generate daily collection report.

        Args:
            report_date: Date (YYYY-MM-DD)

        Returns:
            Tuple of (success, message, report_data)
        """
        try:
            db = get_db()

            # Morning collection
            morning = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as entries,
                    SUM(litres) as total_litres,
                    AVG(fat) as avg_fat,
                    SUM(total_amount) as total_amount
                FROM milk_purchases
                WHERE date = ? AND shift = 'Morning'
                GROUP BY milk_type
                """,
                (report_date,),
            )

            # Evening collection
            evening = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as entries,
                    SUM(litres) as total_litres,
                    AVG(fat) as avg_fat,
                    SUM(total_amount) as total_amount
                FROM milk_purchases
                WHERE date = ? AND shift = 'Evening'
                GROUP BY milk_type
                """,
                (report_date,),
            )

            # Daily sales
            sales = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as entries,
                    SUM(litres) as total_litres,
                    SUM(total_amount) as total_amount
                FROM retail_sales
                WHERE date = ?
                GROUP BY milk_type
                """,
                (report_date,),
            )

            report = {
                "date": report_date,
                "morning": [dict(row) for row in morning],
                "evening": [dict(row) for row in evening],
                "sales": [dict(row) for row in sales],
            }

            logger.info(f"Daily report generated: {report_date}")
            return True, "Report generated", report
        except Exception as e:
            logger.error(f"Failed to generate daily report: {e}")
            return False, "Failed to generate report", {}

    @staticmethod
    def get_monthly_report(year: int, month: int) -> Tuple[bool, str, Dict]:
        """
        Generate monthly summary report.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Tuple of (success, message, report_data)
        """
        try:
            db = get_db()
            month_str = f"{year}-{month:02d}"

            # Total milk purchased
            purchases = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as total_entries,
                    SUM(litres) as total_litres,
                    AVG(fat) as avg_fat,
                    AVG(rate) as avg_rate,
                    SUM(total_amount) as total_amount
                FROM milk_purchases
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY milk_type
                """,
                (month_str,),
            )

            # Total sales
            sales = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as total_entries,
                    SUM(litres) as total_litres,
                    SUM(total_amount) as total_amount
                FROM retail_sales
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY milk_type
                """,
                (month_str,),
            )

            # Total payments to farmers
            farmer_payments = db.execute_query(
                """
                SELECT
                    SUM(amount) as total_payments,
                    COUNT(*) as payment_count
                FROM farmer_payments
                WHERE strftime('%Y-%m', date) = ?
                """,
                (month_str,),
            )

            report = {
                "period": month_str,
                "purchases": [dict(row) for row in purchases],
                "sales": [dict(row) for row in sales],
                "payments": dict(farmer_payments[0]) if farmer_payments else {},
            }

            logger.info(f"Monthly report generated: {month_str}")
            return True, "Report generated", report
        except Exception as e:
            logger.error(f"Failed to generate monthly report: {e}")
            return False, "Failed to generate report", {}

    @staticmethod
    def get_outstanding_report() -> Tuple[bool, str, List[Dict]]:
        """
        Generate outstanding payments report.

        Returns:
            Tuple of (success, message, outstanding_list)
        """
        try:
            db = get_db()

            # Get all farmers with outstanding
            outstanding = db.execute_query(
                """
                SELECT
                    f.code,
                    f.name,
                    f.phone,
                    COALESCE(SUM(mp.total_amount), 0) as purchase_amount,
                    COALESCE(SUM(fp.amount), 0) as payment_amount,
                    COALESCE(SUM(mp.total_amount), 0) - COALESCE(SUM(fp.amount), 0) as outstanding
                FROM farmers f
                LEFT JOIN milk_purchases mp ON f.code = mp.farmer_code
                LEFT JOIN farmer_payments fp ON f.code = fp.farmer_code
                WHERE f.is_active = 1
                GROUP BY f.code
                HAVING outstanding > 0
                ORDER BY outstanding DESC
                """
            )

            report = [dict(row) for row in outstanding]
            logger.info(f"Outstanding report generated: {len(report)} entries")
            return True, f"Found {len(report)} pending payments", report
        except Exception as e:
            logger.error(f"Failed to generate outstanding report: {e}")
            return False, "Failed to generate report", []
