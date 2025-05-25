import json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class LogAnalyzer:
    """Analyzer for test execution logs"""

    def __init__(self, log_dir):
        self.log_dir = Path(log_dir)
        self.test_logs = self.log_dir / 'test_execution' / 'test.log'

    def parse_logs(self, days=7):
        """Parse test execution logs for the specified number of days"""
        logs = []
        cutoff_date = datetime.now() - timedelta(days=days)

        with open(self.test_logs) as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    log_date = datetime.fromisoformat(log_entry['timestamp'])
                    if log_date >= cutoff_date:
                        logs.append(log_entry)
                except (json.JSONDecodeError, KeyError):
                    continue

        return pd.DataFrame(logs)

    def analyze_test_duration(self):
        """Analyze test execution duration statistics"""
        df = self.parse_logs()
        duration_stats = df[df['message'].str.contains('Test completed', na=False)]
        
        # Create duration analysis chart
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=duration_stats['duration'],
            name='Test Duration'
        ))
        fig.update_layout(
            title='Test Duration Distribution',
            yaxis_title='Duration (seconds)'
        )
        return fig

    def analyze_failure_patterns(self):
        """Analyze test failure patterns"""
        df = self.parse_logs()
        failures = df[
            (df['level'] == 'ERROR') | 
            (df['message'].str.contains('failed', case=False, na=False))
        ]
        
        failure_counts = failures.groupby('module')['message'].count()
        
        # Create failure pattern chart
        fig = px.bar(
            x=failure_counts.index,
            y=failure_counts.values,
            title='Test Failures by Module'
        )
        return fig

    def generate_daily_report(self):
        """Generate daily test execution report"""
        df = self.parse_logs(days=1)
        
        total_tests = len(df[df['message'].str.contains('Starting test', na=False)])
        failed_tests = len(df[df['message'].str.contains('failed', case=False, na=False)])
        passed_tests = len(df[df['message'].str.contains('passed', case=False, na=False)])
        
        avg_duration = df[df['duration'].notna()]['duration'].mean()
        
        report = {
            'date': datetime.now().date().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'avg_duration': avg_duration
        }
        
        return report

    def analyze_step_performance(self):
        """Analyze performance of individual test steps"""
        df = self.parse_logs()
        steps = df[df['message'].str.contains('Test step:', na=False)]
        
        step_durations = []
        current_step = None
        start_time = None
        
        for _, row in steps.iterrows():
            if 'started' in row['message']:
                current_step = row['message'].split(':')[1].strip().split('-')[0].strip()
                start_time = datetime.fromisoformat(row['timestamp'])
            elif 'completed' in row['message'] and current_step and start_time:
                end_time = datetime.fromisoformat(row['timestamp'])
                duration = (end_time - start_time).total_seconds()
                step_durations.append({
                    'step': current_step,
                    'duration': duration
                })
                
        step_df = pd.DataFrame(step_durations)
        
        # Create step performance chart
        fig = px.box(
            step_df,
            x='step',
            y='duration',
            title='Test Step Duration Distribution'
        )
        return fig

    def export_analysis(self, output_dir):
        """Export log analysis results"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate and save all analyses
        self.analyze_test_duration().write_html(
            output_path / 'test_duration.html'
        )
        self.analyze_failure_patterns().write_html(
            output_path / 'failure_patterns.html'
        )
        self.analyze_step_performance().write_html(
            output_path / 'step_performance.html'
        )
        
        # Save daily report
        daily_report = self.generate_daily_report()
        with open(output_path / 'daily_report.json', 'w') as f:
            json.dump(daily_report, f, indent=2)

def analyze_logs():
    """Command-line interface for log analysis"""
    analyzer = LogAnalyzer('logs')
    analyzer.export_analysis('reports/log_analysis')
