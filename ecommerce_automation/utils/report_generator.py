import sqlite3
from datetime import datetime
import json
import os
import plotly.graph_objects as go
from jinja2 import Template
import glob
from pathlib import Path

class TestReport:
    def __init__(self, db_file="test_results.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    def get_test_stats(self):
        """Get overall test statistics"""
        self.cursor.execute('''
        SELECT 
            COUNT(*) as total_runs,
            SUM(total_tests) as total_tests,
            SUM(passed_tests) as passed_tests,
            SUM(failed_tests) as failed_tests
        FROM test_runs
        WHERE start_time >= date('now', '-7 days')
        ''')
        return self.cursor.fetchone()

    def get_failure_analysis(self):
        """Get failure analysis"""
        self.cursor.execute('''
        SELECT 
            test_name,
            COUNT(*) as failure_count,
            error_message
        FROM test_results
        WHERE status = 'failed'
        AND timestamp >= datetime('now', '-7 days')
        GROUP BY test_name
        ORDER BY failure_count DESC
        LIMIT 5
        ''')
        return self.cursor.fetchall()

    def get_test_durations(self):
        """Get test execution durations"""
        self.cursor.execute('''
        SELECT 
            test_name,
            AVG(execution_time) as avg_time,
            MIN(execution_time) as min_time,
            MAX(execution_time) as max_time
        FROM test_results
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY test_name
        ORDER BY avg_time DESC
        LIMIT 10
        ''')
        return self.cursor.fetchall()

    def generate_html_report(self):
        """Generate HTML report"""
        stats = self.get_test_stats()
        failures = self.get_failure_analysis()
        durations = self.get_test_durations()
        
        # Create bar chart for test durations
        fig = go.Figure()
        test_names = [d[0] for d in durations]
        avg_times = [d[1] for d in durations]
        
        fig.add_trace(go.Bar(
            x=test_names,
            y=avg_times,
            name='Average Duration (s)'
        ))
        
        fig.update_layout(
            title='Test Execution Duration',
            xaxis_title='Test Name',
            yaxis_title='Duration (seconds)'
        )
        
        # Generate HTML report using template
        template = Template('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Automation Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
                .stat-box { 
                    display: inline-block; 
                    width: 200px; 
                    margin: 10px;
                    padding: 15px;
                    text-align: center;
                    border: 1px solid #ddd;
                }
                .failure-item {
                    margin: 10px 0;
                    padding: 10px;
                    border-left: 3px solid #ff4444;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Test Automation Report</h1>
                <div class="section">
                    <h2>Test Statistics (Last 7 Days)</h2>
                    <div class="stat-box">
                        <h3>Total Runs</h3>
                        <p>{{ stats[0] }}</p>
                    </div>
                    <div class="stat-box">
                        <h3>Total Tests</h3>
                        <p>{{ stats[1] }}</p>
                    </div>
                    <div class="stat-box">
                        <h3>Passed</h3>
                        <p style="color: green;">{{ stats[2] }}</p>
                    </div>
                    <div class="stat-box">
                        <h3>Failed</h3>
                        <p style="color: red;">{{ stats[3] }}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Test Duration Analysis</h2>
                    <div id="durationChart"></div>
                </div>

                <div class="section">
                    <h2>Top Failures</h2>
                    {% for failure in failures %}
                    <div class="failure-item">
                        <h3>{{ failure[0] }}</h3>
                        <p>Failed {{ failure[1] }} times</p>
                        <p>Error: {{ failure[2] }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <script>
                {{ plotly_chart }}
            </script>
        </body>
        </html>
        ''')
        
        return template.render(
            stats=stats,
            failures=failures,
            plotly_chart=fig.to_html(full_html=False)
        )

    def save_report(self, format='html'):
        """Save the report in the specified format"""
        if format == 'html':
            report = self.generate_html_report()
            output_file = 'test_report.html'
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(output_file, 'w') as f:
            f.write(report)
        return output_file

def generate_test_report(format='html'):
    """Main function to generate and save the test report"""
    report = TestReport()
    return report.save_report(format)

if __name__ == '__main__':
    generate_test_report()
