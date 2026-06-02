from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
from pathlib import Path
from typing import Any

# Ensure root dir is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Reconfigure stdout/stderr to handle encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass

from src.agent.graph import run_agent, build_system_prompt


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Multi-threaded HTTP server to prevent UI hanging during long Agent runs."""
    daemon_threads = True


class AgentUIRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format: str, *args: Any) -> None:
        # Prevent spamming the console with static resource GET logs
        pass

    def do_GET(self) -> None:
        try:
            if self.path == "/" or self.path == "/index.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_path = ROOT_DIR / "src" / "ui" / "index.html"
                self.wfile.write(html_path.read_bytes())
                return

            elif self.path == "/api/cases":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                cases_path = ROOT_DIR / "data" / "graded_cases.json"
                self.wfile.write(cases_path.read_bytes())
                return

            elif self.path == "/api/products":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                products_path = ROOT_DIR / "data" / "products.json"
                self.wfile.write(products_path.read_bytes())
                return

            elif self.path == "/api/system_prompt":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                prompt = build_system_prompt()
                payload = {"system_prompt": prompt}
                self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
                return

            else:
                self.send_error(404, "File not found")
                return

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_POST(self) -> None:
        if self.path == "/api/run":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                params = json.loads(post_data.decode("utf-8"))
                query = params.get("query", "").strip()
                provider = params.get("provider", "openai").strip()

                if not query:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Query cannot be empty"}).encode("utf-8"))
                    return

                # Execute the Agent graph live!
                print(f"UI SERVER: Executing agent for query: '{query[:50]}...' via '{provider}'")
                agent_result = run_agent(query, provider=provider)
                
                # Format response payload
                response_data = {
                    "query": agent_result.query,
                    "final_answer": agent_result.final_answer,
                    "tool_calls": [
                        {
                            "name": tool.name,
                            "args": tool.args,
                            "output": tool.output
                        }
                        for tool in agent_result.tool_calls
                    ],
                    "provider": agent_result.provider,
                    "model_name": agent_result.model_name,
                    "saved_order": agent_result.saved_order,
                    "saved_order_path": agent_result.saved_order_path,
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))


def main() -> None:
    PORT = 8888
    print("----------------------------------------------------------------")
    print("ORDERDESK INTERACTIVE UI SERVER STARTED SUCCESSFULLY...")
    print(f"Open your browser at: http://127.0.0.1:{PORT}")
    print("----------------------------------------------------------------")
    
    # Configure threaded server
    ThreadingHTTPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("127.0.0.1", PORT), AgentUIRequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down UI server cleanly...")


if __name__ == "__main__":
    main()
