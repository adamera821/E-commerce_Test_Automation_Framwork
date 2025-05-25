import sqlite3
from datetime import datetime

class TestResultsDB:
    def __init__(self, db_file="test_results.db"):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create test_runs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time DATETIME,
            end_time DATETIME,
            total_tests INTEGER,
            passed_tests INTEGER,
            failed_tests INTEGER
        )''')

        # Create test_results table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            test_name TEXT,
            status TEXT,
            error_message TEXT,
            screenshot_path TEXT,
            execution_time FLOAT,
            timestamp DATETIME,
            FOREIGN KEY (run_id) REFERENCES test_runs(id)
        )''')

        conn.commit()
        conn.close()

    def start_test_run(self):
        """Record the start of a test run"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO test_runs (start_time, total_tests, passed_tests, failed_tests)
        VALUES (?, 0, 0, 0)
        ''', (datetime.now(),))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return run_id

    def end_test_run(self, run_id, total, passed, failed):
        """Update test run with final results"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE test_runs 
        SET end_time = ?, total_tests = ?, passed_tests = ?, failed_tests = ?
        WHERE id = ?
        ''', (datetime.now(), total, passed, failed, run_id))
        
        conn.commit()
        conn.close()

    def save_test_result(self, run_id, test_name, status, error_message=None, screenshot_path=None, execution_time=0):
        """Save individual test result"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO test_results 
        (run_id, test_name, status, error_message, screenshot_path, execution_time, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (run_id, test_name, status, error_message, screenshot_path, execution_time, datetime.now()))
        
        conn.commit()
        conn.close()

    def get_test_run_summary(self, run_id):
        """Get summary of a test run"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM test_runs WHERE id = ?
        ''', (run_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result

    def get_test_results(self, run_id):
        """Get all test results for a specific run"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM test_results WHERE run_id = ?
        ''', (run_id,))
        
        results = cursor.fetchall()
        conn.close()
        return results
