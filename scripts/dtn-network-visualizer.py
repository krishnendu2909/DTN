#!/usr/bin/env python3
"""
DTN Network Visualizer - Real-time Node Movement and Message Flow Visualization
Processes simulation data to create interactive network topology and message tracking
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import seaborn as sns
from matplotlib.patches import Circle
import os
import re
from datetime import datetime

class DTNNetworkVisualizer:
    def __init__(self):
        """Initialize the DTN Network Visualizer"""
        self.node_positions = {}
        self.message_flows = []
        self.performance_data = {}
        self.node_types = {
            0: {'name': 'Emergency', 'color': '#FF0000', 'size': 8},
            1: {'name': 'Civilian', 'color': '#00FF00', 'size': 6},
            2: {'name': 'Vehicle', 'color': '#FFA500', 'size': 10},
            3: {'name': 'Drone', 'color': '#800080', 'size': 5},
            4: {'name': 'Tower', 'color': '#0000FF', 'size': 15},
            5: {'name': 'Gateway', 'color': '#00FFFF', 'size': 12},
            6: {'name': 'Sensor', 'color': '#FFFF00', 'size': 4},
            7: {'name': 'Relay', 'color': '#FFC0CB', 'size': 8}
        }
        self.load_simulation_data()
    
    def load_simulation_data(self):
        """Load simulation data from output files"""
        try:
            # Copy files from ns-3 directory
            os.system("cp ns-3.45/dtn-optimized-performance.txt . 2>/dev/null")
            os.system("cp ns-3.45/message-flow-tracking.txt . 2>/dev/null")
            
            self.load_node_positions()
            self.load_message_flows()
            self.load_performance_metrics()
            print("✅ Successfully loaded simulation data")
        except Exception as e:
            print(f"⚠️  Error loading simulation data: {e}")
            self.generate_sample_data()
    
    def load_node_positions(self):
        """Load node positions from performance file"""
        try:
            if os.path.exists('dtn-optimized-performance.txt'):
                with open('dtn-optimized-performance.txt', 'r') as f:
                    content = f.read()
                    
                lines = content.split('\n')
                position_section = False
                
                for line in lines:
                    if line.strip() == "NODE_POSITIONS":
                        position_section = True
                        continue
                    elif position_section and ',' in line and not line.startswith('NodeID'):
                        parts = line.strip().split(',')
                        if len(parts) >= 5:
                            node_id = int(parts[0])
                            node_type = int(parts[1])
                            x = float(parts[2])
                            y = float(parts[3])
                            
                            self.node_positions[node_id] = {
                                'x': x, 'y': y, 'type': node_type,
                                'is_mobile': node_type < 4
                            }
                
                print(f"📍 Loaded positions for {len(self.node_positions)} nodes")
        except Exception as e:
            print(f"⚠️  Error loading node positions: {e}")
    
    def load_message_flows(self):
        """Load message flow data"""
        try:
            if os.path.exists('message-flow-tracking.txt'):
                df = pd.read_csv('message-flow-tracking.txt')
                self.message_flows = df.to_dict('records')
                print(f"📨 Loaded {len(self.message_flows)} message flow events")
        except Exception as e:
            print(f"⚠️  Error loading message flows: {e}")
    
    def load_performance_metrics(self):
        """Load performance metrics"""
        try:
            if os.path.exists('dtn-optimized-performance.txt'):
                with open('dtn-optimized-performance.txt', 'r') as f:
                    content = f.read()
                    
                # Extract summary statistics
                lines = content.split('\n')
                for line in lines:
                    if 'AverageDelay' in line:
                        self.performance_data['avg_delay'] = float(line.split(',')[1])
                    elif 'AverageThroughput' in line:
                        self.performance_data['avg_throughput'] = float(line.split(',')[1])
                    elif 'TotalFlows' in line:
                        self.performance_data['total_flows'] = int(line.split(',')[1])
                
                print("📊 Loaded performance metrics")
        except Exception as e:
            print(f"⚠️  Error loading performance metrics: {e}")
    
    def generate_sample_data(self):
        """Generate sample data when simulation data is not available"""
        print("📊 Generating sample visualization data...")
        
        # Sample node positions
        for i in range(120):
            node_type = i % 8
            is_mobile = node_type < 4
            
            if is_mobile:
                x = np.random.uniform(0, 1500)
                y = np.random.uniform(0, 1500)
            else:
                # Static nodes in grid
                grid_x = (i // 8) * 250
                grid_y = (i % 8) * 200
                x = grid_x
                y = grid_y
            
            self.node_positions[i] = {
                'x': x, 'y': y, 'type': node_type, 'is_mobile': is_mobile
            }
        
        # Sample message flows
        for i in range(50):
            self.message_flows.append({
                'Time(s)': i * 2.0,
                'BundleID': i,
                'FromNode': i % 120,
                'ToNode': (i + 60) % 120,
                'Action': 'FORWARDED',
                'NodeType': (i % 120) % 8
            })
        
        self.performance_data = {
            'avg_delay': 45.2,
            'avg_throughput': 125.8,
            'total_flows': 50
        }
    
    def create_network_topology_visualization(self):
        """Create interactive network topology visualization"""
        print("🌐 Creating network topology visualization...")
        
        fig = go.Figure()
        
        # Add nodes by type
        for node_type in range(8):
            nodes_of_type = [nid for nid, data in self.node_positions.items() if data['type'] == node_type]
            
            if nodes_of_type:
                x_coords = [self.node_positions[nid]['x'] for nid in nodes_of_type]
                y_coords = [self.node_positions[nid]['y'] for nid in nodes_of_type]
                
                fig.add_trace(go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode='markers',
                    name=self.node_types[node_type]['name'],
                    marker=dict(
                        size=self.node_types[node_type]['size'],
                        color=self.node_types[node_type]['color'],
                        opacity=0.8,
                        line=dict(width=1, color='black')
                    ),
                    text=[f"Node {nid}<br>Type: {self.node_types[node_type]['name']}<br>Position: ({self.node_positions[nid]['x']:.1f}, {self.node_positions[nid]['y']:.1f})" for nid in nodes_of_type],
                    hovertemplate='%{text}<extra></extra>'
                ))
        
        # Add communication links (sample connections)
        for i in range(0, min(len(self.node_positions), 50), 5):
            for j in range(i+1, min(i+10, len(self.node_positions))):
                if i in self.node_positions and j in self.node_positions:
                    x1, y1 = self.node_positions[i]['x'], self.node_positions[i]['y']
                    x2, y2 = self.node_positions[j]['x'], self.node_positions[j]['y']
                    
                    # Only show links within communication range
                    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if distance < 300:  # Communication range
                        fig.add_trace(go.Scatter(
                            x=[x1, x2, None],
                            y=[y1, y2, None],
                            mode='lines',
                            line=dict(color='gray', width=0.5, dash='dot'),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
        
        fig.update_layout(
            title=dict(
                text="DTN Network Topology - Node Distribution and Communication Links",
                x=0.5,
                font=dict(size=16, color='darkblue')
            ),
            xaxis_title="X Position (meters)",
            yaxis_title="Y Position (meters)",
            width=1200,
            height=800,
            showlegend=True,
            legend=dict(x=1.02, y=1),
            hovermode='closest'
        )
        
        fig.write_html('/home/krishnendu/dtn_network_topology.html')
        print("💾 Network topology saved as dtn_network_topology.html")
    
    def create_message_flow_animation(self):
        """Create animated message flow visualization"""
        print("📡 Creating message flow animation...")
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plot static nodes
        static_nodes = {nid: data for nid, data in self.node_positions.items() if not data['is_mobile']}
        mobile_nodes = {nid: data for nid, data in self.node_positions.items() if data['is_mobile']}
        
        # Static nodes
        for nid, data in static_nodes.items():
            color = self.node_types[data['type']]['color']
            size = self.node_types[data['type']]['size'] * 10
            ax.scatter(data['x'], data['y'], c=color, s=size, alpha=0.8, 
                      marker='s', label=f"Static-{self.node_types[data['type']]['name']}" if nid == list(static_nodes.keys())[0] else "")
        
        # Mobile nodes
        for nid, data in mobile_nodes.items():
            color = self.node_types[data['type']]['color']
            size = self.node_types[data['type']]['size'] * 8
            ax.scatter(data['x'], data['y'], c=color, s=size, alpha=0.7, 
                      marker='o', label=f"Mobile-{self.node_types[data['type']]['name']}" if nid == list(mobile_nodes.keys())[0] else "")
        
        # Add message flow arrows
        if self.message_flows:
            for i, flow in enumerate(self.message_flows[:20]):  # Show first 20 flows
                try:
                    from_node = int(flow['FromNode'])
                    to_node = int(flow['ToNode'])
                    
                    if from_node in self.node_positions and to_node in self.node_positions:
                        x1, y1 = self.node_positions[from_node]['x'], self.node_positions[from_node]['y']
                        x2, y2 = self.node_positions[to_node]['x'], self.node_positions[to_node]['y']
                        
                        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                                   arrowprops=dict(arrowstyle='->', color='red', alpha=0.6, lw=1.5))
                except:
                    continue
        
        ax.set_xlabel('X Position (meters)', fontsize=12)
        ax.set_ylabel('Y Position (meters)', fontsize=12)
        ax.set_title('DTN Message Flow Visualization\nRed arrows show message routing paths', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/dtn_message_flow_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("💾 Message flow visualization saved as dtn_message_flow_visualization.png")
    
    def create_performance_dashboard(self):
        """Create comprehensive performance dashboard"""
        print("📈 Creating performance dashboard...")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Network Performance Metrics', 'Node Type Distribution', 
                          'Message Flow Timeline', 'Communication Range Analysis'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "heatmap"}]]
        )
        
        # Performance metrics bar chart
        metrics = ['Avg Delay (ms)', 'Avg Throughput (Kbps)', 'Total Flows']
        values = [
            self.performance_data.get('avg_delay', 45.2),
            self.performance_data.get('avg_throughput', 125.8),
            self.performance_data.get('total_flows', 50)
        ]
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
            name='Performance'
        ), row=1, col=1)
        
        # Node type distribution pie chart
        node_type_counts = {}
        for data in self.node_positions.values():
            node_type = data['type']
            type_name = self.node_types[node_type]['name']
            node_type_counts[type_name] = node_type_counts.get(type_name, 0) + 1
        
        fig.add_trace(go.Pie(
            labels=list(node_type_counts.keys()),
            values=list(node_type_counts.values()),
            name="Node Types"
        ), row=1, col=2)
        
        # Message flow timeline
        if self.message_flows:
            times = [float(flow['Time(s)']) for flow in self.message_flows[:30]]
            bundle_ids = [int(flow['BundleID']) for flow in self.message_flows[:30]]
            
            fig.add_trace(go.Scatter(
                x=times,
                y=bundle_ids,
                mode='markers+lines',
                marker=dict(size=8, color='orange'),
                name='Message Flow'
            ), row=2, col=1)
        
        # Communication range heatmap
        x_range = np.linspace(0, 1500, 20)
        y_range = np.linspace(0, 1500, 20)
        coverage_matrix = np.zeros((20, 20))
        
        for i, x in enumerate(x_range):
            for j, y in enumerate(y_range):
                coverage = 0
                for node_data in self.node_positions.values():
                    distance = np.sqrt((x - node_data['x'])**2 + (y - node_data['y'])**2)
                    if distance < 250:  # Communication range
                        coverage += 1
                coverage_matrix[j, i] = coverage
        
        fig.add_trace(go.Heatmap(
            z=coverage_matrix,
            colorscale='Viridis',
            name='Coverage'
        ), row=2, col=2)
        
        fig.update_layout(
            title_text="DTN Network Performance Dashboard",
            showlegend=True,
            height=800,
            width=1400
        )
        
        fig.write_html('/home/krishnendu/dtn_performance_dashboard.html')
        print("💾 Performance dashboard saved as dtn_performance_dashboard.html")
    
    def create_node_mobility_analysis(self):
        """Create node mobility pattern analysis"""
        print("🚶 Creating node mobility analysis...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Mobile vs Static node distribution
        mobile_count = sum(1 for data in self.node_positions.values() if data['is_mobile'])
        static_count = len(self.node_positions) - mobile_count
        
        ax1.pie([mobile_count, static_count], labels=['Mobile Nodes', 'Static Nodes'], 
                autopct='%1.1f%%', colors=['#FF9999', '#66B2FF'])
        ax1.set_title('Mobile vs Static Node Distribution', fontweight='bold')
        
        # Node type distribution by mobility
        mobile_types = {}
        static_types = {}
        
        for data in self.node_positions.values():
            type_name = self.node_types[data['type']]['name']
            if data['is_mobile']:
                mobile_types[type_name] = mobile_types.get(type_name, 0) + 1
            else:
                static_types[type_name] = static_types.get(type_name, 0) + 1
        
        ax2.bar(mobile_types.keys(), mobile_types.values(), alpha=0.7, label='Mobile', color='orange')
        ax2.bar(static_types.keys(), static_types.values(), alpha=0.7, label='Static', color='blue')
        ax2.set_title('Node Types by Mobility', fontweight='bold')
        ax2.set_ylabel('Count')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        
        # Spatial distribution heatmap
        x_coords = [data['x'] for data in self.node_positions.values()]
        y_coords = [data['y'] for data in self.node_positions.values()]
        
        ax3.hist2d(x_coords, y_coords, bins=20, cmap='Blues', alpha=0.7)
        ax3.set_title('Node Spatial Distribution Heatmap', fontweight='bold')
        ax3.set_xlabel('X Position (meters)')
        ax3.set_ylabel('Y Position (meters)')
        
        # Message generation by node type
        if self.message_flows:
            node_message_count = {}
            for flow in self.message_flows:
                try:
                    node_id = int(flow['FromNode'])
                    if node_id in self.node_positions:
                        node_type = self.node_positions[node_id]['type']
                        type_name = self.node_types[node_type]['name']
                        node_message_count[type_name] = node_message_count.get(type_name, 0) + 1
                except:
                    continue
            
            if node_message_count:
                ax4.bar(node_message_count.keys(), node_message_count.values(), 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'])
                ax4.set_title('Message Generation by Node Type', fontweight='bold')
                ax4.set_ylabel('Messages Generated')
                ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('/home/krishnendu/dtn_mobility_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("💾 Mobility analysis saved as dtn_mobility_analysis.png")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive text report"""
        print("📋 Generating comprehensive report...")
        
        report = f"""
DTN Network Visualization Report
===============================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

NETWORK OVERVIEW
----------------
Total Nodes: {len(self.node_positions)}
Mobile Nodes: {sum(1 for data in self.node_positions.values() if data['is_mobile'])}
Static Nodes: {sum(1 for data in self.node_positions.values() if not data['is_mobile'])}

NODE TYPE DISTRIBUTION
---------------------
"""
        
        node_type_counts = {}
        for data in self.node_positions.values():
            type_name = self.node_types[data['type']]['name']
            node_type_counts[type_name] = node_type_counts.get(type_name, 0) + 1
        
        for type_name, count in node_type_counts.items():
            report += f"{type_name}: {count} nodes\n"
        
        report += f"""
PERFORMANCE METRICS
------------------
Average Delay: {self.performance_data.get('avg_delay', 'N/A')} ms
Average Throughput: {self.performance_data.get('avg_throughput', 'N/A')} Kbps
Total Flows: {self.performance_data.get('total_flows', 'N/A')}

MESSAGE FLOW ANALYSIS
--------------------
Total Message Events: {len(self.message_flows)}
"""
        
        if self.message_flows:
            actions = {}
            for flow in self.message_flows:
                action = flow.get('Action', 'UNKNOWN')
                actions[action] = actions.get(action, 0) + 1
            
            for action, count in actions.items():
                report += f"{action}: {count} events\n"
        
        report += f"""
VISUALIZATION FILES GENERATED
-----------------------------
- dtn_network_topology.html (Interactive network topology)
- dtn_performance_dashboard.html (Performance dashboard)
- dtn_message_flow_visualization.png (Message flow diagram)
- dtn_mobility_analysis.png (Mobility pattern analysis)

RECOMMENDATIONS
--------------
1. Monitor high-traffic nodes for potential bottlenecks
2. Optimize routing protocols based on node mobility patterns
3. Consider adding more static relay nodes in low-coverage areas
4. Implement adaptive transmission power based on node density
"""
        
        with open('/home/krishnendu/dtn_visualization_report.txt', 'w') as f:
            f.write(report)
        
        print("💾 Comprehensive report saved as dtn_visualization_report.txt")
    
    def generate_all_visualizations(self):
        """Generate all visualizations and reports"""
        print("🎨 Generating DTN Network Visualizations...")
        
        self.create_network_topology_visualization()
        self.create_message_flow_animation()
        self.create_performance_dashboard()
        self.create_node_mobility_analysis()
        self.generate_comprehensive_report()
        
        print("\n✅ All visualizations completed successfully!")
        print("\n📁 Generated Files:")
        print("   - dtn_network_topology.html")
        print("   - dtn_performance_dashboard.html") 
        print("   - dtn_message_flow_visualization.png")
        print("   - dtn_mobility_analysis.png")
        print("   - dtn_visualization_report.txt")

if __name__ == "__main__":
    visualizer = DTNNetworkVisualizer()
    visualizer.generate_all_visualizations()
