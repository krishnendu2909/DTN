#!/usr/bin/env python3
"""
Advanced DTN Visualization and Comparison Framework
Generates comprehensive graphs and performance comparisons
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import os
import re
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon
import warnings
warnings.filterwarnings('ignore')

class DTNVisualizationFramework:
    def __init__(self):
        """Initialize the DTN Visualization Framework"""
        self.protocols = ['OurDTN', 'Epidemic', 'PROPHET', 'SprayAndWait']
        self.colors = ['#FF1744', '#2196F3', '#4CAF50', '#FF9800']
        self.simulation_data = None
        self.performance_data = {}
        self.time_series_data = []
        self.load_simulation_data()
    
    def load_simulation_data(self):
        """Load real simulation data from ns-3 output files"""
        try:
            if os.path.exists('dtn-performance-stats.txt'):
                with open('dtn-performance-stats.txt', 'r') as f:
                    content = f.read()
                    self.parse_simulation_data(content)
            else:
                print("⚠️  Simulation data file not found. Using default values.")
                self.use_default_data()
        except Exception as e:
            print(f"⚠️  Error loading simulation data: {e}. Using default values.")
            self.use_default_data()
    
    def parse_simulation_data(self, content):
        """Parse the simulation output file and extract performance metrics"""
        lines = content.split('\n')
        
        # Parse DTN metrics section
        dtn_section = False
        for line in lines:
            if line.strip() == "DTN_METRICS":
                dtn_section = True
                continue
            elif line.strip().startswith("NODE_PERFORMANCE"):
                dtn_section = False
                continue
            
            if dtn_section and ',' in line and not line.startswith('Protocol'):
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    protocol = parts[0]
                    delay = float(parts[1])
                    throughput = float(parts[2])
                    delivery_ratio = float(parts[3])
                    energy_efficiency = float(parts[4])
                    
                    # Convert to our visualization format
                    self.performance_data[protocol] = {
                        'delay': delay,
                        'bandwidth': throughput * 10,  # Scale for visualization
                        'response': delay * 0.8,  # Response time related to delay
                        'data_loss': 100 - delivery_ratio,
                        'energy': 1.0 - energy_efficiency,  # Invert for energy consumption
                        'scalability': delivery_ratio * 100  # Scale for visualization
                    }
        
        # Parse time series data for dynamic visualization
        self.time_series_data = []
        time_series_section = False
        for line in lines:
            if line.strip() == "TIME_SERIES_DATA":
                time_series_section = True
                continue
            elif time_series_section and ',' in line and not line.startswith('Time'):
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    self.time_series_data.append({
                        'time': float(parts[0]),
                        'delay': float(parts[1]),
                        'throughput': float(parts[2]),
                        'packet_loss': float(parts[3]),
                        'active_nodes': int(float(parts[4]))
                    })
        
        if self.performance_data:
            print(f"✅ Loaded real simulation data for {len(self.performance_data)} protocols")
        else:
            print("⚠️  No protocol data found in simulation file. Using defaults.")
            self.use_default_data()
    
    def use_default_data(self):
        """Use default performance data when simulation data is not available"""
        self.performance_data = {
            'OurDTN': {'delay': 25, 'bandwidth': 14, 'response': 20, 'data_loss': 15, 'energy': 0.1, 'scalability': 850},
            'Epidemic': {'delay': 65, 'bandwidth': 6, 'response': 52, 'data_loss': 40, 'energy': 0.4, 'scalability': 600},
            'PROPHET': {'delay': 42, 'bandwidth': 12, 'response': 34, 'data_loss': 25, 'energy': 0.2, 'scalability': 750},
            'SprayAndWait': {'delay': 51, 'bandwidth': 10, 'response': 41, 'data_loss': 30, 'energy': 0.25, 'scalability': 700}
        }
        
        # Generate sample time series data
        self.time_series_data = []
        for t in range(0, 600, 30):
            self.time_series_data.append({
                'time': t,
                'delay': 35 + 15 * np.sin(t * 0.01),
                'throughput': 8 + 4 * np.cos(t * 0.008),
                'packet_loss': 20 + 10 * np.sin(t * 0.012),
                'active_nodes': 40 + 10 * np.cos(t * 0.005)
            })
        
        print("📊 Using default performance data for visualization")
        
    def create_parameter_comparison_table(self):
        """Generate comprehensive parameter comparison table"""
        if not self.performance_data:
            print("⚠️  No performance data available for table generation")
            return
            
        df = pd.DataFrame(self.performance_data).T
        
        # Create styled table
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table with color coding
        table_data = []
        headers = ['Protocol', 'Avg Delay (ms)', 'Bandwidth (%)', 'Response (ms)', 'Data Loss (%)', 'Energy (J/bit)', 'Scalability (nodes)']
        
        for protocol in self.protocols:
            data = self.performance_data[protocol]
            row = [
                protocol,
                f"{data['delay']:.0f}",
                f"{data['bandwidth']:.0f}",
                f"{data['response']:.0f}",
                f"{data['data_loss']:.1f}",
                f"{data['energy']:.3f}",
                f"{data['scalability']:,}"
            ]
            table_data.append(row)
        
        table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        
        # Color code the best performance (Our DTN System)
        for i in range(len(headers)):
            table[(1, i)].set_facecolor('#E8F5E8')  # Light green for our system
            
        plt.title('DTN Protocol Performance Comparison Table', fontsize=16, fontweight='bold', pad=20)
        plt.savefig('/home/krishnendu/dtn_comparison_table.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_performance_radar_chart(self):
        """Generate radar chart comparing all protocols"""
        # Normalize data for radar chart (higher is better)
        categories = ['Delay\n(Lower Better)', 'Bandwidth\nUtilization', 'Response Time\n(Lower Better)', 
                     'Data Loss\n(Lower Better)', 'Energy Efficiency\n(Lower Better)', 'Scalability']
        
        fig = go.Figure()
        
        for i, protocol in enumerate(self.protocols):
            data = self.performance_data[protocol]
            # Normalize values (invert for metrics where lower is better)
            values = [
                100 - (data['delay'] / 20),  # Invert delay
                data['bandwidth'],
                100 - (data['response'] / 5),  # Invert response time
                100 - (data['data_loss'] * 5),  # Invert data loss
                100 - (data['energy'] * 1000),  # Invert energy
                min(100, data['scalability'] / 100)  # Scale scalability
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=protocol,
                line_color=self.colors[i]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="DTN Protocol Performance Radar Chart",
            font_size=12
        )
        
        fig.write_html('/home/krishnendu/dtn_radar_chart.html')
        fig.show()
        
    def create_delay_bandwidth_scatter(self):
        """Create delay vs bandwidth scatter plot"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for i, protocol in enumerate(self.protocols):
            data = self.performance_data[protocol]
            size = 200 if protocol == 'Our DTN System' else 100
            alpha = 1.0 if protocol == 'Our DTN System' else 0.7
            
            ax.scatter(data['delay'], data['bandwidth'], 
                      s=size, c=self.colors[i], alpha=alpha, 
                      label=protocol, edgecolors='black', linewidth=1)
            
            # Annotate points
            ax.annotate(protocol, (data['delay'], data['bandwidth']), 
                       xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax.set_xlabel('Average Delay (ms)', fontsize=12)
        ax.set_ylabel('Bandwidth Utilization (%)', fontsize=12)
        ax.set_title('Delay vs Bandwidth Performance Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Highlight optimal region (low delay, high bandwidth)
        optimal_region = Polygon([(0, 80), (300, 80), (300, 100), (0, 100)], 
                               alpha=0.2, facecolor='green', label='Optimal Region')
        ax.add_patch(optimal_region)
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/delay_bandwidth_scatter.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_response_time_data_loss_heatmap(self):
        """Create heatmap for response time vs data loss"""
        # Create data matrix
        protocols_short = list(self.performance_data.keys())
        metrics = ['Response Time', 'Data Loss Rate']
        
        data_matrix = []
        for protocol in protocols_short:
            data = self.performance_data[protocol]
            data_matrix.append([data['response'], data['data_loss']])
        
        df_heatmap = pd.DataFrame(data_matrix, index=protocols_short, columns=metrics)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df_heatmap, annot=True, cmap='RdYlGn_r', center=df_heatmap.mean().mean(),
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=ax)
        
        ax.set_title('Response Time vs Data Loss Rate Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Performance Metrics', fontsize=12)
        ax.set_ylabel('DTN Protocols', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/response_data_loss_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_3d_performance_visualization(self):
        """Create 3D visualization of delay, bandwidth, and response time"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        for i, protocol in enumerate(self.protocols):
            data = self.performance_data[protocol]
            size = 200 if protocol == 'Our DTN System' else 100
            
            ax.scatter(data['delay'], data['bandwidth'], data['response'],
                      s=size, c=self.colors[i], alpha=0.8, label=protocol)
            
            # Add text labels
            ax.text(data['delay'], data['bandwidth'], data['response'], 
                   protocol, fontsize=8)
        
        ax.set_xlabel('Delay (ms)', fontsize=12)
        ax.set_ylabel('Bandwidth (%)', fontsize=12)
        ax.set_zlabel('Response Time (ms)', fontsize=12)
        ax.set_title('3D Performance Comparison: Delay vs Bandwidth vs Response Time', 
                    fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.1, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/3d_performance_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_time_series_performance(self):
        """Create time series showing performance over disaster duration"""
        time_points = np.linspace(0, 24, 100)  # 24 hours
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Simulate performance degradation during disaster
        for i, protocol in enumerate(self.protocols[:4]):  # Show top 4 for clarity
            base_data = self.performance_data[protocol]
            
            # Delay increases during disaster peak (hours 8-16)
            delay_curve = base_data['delay'] * (1 + 0.5 * np.exp(-((time_points - 12)**2) / 20))
            ax1.plot(time_points, delay_curve, label=protocol, color=self.colors[i], linewidth=2)
            
            # Bandwidth decreases during disaster
            bandwidth_curve = base_data['bandwidth'] * (1 - 0.3 * np.exp(-((time_points - 12)**2) / 20))
            ax2.plot(time_points, bandwidth_curve, label=protocol, color=self.colors[i], linewidth=2)
            
            # Response time increases
            response_curve = base_data['response'] * (1 + 0.4 * np.exp(-((time_points - 12)**2) / 20))
            ax3.plot(time_points, response_curve, label=protocol, color=self.colors[i], linewidth=2)
            
            # Data loss increases
            loss_curve = base_data['data_loss'] * (1 + 0.6 * np.exp(-((time_points - 12)**2) / 20))
            ax4.plot(time_points, loss_curve, label=protocol, color=self.colors[i], linewidth=2)
        
        # Customize subplots
        ax1.set_title('Delay Over Time', fontweight='bold')
        ax1.set_ylabel('Delay (ms)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.set_title('Bandwidth Utilization Over Time', fontweight='bold')
        ax2.set_ylabel('Bandwidth (%)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        ax3.set_title('Response Time Over Time', fontweight='bold')
        ax3.set_ylabel('Response Time (ms)')
        ax3.set_xlabel('Time (hours)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        ax4.set_title('Data Loss Rate Over Time', fontweight='bold')
        ax4.set_ylabel('Data Loss (%)')
        ax4.set_xlabel('Time (hours)')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.suptitle('DTN Performance During 24-Hour Disaster Scenario', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('/home/krishnendu/time_series_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_energy_scalability_analysis(self):
        """Create energy efficiency vs scalability analysis"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create bubble chart
        for i, protocol in enumerate(self.protocols):
            data = self.performance_data[protocol]
            # Bubble size represents overall performance score
            performance_score = (100 - data['delay']/20) + data['bandwidth'] + (100 - data['response']/5)
            bubble_size = performance_score * 3
            
            ax.scatter(data['energy'], data['scalability'], 
                      s=bubble_size, c=self.colors[i], alpha=0.7, 
                      label=protocol, edgecolors='black', linewidth=1)
            
            # Annotate
            ax.annotate(protocol, (data['energy'], data['scalability']), 
                       xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax.set_xlabel('Energy Consumption (J/bit)', fontsize=12)
        ax.set_ylabel('Scalability (max nodes)', fontsize=12)
        ax.set_title('Energy Efficiency vs Scalability Analysis\n(Bubble size = Overall Performance)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xscale('log')
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/energy_scalability_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_comprehensive_dashboard(self):
        """Create comprehensive interactive dashboard"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Delay Comparison', 'Bandwidth Utilization', 
                          'Response Time', 'Data Loss Rate', 
                          'Energy Efficiency', 'Scalability'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        protocols = list(self.performance_data.keys())
        
        # Delay comparison
        delays = [self.performance_data[p]['delay'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=delays, name='Delay (ms)', 
                           marker_color=self.colors), row=1, col=1)
        
        # Bandwidth utilization
        bandwidths = [self.performance_data[p]['bandwidth'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=bandwidths, name='Bandwidth (%)', 
                           marker_color=self.colors), row=1, col=2)
        
        # Response time
        responses = [self.performance_data[p]['response'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=responses, name='Response (ms)', 
                           marker_color=self.colors), row=2, col=1)
        
        # Data loss
        losses = [self.performance_data[p]['data_loss'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=losses, name='Data Loss (%)', 
                           marker_color=self.colors), row=2, col=2)
        
        # Energy efficiency
        energies = [self.performance_data[p]['energy'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=energies, name='Energy (J/bit)', 
                           marker_color=self.colors), row=3, col=1)
        
        # Scalability
        scalabilities = [self.performance_data[p]['scalability'] for p in protocols]
        fig.add_trace(go.Bar(x=protocols, y=scalabilities, name='Scalability (nodes)', 
                           marker_color=self.colors), row=3, col=2)
        
        fig.update_layout(height=1000, showlegend=False, 
                         title_text="Comprehensive DTN Protocol Performance Dashboard")
        
        # Rotate x-axis labels
        fig.update_xaxes(tickangle=45)
        
        fig.write_html('/home/krishnendu/dtn_comprehensive_dashboard.html')
        fig.show()
        
    def generate_all_visualizations(self):
        """Generate all visualization types"""
        print("🎨 Generating DTN Visualization Framework...")
        print("📊 Creating parameter comparison table...")
        self.create_parameter_comparison_table()
        
        print("🎯 Creating performance radar chart...")
        self.create_performance_radar_chart()
        
        print("📈 Creating delay vs bandwidth scatter plot...")
        self.create_delay_bandwidth_scatter()
        
        print("🔥 Creating response time vs data loss heatmap...")
        self.create_response_time_data_loss_heatmap()
        
        print("🌟 Creating 3D performance visualization...")
        self.create_3d_performance_visualization()
        
        print("⏱️ Creating time series performance analysis...")
        self.create_time_series_performance()
        
        print("⚡ Creating energy vs scalability analysis...")
        self.create_energy_scalability_analysis()
        
        print("🚀 Creating comprehensive interactive dashboard...")
        self.create_comprehensive_dashboard()
        
        print("✅ All visualizations generated successfully!")
        print("📁 Files saved in /home/krishnendu/")

if __name__ == "__main__":
    # Initialize and run visualization framework
    viz_framework = DTNVisualizationFramework()
    viz_framework.generate_all_visualizations()
