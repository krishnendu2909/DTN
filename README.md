# DTN Disaster-Resilient Network System

![DTN Network](https://img.shields.io/badge/DTN-Network-blue) ![ns--3](https://img.shields.io/badge/ns--3-Simulation-green) ![Python](https://img.shields.io/badge/Python-Visualization-orange) ![Status](https://img.shields.io/badge/Status-Complete-success)

## 🌟 Overview

A comprehensive **Delay-Tolerant Networking (DTN)** system designed for disaster-resilient communication with advanced visualization capabilities. This project implements a large-scale network simulation with 120 nodes, real-time message flow tracking, and professional-grade performance analysis.

## 🎯 Key Features

### 🔧 Core Implementation
- **120-Node Network**: 80 mobile + 40 static nodes with realistic mobility patterns
- **8 Node Types**: Emergency, Civilian, Vehicle, Drone, Tower, Gateway, Sensor, Relay
- **Optimized Performance**: No hanging issues, efficient epidemic routing with buffer management
- **Real-time Tracking**: 2,699+ message flow events captured and analyzed

### 📊 Advanced Visualizations
- **Interactive Network Topology**: Web-based node positioning and communication links
- **Performance Dashboards**: Real-time metrics with comparative analysis
- **Message Flow Animation**: Visual representation of routing paths and data deployment
- **Mobility Analysis**: Node movement patterns and spatial distribution
- **NetAnim Integration**: Real-time animation of network behavior

### 🚀 Performance Optimizations
- **Staggered Timing**: Reduced network collisions through intelligent scheduling
- **Adaptive Intervals**: Dynamic broadcast timing based on buffer occupancy
- **Buffer Management**: Intelligent message storage with TTL-based cleanup
- **Scalable Architecture**: Handles large-scale networks efficiently

## 📁 Project Structure

```
DTN-Project/
├── src/                          # ns-3 C++ simulation files
│   ├── dtn-disaster-system.cc    # Basic DTN with disaster scenarios
│   ├── dtn-optimized-visualization.cc  # Optimized 120-node simulation
│   └── dtn-advanced-routing.cc   # AI/ML enhanced routing protocols
├── scripts/                      # Python visualization scripts
│   ├── dtn-visualization-scripts.py    # Performance comparison framework
│   └── dtn-network-visualizer.py       # Network topology visualization
├── visualizations/               # Generated charts and dashboards
│   ├── dtn_network_topology.html       # Interactive network map
│   ├── dtn_performance_dashboard.html  # Performance metrics
│   ├── dtn_message_flow_visualization.png  # Message routing diagram
│   └── [Additional charts and heatmaps]
├── data/                        # Simulation output data
│   ├── dtn-optimized-performance.txt   # Performance metrics
│   ├── message-flow-tracking.txt       # Message flow events (2,699 entries)
│   └── dtn-performance-stats.txt       # Basic statistics
└── docs/                        # Documentation
    ├── DTN_PROJECT_SUMMARY.md          # Comprehensive project summary
    └── dtn-project-flowchart.md        # Architecture and design docs
```

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Install ns-3.45
sudo apt-get update
sudo apt-get install ns3-dev

# Install Python dependencies
pip3 install matplotlib seaborn pandas plotly numpy networkx
```

### Quick Start
```bash
# Clone the repository
git clone https://github.com/krishnendu2909/DTN.git
cd DTN

# Run the optimized DTN simulation
cd ns-3.45
./ns3 run scratch/dtn-optimized-visualization

# Generate visualizations
python3 scripts/dtn-network-visualizer.py

# Start web server for interactive dashboards
python3 -m http.server 8080
```

## 📊 Simulation Results

### Network Statistics
- **Total Nodes**: 120 (80 mobile + 40 static)
- **Message Events**: 2,699 tracked events
- **Simulation Time**: 300 seconds
- **Node Types**: 8 distinct categories with realistic behavior

### Performance Metrics
- **Average Delay**: Optimized epidemic routing
- **Message Delivery**: Store-carry-forward with intelligent buffering
- **Network Coverage**: Strategic static node placement
- **Scalability**: Efficient handling of large-scale networks

## 🎨 Visualizations

### Interactive Dashboards (HTML)
- **Network Topology**: Real-time node positions with hover details
- **Performance Dashboard**: Comprehensive metrics and analysis
- **Radar Charts**: Protocol comparison visualization

### Static Analysis (PNG)
- **Message Flow Diagram**: Routing paths with directional arrows
- **Mobility Analysis**: Movement patterns and spatial distribution
- **Performance Comparisons**: Scatter plots and heatmaps
- **Energy Analysis**: Efficiency and scalability metrics

### Real-time Animation
- **NetAnim Integration**: Live node movement and message transmission
- **120-Node Visualization**: Color-coded node types with size differentiation
- **Message Deployment**: Visual packet routing demonstration

## 🔬 Technical Implementation

### DTN Protocols
- **Epidemic Routing**: Optimized with buffer management
- **Store-Carry-Forward**: Intelligent message storage and delivery
- **Adaptive Broadcasting**: Dynamic intervals based on network conditions
- **TTL Management**: Automatic cleanup of expired messages

### Node Architecture
- **Mobile Nodes**: Emergency, Civilian, Vehicle, Drone (Random Waypoint mobility)
- **Static Nodes**: Tower, Gateway, Sensor, Relay (Strategic grid placement)
- **Communication Range**: 250-meter radius with realistic propagation models
- **Buffer Capacity**: Configurable with performance optimization

### Visualization Framework
- **Real Data Integration**: Uses actual simulation output (not hardcoded values)
- **Multi-format Output**: HTML, PNG, TXT reports
- **Interactive Elements**: Zoom, pan, hover information
- **Professional Quality**: Publication-ready graphics

## 📈 Performance Analysis

### Key Achievements
✅ **Large Scale**: 120 nodes simulated successfully  
✅ **No Hanging**: Optimized performance without execution issues  
✅ **Real Tracking**: 2,699+ message events captured  
✅ **Visual Quality**: Professional, interactive visualizations  
✅ **Data Accuracy**: Actual simulation metrics, not synthetic data  

### Comparative Results
- **Improved Delivery Ratio**: Enhanced over standard epidemic routing
- **Reduced Latency**: Optimized forwarding algorithms
- **Energy Efficiency**: Intelligent power management
- **Scalability**: Handles large networks without performance degradation

## 🚀 Usage Examples

### Running Simulations
```bash
# Basic DTN simulation
./ns3 run scratch/dtn-disaster-system

# Optimized large-scale simulation
./ns3 run scratch/dtn-optimized-visualization

# Advanced routing with AI/ML
./ns3 run scratch/dtn-advanced-routing
```

### Generating Visualizations
```bash
# Network topology and message flows
python3 scripts/dtn-network-visualizer.py

# Performance comparison charts
python3 scripts/dtn-visualization-scripts.py

# Start web server for interactive viewing
python3 -m http.server 8080
# Open browser: http://localhost:8080
```

### NetAnim Animation
```bash
# Launch NetAnim with simulation data
cd netanim
./NetAnim ../data/dtn-optimized-animation.xml
```

## 📚 Documentation

- **[Project Summary](docs/DTN_PROJECT_SUMMARY.md)**: Comprehensive overview and results
- **[Architecture Design](docs/dtn-project-flowchart.md)**: System design and flowchart
- **[Performance Report](data/dtn_visualization_report.txt)**: Detailed analysis results

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Krishnendu**
- GitHub: [@krishnendu2909](https://github.com/krishnendu2909)
- Project: [DTN Disaster-Resilient Network System](https://github.com/krishnendu2909/DTN)

## 🙏 Acknowledgments

- ns-3 Network Simulator community
- NetAnim visualization tool
- Python visualization libraries (matplotlib, plotly, seaborn)

---

**Status**: ✅ **Project Complete**  
**Last Updated**: September 2025  
**Version**: 1.0.0
