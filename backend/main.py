import os
import json
import threading
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 备份相关代码
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
os.makedirs(DATA_DIR, exist_ok=True)
frontend_dist = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../frontend/dist'))

def get_latest_backup():
    files = [f for f in os.listdir(DATA_DIR) if f.startswith('backup_') and f.endswith('.json')]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(DATA_DIR, files[0])

def load_backup():
    path = get_latest_backup()
    if path and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('notes', {}), data.get('gens', {})
        except Exception as e:
            print('备份读取失败:', e)
    return {}, {}

def save_backup():
    ts = int(time.time())
    path = os.path.join(DATA_DIR, f'backup_{ts}.json')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'notes': notes, 'gens': gens}, f, ensure_ascii=False)
        print(f'已备份到 {path}')
    except Exception as e:
        print('备份失败:', e)

def backup_loop():
    while True:
        time.sleep(60)
        save_backup()
        # 保留最新40个备份文件
        files = [f for f in os.listdir(DATA_DIR) if f.startswith('backup_') and f.endswith('.json')]
        if len(files) > 40:
            files.sort(reverse=True)
            for old in files[40:]:
                try:
                    os.remove(os.path.join(DATA_DIR, old))
                except Exception as e:
                    print('删除备份失败:', e)

notes, gens = load_backup()
threading.Thread(target=backup_loop, daemon=True).start()

app = FastAPI()

# 允许跨域，便于本地前后端联调
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/{hash}")
def get_note(hash: str):
    return {"content": notes.get(hash, "")}

@app.post("/api/{hash}")
async def save_note(hash: str, request: Request):
    data = await request.json()
    notes[hash] = data.get("content", "")
    p = data.get("gen", "")
    if p:
        gens[hash] = p
    return {"success": True}
from genlang.generator import generate_from_json
@app.get("/gen/{hash}")
def gen_text(hash: str, start: str = "START"):
    print(f"gen_text {hash} {start}")
    payload = {"rules":gens.get(hash, "")}
    if False:
        payload.update({"start":start})
    return generate_from_json(payload)

@app.get("/assets/{path:path}")
def static_assets(path: str):
    asset_path = os.path.join(frontend_dist, "assets", path)
    if os.path.exists(asset_path):
        return FileResponse(asset_path)
    return JSONResponse(status_code=404, content={"error": "Asset not found"})
@app.get("/{path:path}")
def index():
    return FileResponse(frontend_dist + "/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
