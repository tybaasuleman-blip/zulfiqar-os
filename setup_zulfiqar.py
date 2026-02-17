import os

# Define the project structure
project_name = "Project_Zulfiqar"
structure = {
    "app": {
        "main.py": "# FastAPI (The Face - Traffic Controller)",
        "core": {
            "agent.py": "# LangChain/LangGraph (The Brain)",
            "mcp_client.py": "# Connects Agent to MCP Tools"
        },
        "mcp": {
            "server.py": "# FastMCP (The Hands - Tactical Tools)"
        },
        "templates": {
            "index.html": "",
            "agent_view.html": "",
            "mcp_view.html": "",
            "port_view.html": ""
        }
    },
    ".env": "# API Keys (OpenAI/Gemini)"
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # It's a file
            with open(path, 'w') as f:
                f.write(content)
            print(f"Created file: {path}")

if __name__ == "__main__":
    # Create the root project folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    root_path = os.path.join(desktop, project_name)
    
    if not os.path.exists(root_path):
        os.makedirs(root_path)
        print(f"Project root created at: {root_path}")
    
    create_structure(root_path, structure)
    print("\n--- Project Zulfiqar Structure Completed Successfully ---")