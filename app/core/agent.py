import httpx
import asyncio

GEMINI_KEY = "AIzaSyDFzCXbtilQgwS2DziK5Unv9eW4oF4aP1s"

async def run_intelligence_task(user_input: str, manager):
    await manager.broadcast(f"ANALYZING MISSION: {user_input}", "agent")
    
    # 2026 Recommended Model for Agentic Workflows
    model_id = "gemini-3-flash-preview" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={GEMINI_KEY}"
    
    # Base Config
    config = {"temperature": 1.0} # Standard for Gemini 3

    # 2026 PARAMETER ADAPTER
    if "gemini-3" in model_id:
        # Gemini 3 uses thinking_level (minimal, low, medium, high)
        config["thinking_config"] = {"include_thoughts": True, "thinking_level": "low"}
    else:
        # Gemini 2.5 uses thinking_budget (token count)
        config["thinking_config"] = {"include_thoughts": True, "thinking_budget": 1024}

    payload = {
        "contents": [{"parts": [{"text": f"SYSTEM: You are ZULFIQAR-1. MISSION: {user_input}"}]}],
        "generationConfig": config
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                parts = data['candidates'][0]['content']['parts']
                
                for part in parts:
                    # Accessing the 2026 Thinking Stream
                    if part.get("thought") is True:
                        await manager.broadcast(f"THOUGHTS: {part['text']}", "mcp")
                        await asyncio.sleep(0.5)
                    elif "text" in part:
                        await manager.broadcast(f"ZULFIQAR-1: {part['text']}", "agent")
            else:
                # Direct error reporting to help you if it fails again
                err_msg = response.json().get('error', {}).get('message', 'Unknown Error')
                await manager.broadcast(f"BRAIN ERROR: {err_msg}", "agent")
        except Exception as e:
            await manager.broadcast(f"SYSTEM FAILURE: {str(e)}", "agent")

    await manager.broadcast("MISSION COMPLETE.", "agent")