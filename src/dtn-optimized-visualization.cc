/*
 * Optimized DTN System with Node Movement and Message Visualization
 * High-performance simulation with large node count and real-time tracking
 * 
 * Author: Krishnendu
 * Project: Advanced DTN Visualization System
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/netanim-module.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("DTNOptimizedVisualization");

// Enhanced Bundle with tracking information
struct DTNBundle {
    uint32_t bundleId;
    uint32_t sourceNode;
    uint32_t destinationNode;
    Time creationTime;
    Time ttl;
    uint32_t hopCount;
    std::string payload;
    bool delivered;
    std::vector<uint32_t> routePath;  // Track message path
    Time lastForwardTime;
};

// Node types for visualization
enum NodeType {
    MOBILE_EMERGENCY = 0,
    MOBILE_CIVILIAN = 1,
    MOBILE_VEHICLE = 2,
    MOBILE_DRONE = 3,
    STATIC_TOWER = 4,
    STATIC_GATEWAY = 5,
    STATIC_SENSOR = 6,
    STATIC_RELAY = 7
};

// Optimized DTN Application
class OptimizedDTNApplication : public Application {
public:
    static TypeId GetTypeId(void);
    OptimizedDTNApplication();
    virtual ~OptimizedDTNApplication();
    
    void SetNodeInfo(uint32_t nodeId, NodeType nodeType);
    void SendBundle(uint32_t destination, std::string payload);
    
private:
    virtual void StartApplication(void);
    virtual void StopApplication(void);
    
    void HandleRead(Ptr<Socket> socket);
    void PeriodicBroadcast();
    void OptimizedRouting();
    void LogMessageFlow(uint32_t bundleId, uint32_t fromNode, uint32_t toNode, std::string action);
    
    Ptr<Socket> m_socket;
    uint32_t m_nodeId;
    NodeType m_nodeType;
    uint32_t m_bundleCounter;
    std::vector<DTNBundle> m_bundleStore;
    EventId m_broadcastEvent;
    Time m_broadcastInterval;
    
    // Performance tracking
    uint32_t m_messagesGenerated;
    uint32_t m_messagesForwarded;
    uint32_t m_messagesDelivered;
    
public:
    // Static message flow tracker
    static std::ofstream s_messageFlowFile;
    static bool s_fileInitialized;
};

std::ofstream OptimizedDTNApplication::s_messageFlowFile;
bool OptimizedDTNApplication::s_fileInitialized = false;

TypeId OptimizedDTNApplication::GetTypeId(void) {
    static TypeId tid = TypeId("OptimizedDTNApplication")
        .SetParent<Application>()
        .SetGroupName("Applications")
        .AddConstructor<OptimizedDTNApplication>();
    return tid;
}

OptimizedDTNApplication::OptimizedDTNApplication() 
    : m_nodeId(0),
      m_nodeType(MOBILE_CIVILIAN),
      m_bundleCounter(0),
      m_broadcastInterval(Seconds(2.0)),
      m_messagesGenerated(0),
      m_messagesForwarded(0),
      m_messagesDelivered(0) {
}

OptimizedDTNApplication::~OptimizedDTNApplication() {}

void OptimizedDTNApplication::SetNodeInfo(uint32_t nodeId, NodeType nodeType) {
    m_nodeId = nodeId;
    m_nodeType = nodeType;
}

void OptimizedDTNApplication::StartApplication(void) {
    NS_LOG_FUNCTION(this);
    
    // Initialize message flow file once
    if (!s_fileInitialized) {
        s_messageFlowFile.open("message-flow-tracking.txt");
        s_messageFlowFile << "Time(s),BundleID,FromNode,ToNode,Action,NodeType\n";
        s_fileInitialized = true;
    }
    
    m_socket = Socket::CreateSocket(GetNode(), UdpSocketFactory::GetTypeId());
    InetSocketAddress local = InetSocketAddress(Ipv4Address::GetAny(), 9999);
    m_socket->Bind(local);
    m_socket->SetRecvCallback(MakeCallback(&OptimizedDTNApplication::HandleRead, this));
    
    // Start periodic broadcasting with staggered timing to reduce collisions
    Time startDelay = Seconds(m_nodeId * 0.1);  // Stagger start times
    m_broadcastEvent = Simulator::Schedule(startDelay, &OptimizedDTNApplication::PeriodicBroadcast, this);
    
    NS_LOG_INFO("Optimized DTN App started on node " << m_nodeId << " (Type: " << m_nodeType << ")");
}

void OptimizedDTNApplication::StopApplication(void) {
    NS_LOG_FUNCTION(this);
    
    if (m_broadcastEvent.IsPending()) {
        Simulator::Cancel(m_broadcastEvent);
    }
    
    if (m_socket) {
        m_socket->Close();
        m_socket = 0;
    }
    
    // Log final statistics
    NS_LOG_INFO("Node " << m_nodeId << " Final Stats - Generated: " << m_messagesGenerated 
                << ", Forwarded: " << m_messagesForwarded << ", Delivered: " << m_messagesDelivered);
}

void OptimizedDTNApplication::SendBundle(uint32_t destination, std::string payload) {
    DTNBundle newBundle;
    newBundle.bundleId = m_bundleCounter++;
    newBundle.sourceNode = m_nodeId;
    newBundle.destinationNode = destination;
    newBundle.creationTime = Simulator::Now();
    newBundle.ttl = Seconds(300);  // 5 minutes TTL
    newBundle.hopCount = 0;
    newBundle.payload = payload;
    newBundle.delivered = false;
    newBundle.routePath.push_back(m_nodeId);
    newBundle.lastForwardTime = Simulator::Now();
    
    m_bundleStore.push_back(newBundle);
    m_messagesGenerated++;
    
    LogMessageFlow(newBundle.bundleId, m_nodeId, m_nodeId, "CREATED");
    
    NS_LOG_INFO("Bundle " << newBundle.bundleId << " created at node " << m_nodeId 
                << " for destination " << destination);
}

void OptimizedDTNApplication::HandleRead(Ptr<Socket> socket) {
    Ptr<Packet> packet;
    Address from;
    
    while ((packet = socket->RecvFrom(from))) {
        // Simulate bundle reception and processing
        InetSocketAddress iaddr = InetSocketAddress::ConvertFrom(from);
        uint32_t fromNodeId = (iaddr.GetIpv4().Get() & 0xFF) - 1;  // Extract node ID from IP
        
        // Create a received bundle (simplified)
        DTNBundle receivedBundle;
        receivedBundle.bundleId = m_bundleCounter++;
        receivedBundle.sourceNode = fromNodeId;
        receivedBundle.destinationNode = m_nodeId;
        receivedBundle.creationTime = Simulator::Now();
        receivedBundle.ttl = Seconds(300);
        receivedBundle.hopCount = 1;
        receivedBundle.delivered = false;
        receivedBundle.routePath.push_back(fromNodeId);
        receivedBundle.routePath.push_back(m_nodeId);
        
        if (receivedBundle.destinationNode == m_nodeId) {
            // Bundle delivered
            receivedBundle.delivered = true;
            m_messagesDelivered++;
            LogMessageFlow(receivedBundle.bundleId, fromNodeId, m_nodeId, "DELIVERED");
            NS_LOG_INFO("Bundle " << receivedBundle.bundleId << " delivered to node " << m_nodeId);
        } else {
            // Store for forwarding
            if (m_bundleStore.size() < 50) {  // Limit buffer size for performance
                m_bundleStore.push_back(receivedBundle);
                LogMessageFlow(receivedBundle.bundleId, fromNodeId, m_nodeId, "RECEIVED");
            }
        }
    }
}

void OptimizedDTNApplication::PeriodicBroadcast() {
    OptimizedRouting();
    
    // Schedule next broadcast with adaptive interval
    Time nextInterval = m_broadcastInterval;
    if (m_bundleStore.size() > 20) {
        nextInterval = Seconds(1.0);  // Faster when buffer is full
    }
    
    m_broadcastEvent = Simulator::Schedule(nextInterval, &OptimizedDTNApplication::PeriodicBroadcast, this);
}

void OptimizedDTNApplication::OptimizedRouting() {
    // Optimized epidemic routing with buffer management
    std::vector<DTNBundle> bundlesToForward;
    
    for (auto& bundle : m_bundleStore) {
        if (!bundle.delivered && (Simulator::Now() - bundle.creationTime) < bundle.ttl) {
            // Limit forwarding rate to prevent flooding
            if ((Simulator::Now() - bundle.lastForwardTime) > Seconds(1.0)) {
                bundlesToForward.push_back(bundle);
                bundle.lastForwardTime = Simulator::Now();
                
                if (bundlesToForward.size() >= 5) break;  // Limit per-cycle forwards
            }
        }
    }
    
    // Forward selected bundles
    for (const auto& bundle : bundlesToForward) {
        Ptr<Packet> packet = Create<Packet>((uint8_t*)bundle.payload.c_str(), bundle.payload.length());
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 9999);
        m_socket->SendTo(packet, 0, remote);
        
        m_messagesForwarded++;
        LogMessageFlow(bundle.bundleId, m_nodeId, 0, "FORWARDED");  // 0 = broadcast
    }
    
    // Clean up expired bundles
    m_bundleStore.erase(
        std::remove_if(m_bundleStore.begin(), m_bundleStore.end(),
            [](const DTNBundle& bundle) {
                return (Simulator::Now() - bundle.creationTime) >= bundle.ttl;
            }),
        m_bundleStore.end()
    );
}

void OptimizedDTNApplication::LogMessageFlow(uint32_t bundleId, uint32_t fromNode, uint32_t toNode, std::string action) {
    if (s_messageFlowFile.is_open()) {
        s_messageFlowFile << Simulator::Now().GetSeconds() << ","
                         << bundleId << ","
                         << fromNode << ","
                         << toNode << ","
                         << action << ","
                         << m_nodeType << "\n";
        s_messageFlowFile.flush();  // Ensure immediate write
    }
}

// Main simulation function
int main(int argc, char *argv[]) {
    LogComponentEnable("DTNOptimizedVisualization", LOG_LEVEL_INFO);
    
    // Optimized parameters for performance
    uint32_t nMobileNodes = 80;
    uint32_t nStaticNodes = 40;
    double simulationTime = 300.0;  // 5 minutes for faster execution
    
    CommandLine cmd;
    cmd.AddValue("mobileNodes", "Number of mobile nodes", nMobileNodes);
    cmd.AddValue("staticNodes", "Number of static nodes", nStaticNodes);
    cmd.AddValue("simTime", "Simulation time", simulationTime);
    cmd.Parse(argc, argv);
    
    NS_LOG_INFO("Starting Optimized DTN Visualization");
    NS_LOG_INFO("Mobile nodes: " << nMobileNodes << ", Static nodes: " << nStaticNodes);
    NS_LOG_INFO("Simulation time: " << simulationTime << " seconds");
    
    // Create nodes
    NodeContainer mobileNodes, staticNodes, allNodes;
    mobileNodes.Create(nMobileNodes);
    staticNodes.Create(nStaticNodes);
    allNodes.Add(mobileNodes);
    allNodes.Add(staticNodes);
    
    // Optimized WiFi configuration
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211n);
    
    WifiMacHelper wifiMac;
    wifiMac.SetType("ns3::AdhocWifiMac");
    
    YansWifiPhyHelper wifiPhy;
    YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default();
    wifiChannel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
    wifiChannel.AddPropagationLoss("ns3::RangePropagationLossModel", "MaxRange", DoubleValue(250.0));
    
    wifiPhy.SetChannel(wifiChannel.Create());
    wifiPhy.Set("TxPowerStart", DoubleValue(15.0));
    wifiPhy.Set("TxPowerEnd", DoubleValue(15.0));
    
    NetDeviceContainer wifiDevices = wifi.Install(wifiPhy, wifiMac, allNodes);
    
    // Enhanced mobility models
    MobilityHelper mobilityMobile, mobilityStatic;
    
    // Mobile nodes with realistic movement patterns
    mobilityMobile.SetPositionAllocator("ns3::RandomRectanglePositionAllocator",
                                       "X", StringValue("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"),
                                       "Y", StringValue("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));
    
    mobilityMobile.SetMobilityModel("ns3::RandomWaypointMobilityModel",
                                   "Speed", StringValue("ns3::UniformRandomVariable[Min=2.0|Max=20.0]"),
                                   "Pause", StringValue("ns3::ConstantRandomVariable[Constant=2.0]"),
                                   "PositionAllocator", StringValue("ns3::RandomRectanglePositionAllocator"));
    
    mobilityMobile.Install(mobileNodes);
    
    // Static nodes in strategic positions
    mobilityStatic.SetPositionAllocator("ns3::GridPositionAllocator",
                                       "MinX", DoubleValue(0.0),
                                       "MinY", DoubleValue(0.0),
                                       "DeltaX", DoubleValue(250.0),
                                       "DeltaY", DoubleValue(250.0),
                                       "GridWidth", UintegerValue(8),
                                       "LayoutType", StringValue("RowFirst"));
    
    mobilityStatic.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobilityStatic.Install(staticNodes);
    
    // Install Internet stack
    InternetStackHelper internet;
    internet.Install(allNodes);
    
    Ipv4AddressHelper ipv4;
    ipv4.SetBase("192.168.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = ipv4.Assign(wifiDevices);
    
    // Install optimized DTN applications
    for (uint32_t i = 0; i < allNodes.GetN(); ++i) {
        Ptr<OptimizedDTNApplication> app = CreateObject<OptimizedDTNApplication>();
        
        NodeType nodeType;
        if (i < nMobileNodes) {
            nodeType = static_cast<NodeType>(i % 4);  // Mobile types 0-3
        } else {
            nodeType = static_cast<NodeType>(4 + (i % 4));  // Static types 4-7
        }
        
        app->SetNodeInfo(i, nodeType);
        allNodes.Get(i)->AddApplication(app);
        app->SetStartTime(Seconds(1.0));
        app->SetStopTime(Seconds(simulationTime));
    }
    
    // Generate realistic message traffic
    for (uint32_t i = 0; i < 30; ++i) {  // Reduced message count for performance
        Simulator::Schedule(Seconds(5.0 + i * 8.0), [&, i]() {
            uint32_t source = i % allNodes.GetN();
            uint32_t dest = (i + allNodes.GetN()/2) % allNodes.GetN();
            
            Ptr<OptimizedDTNApplication> app = DynamicCast<OptimizedDTNApplication>(allNodes.Get(source)->GetApplication(0));
            app->SendBundle(dest, "Emergency message " + std::to_string(i));
        });
    }
    
    // Enhanced NetAnim configuration
    std::string animFile = "dtn-optimized-animation.xml";
    AnimationInterface anim(animFile);
    
    // Set node descriptions and colors for better visualization
    for (uint32_t i = 0; i < nMobileNodes; ++i) {
        NodeType nodeType = static_cast<NodeType>(i % 4);
        switch(nodeType) {
            case MOBILE_EMERGENCY:
                anim.UpdateNodeDescription(mobileNodes.Get(i), "Emergency-" + std::to_string(i));
                anim.UpdateNodeColor(mobileNodes.Get(i), 255, 0, 0);  // Red
                anim.UpdateNodeSize(i, 8.0, 8.0);
                break;
            case MOBILE_CIVILIAN:
                anim.UpdateNodeDescription(mobileNodes.Get(i), "Civilian-" + std::to_string(i));
                anim.UpdateNodeColor(mobileNodes.Get(i), 0, 255, 0);  // Green
                anim.UpdateNodeSize(i, 6.0, 6.0);
                break;
            case MOBILE_VEHICLE:
                anim.UpdateNodeDescription(mobileNodes.Get(i), "Vehicle-" + std::to_string(i));
                anim.UpdateNodeColor(mobileNodes.Get(i), 255, 165, 0);  // Orange
                anim.UpdateNodeSize(i, 10.0, 6.0);
                break;
            case MOBILE_DRONE:
                anim.UpdateNodeDescription(mobileNodes.Get(i), "Drone-" + std::to_string(i));
                anim.UpdateNodeColor(mobileNodes.Get(i), 128, 0, 128);  // Purple
                anim.UpdateNodeSize(i, 5.0, 5.0);
                break;
        }
    }
    
    for (uint32_t i = 0; i < nStaticNodes; ++i) {
        NodeType nodeType = static_cast<NodeType>(4 + (i % 4));
        uint32_t nodeIndex = nMobileNodes + i;
        switch(nodeType) {
            case STATIC_TOWER:
                anim.UpdateNodeDescription(staticNodes.Get(i), "Tower-" + std::to_string(i));
                anim.UpdateNodeColor(staticNodes.Get(i), 0, 0, 255);  // Blue
                anim.UpdateNodeSize(nodeIndex, 15.0, 15.0);
                break;
            case STATIC_GATEWAY:
                anim.UpdateNodeDescription(staticNodes.Get(i), "Gateway-" + std::to_string(i));
                anim.UpdateNodeColor(staticNodes.Get(i), 0, 255, 255);  // Cyan
                anim.UpdateNodeSize(nodeIndex, 12.0, 12.0);
                break;
            case STATIC_SENSOR:
                anim.UpdateNodeDescription(staticNodes.Get(i), "Sensor-" + std::to_string(i));
                anim.UpdateNodeColor(staticNodes.Get(i), 255, 255, 0);  // Yellow
                anim.UpdateNodeSize(nodeIndex, 4.0, 4.0);
                break;
            case STATIC_RELAY:
                anim.UpdateNodeDescription(staticNodes.Get(i), "Relay-" + std::to_string(i));
                anim.UpdateNodeColor(staticNodes.Get(i), 255, 192, 203);  // Pink
                anim.UpdateNodeSize(nodeIndex, 8.0, 8.0);
                break;
        }
    }
    
    // Enable flow monitoring for performance analysis
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();
    
    NS_LOG_INFO("Starting optimized simulation...");
    
    // Run simulation
    Simulator::Stop(Seconds(simulationTime));
    Simulator::Run();
    
    // Generate comprehensive performance report
    monitor->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());
    std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();
    
    std::ofstream statsFile("dtn-optimized-performance.txt");
    statsFile << "DTN Optimized Visualization Performance Report\n";
    statsFile << "============================================\n";
    statsFile << "Total Nodes: " << allNodes.GetN() << " (Mobile: " << nMobileNodes << ", Static: " << nStaticNodes << ")\n";
    statsFile << "Simulation Time: " << simulationTime << " seconds\n\n";
    
    // Flow statistics
    double totalDelay = 0.0;
    double totalThroughput = 0.0;
    uint32_t totalFlows = 0;
    
    statsFile << "FLOW_STATISTICS\n";
    statsFile << "FlowID,TxPackets,RxPackets,Throughput(Kbps),Delay(ms),PacketLoss(%)\n";
    
    for (auto i = stats.begin(); i != stats.end(); ++i) {
        double throughput = 0.0;
        double delay = 0.0;
        double packetLoss = 0.0;
        
        if (i->second.rxPackets > 0) {
            if (i->second.timeLastRxPacket.GetSeconds() > i->second.timeFirstTxPacket.GetSeconds()) {
                throughput = i->second.rxBytes * 8.0 / (i->second.timeLastRxPacket.GetSeconds() - i->second.timeFirstTxPacket.GetSeconds()) / 1024;
            }
            delay = i->second.delaySum.GetMilliSeconds() / i->second.rxPackets;
        }
        
        if (i->second.txPackets > 0) {
            packetLoss = ((double)(i->second.txPackets - i->second.rxPackets) / i->second.txPackets) * 100.0;
        }
        
        statsFile << i->first << "," << i->second.txPackets << "," << i->second.rxPackets 
                  << "," << throughput << "," << delay << "," << packetLoss << "\n";
        
        totalDelay += delay;
        totalThroughput += throughput;
        totalFlows++;
    }
    
    // Summary statistics
    double avgDelay = totalFlows > 0 ? totalDelay / totalFlows : 0.0;
    double avgThroughput = totalFlows > 0 ? totalThroughput / totalFlows : 0.0;
    
    statsFile << "\nSUMMARY_STATISTICS\n";
    statsFile << "AverageDelay(ms)," << avgDelay << "\n";
    statsFile << "AverageThroughput(Kbps)," << avgThroughput << "\n";
    statsFile << "TotalFlows," << totalFlows << "\n";
    
    // Node position tracking for visualization
    statsFile << "\nNODE_POSITIONS\n";
    statsFile << "NodeID,NodeType,X,Y,Z\n";
    
    for (uint32_t i = 0; i < allNodes.GetN(); ++i) {
        Ptr<MobilityModel> mobility = allNodes.Get(i)->GetObject<MobilityModel>();
        Vector pos = mobility->GetPosition();
        
        NodeType nodeType;
        if (i < nMobileNodes) {
            nodeType = static_cast<NodeType>(i % 4);
        } else {
            nodeType = static_cast<NodeType>(4 + ((i - nMobileNodes) % 4));
        }
        
        statsFile << i << "," << nodeType << "," << pos.x << "," << pos.y << "," << pos.z << "\n";
    }
    
    statsFile.close();
    
    // Close message flow file
    if (OptimizedDTNApplication::s_messageFlowFile.is_open()) {
        OptimizedDTNApplication::s_messageFlowFile.close();
    }
    
    NS_LOG_INFO("Optimized simulation completed successfully!");
    NS_LOG_INFO("Results saved to: dtn-optimized-performance.txt");
    NS_LOG_INFO("Message flow: message-flow-tracking.txt");
    NS_LOG_INFO("Animation file: " << animFile);
    
    Simulator::Destroy();
    return 0;
}
