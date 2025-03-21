from fastapi import FastAPI
from api.route import users, projects, runs, processes, operations, edges
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    # 許可するオリジン（フロントエンドのURL）
    allow_origins=["http://labcode-web-app.com:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(runs.router)
app.include_router(processes.router)
app.include_router(operations.router)
app.include_router(edges.router)
