from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
os.chdir(r"C:\Users\chaus\dev\repos\regulatory-reporting-mart\site")
ThreadingHTTPServer(("127.0.0.1", 8047), SimpleHTTPRequestHandler).serve_forever()
