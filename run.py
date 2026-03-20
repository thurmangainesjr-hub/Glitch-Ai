"""
GLITCH - Run Server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ██████╗ ██╗     ██╗████████╗ ██████╗██╗  ██╗         ║
    ║    ██╔════╝ ██║     ██║╚══██╔══╝██╔════╝██║  ██║         ║
    ║    ██║  ███╗██║     ██║   ██║   ██║     ███████║         ║
    ║    ██║   ██║██║     ██║   ██║   ██║     ██╔══██║         ║
    ║    ╚██████╔╝███████╗██║   ██║   ╚██████╗██║  ██║         ║
    ║     ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝         ║
    ║                                                           ║
    ║        AI Development Orchestration System                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
