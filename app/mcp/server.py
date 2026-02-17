# app/mcp/server.py
from fastmcp import FastMCP
import subprocess
import re

# Initialize the Tactical Server
mcp = FastMCP("Zulfiqar-Tactical")

@mcp.tool()
def nmap_scan(target: str) -> str:
    """
    Performs a real Nmap port scan on a target IP or hostname.
    Args:
        target: The IP address or domain to scan (e.g., '192.168.1.1')
    """
    print(f"[*] Executing Tactical Scan on: {target}")
    try:
        # Runs the real nmap command on your system
        result = subprocess.run(
            ["nmap", "-F", target], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error executing scan: {str(e)}"

@mcp.tool()
def get_system_traffic() -> str:
    """
    Checks local network interface traffic levels.
    """
    # Simplified version: returns a mock status for the demo
    return "TRAFFIC_LEVEL: STABLE | PACKETS_SEC: 42 | THREAT_DETECTED: NONE"

if __name__ == "__main__":
    # Start the MCP server using Standard IO (stdio)
    mcp.run()