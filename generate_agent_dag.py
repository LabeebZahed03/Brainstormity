#!/usr/bin/env python3
"""
Generate a DAG visualization of the agent workflow from agent_details.txt
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_agent_dag():
    # Create directed graph
    G = nx.DiGraph()
    
    # Define agents with their roles
    agents = {
        'Start': 'User Input',
        'A0': 'Planner/Orchestrator',
        'A1': 'Clarifier/Idea-Interpreter', 
        'A2': 'UVP Critic',
        'A3': 'Market Researcher',
        'A4': 'Competitor Scanner',
        'A5': 'Persona & PM-Fit Analyst',
        'A6': 'Feasibility & Cost Estimator',
        'A7': 'Business-Model Synthesizer',
        'A8': 'Devil\'s Advocate/Risk Auditor',
        'A9': 'Action-Plan Composer',
        'A10': 'Quality-Gate/Evaluator',
        'End': 'Final Output'
    }
    
    # Add nodes
    for node_id, role in agents.items():
        G.add_node(node_id, role=role)
    
    # Define edges (workflow connections)
    edges = [
        ('Start', 'A0'),
        ('A0', 'A1'),
        ('A1', 'A2'),
        ('A1', 'A3'),
        ('A1', 'A4'),
        ('A2', 'A5'),
        ('A3', 'A5'),
        ('A4', 'A5'),
        ('A5', 'A6'),
        ('A2', 'A7'),
        ('A3', 'A7'),
        ('A4', 'A7'),
        ('A5', 'A7'),
        ('A6', 'A7'),
        ('A7', 'A8'),
        ('A6', 'A8'),
        ('A8', 'A9'),
        ('A9', 'A10'),
        ('A10', 'End')
    ]
    
    G.add_edges_from(edges)
    
    # Create layout using hierarchical positioning
    pos = {}
    levels = {
        0: ['Start'],
        1: ['A0'],
        2: ['A1'],
        3: ['A2', 'A3', 'A4'],
        4: ['A5'],
        5: ['A6'],
        6: ['A7'],
        7: ['A8'],
        8: ['A9'],
        9: ['A10'],
        10: ['End']
    }
    
    for level, nodes in levels.items():
        for i, node in enumerate(nodes):
            x = (i - (len(nodes) - 1) / 2) * 2
            y = -level * 2
            pos[node] = (x, y)
    
    # Color mapping for different types
    colors = {
        'Start': '#e1f5fe',
        'A0': '#e1f5fe',  # orchestrator
        'A1': '#f3e5f5',  # research
        'A2': '#e8f5e8',  # analysis
        'A3': '#f3e5f5',  # research
        'A4': '#f3e5f5',  # research
        'A5': '#e8f5e8',  # analysis
        'A6': '#e8f5e8',  # analysis
        'A7': '#fff3e0',  # synthesis
        'A8': '#e8f5e8',  # analysis
        'A9': '#fff3e0',  # synthesis
        'A10': '#ffebee', # quality
        'End': '#ffebee'
    }
    
    # Create the plot
    plt.figure(figsize=(16, 20))
    plt.title('Agent Workflow DAG - Brainstormity System', fontsize=20, fontweight='bold', pad=20)
    
    # Draw edges first
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                          arrowsize=20, arrowstyle='->', width=2, alpha=0.7)
    
    # Draw nodes
    for node in G.nodes():
        x, y = pos[node]
        color = colors.get(node, '#f0f0f0')
        
        # Create fancy box for each node
        bbox = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, 
                             boxstyle="round,pad=0.1", 
                             facecolor=color, 
                             edgecolor='black',
                             linewidth=1.5)
        plt.gca().add_patch(bbox)
        
        # Add node text
        role = agents[node]
        if len(role) > 20:
            # Split long text
            words = role.split()
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            plt.text(x, y+0.05, line1, ha='center', va='center', fontsize=9, fontweight='bold')
            plt.text(x, y-0.15, line2, ha='center', va='center', fontsize=9, fontweight='bold')
        else:
            plt.text(x, y, role, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Add node ID
        plt.text(x, y-0.35, node, ha='center', va='center', fontsize=8, 
                style='italic', color='darkblue')
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#e1f5fe', label='Orchestration'),
        plt.Rectangle((0,0),1,1, facecolor='#f3e5f5', label='Research'),
        plt.Rectangle((0,0),1,1, facecolor='#e8f5e8', label='Analysis'),
        plt.Rectangle((0,0),1,1, facecolor='#fff3e0', label='Synthesis'),
        plt.Rectangle((0,0),1,1, facecolor='#ffebee', label='Quality Control')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    # Set axis properties
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('/Users/lbz/Brainstormity/agent_dag_visualization.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('/Users/lbz/Brainstormity/agent_dag_visualization.pdf', 
                bbox_inches='tight', facecolor='white')
    
    print("DAG visualization saved as:")
    print("- agent_dag_visualization.png (high-res image)")
    print("- agent_dag_visualization.pdf (vector format)")
    
    plt.show()

if __name__ == "__main__":
    create_agent_dag()