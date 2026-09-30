import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from run_history import check, document_text, fetch_document


class HistoryTests(unittest.TestCase):
    def test_detects_lost_first_run(self):
        self.assertEqual(check("OUTCOME:run-2", ["OUTCOME:run-1", "OUTCOME:run-2"])["missing"], ["OUTCOME:run-1"])

    def test_nested_document(self):
        self.assertEqual(document_text({"document": {"original_text": "record"}}), "record")

    def test_rejects_duplicate_markers(self):
        with self.assertRaises(ValueError):
            check("x", ["x", "x"])

    def test_reads_hindsight_document_route(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                assert self.path == "/v1/default/banks/demo/documents/conversation%3Aone"
                body = json.dumps({"original_text": "OUTCOME:run-1 OUTCOME:run-2"}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            response = fetch_document(f"http://127.0.0.1:{server.server_port}", "demo", "conversation:one")
            self.assertEqual(check(document_text(response), ["OUTCOME:run-1", "OUTCOME:run-2"])["missing"], [])
        finally:
            server.shutdown()
            server.server_close()
