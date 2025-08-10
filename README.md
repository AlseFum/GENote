## NoteServer

一个简单的在线笔记和随机文本生成工具，支持自定义生成规则。
- 极简的笔记编辑界面
- 实时自动保存
- 支持自定义规则的随机文本生成
- 数据自动备份

## 技术栈

- 前端：Vue 3 + Vite
- 后端：FastAPI + Uvicorn
- DSL: peggyjs

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run build_gen
npm run build
```

### 后端
```bash
cd backend
uvicorn main:app --reload
或者
python -m backend.main
默认在8000端口
```
### 测试DSL
cd genlang
python test.py

## 项目结构

- `frontend/`  - 前端源码
- `backend/`   - 后端源码
- `spec.md`    - 随机文本生成语法说明
- `API.md`     - API接口文档

## 使用示例

1. 创建/编辑笔记：访问 `noteserver.com/any-note-id`
2. 生成随机文本：访问 `noteserver.com/gen/note-id?start=START`

详细的生成规则语法请参考 `spec.md`。

## API端点
NoteServer API 文档

1. 获取笔记内容
接口：GET /api/{hash}
参数：
- hash（路径参数，笔记唯一标识）
返回：
```json
{
    "content": "笔记内容" // 如果笔记不存在则返回空字符串
}
```

2. 保存笔记内容
接口：POST /api/{hash}
参数：
- hash（路径参数，笔记唯一标识）
请求体（JSON）：
```json
{
    "content": "笔记内容",
    "gen": "可选，解析后的生成规则" 
}
```
返回：
```json
{
    "success": true
}
```

3. 生成随机文本
接口：GET /gen/{hash}
参数：
- hash（路径参数，标识）
- start（查询参数，起始项，默认值为"START"）
返回：保存的生成规则内容，如果不存在则返回空字符串

4. 静态资源访问
接口：GET /assets/{path}
参数：
- path（路径参数，资源路径）
返回：
- 成功：返回对应的静态资源文件
- 失败：返回404状态码
```json
{
    "error": "Asset not found"
}
```

5. 前端页面
接口：GET /{path}
说明：处理所有其他路径，返回前端入口页面index.html


## 贡献

欢迎提交 issue 或 PR。

## 许可证

MIT

## To startup
python -m backend.main

regenerate the parser:
cd frontend && pnpm run build_gen