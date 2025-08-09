## NoteServer

一个简单的在线笔记和随机文本生成工具，支持自定义生成规则。

## 特点

- 极简的笔记编辑界面
- 实时自动保存
- 支持自定义规则的随机文本生成
- 数据自动备份

## 技术栈

- 前端：Vue 3 + Vite
- 后端：FastAPI + Uvicorn
- 文本生成：自定义DSL解析器

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
uvicorn main:app --reload
```

## 项目结构

- `frontend/`  - 前端源码
- `backend/`   - 后端源码
- `spec.md`    - 随机文本生成语法说明
- `API.md`     - API接口文档

## 使用示例

1. 创建/编辑笔记：访问 `noteserver.com/any-note-id`
2. 生成随机文本：访问 `noteserver.com/gen/note-id?start=START`

详细的生成规则语法请参考 `spec.md`。
完整的API文档请查看 `API.md`。

## 贡献

欢迎提交 issue 或 PR。

## 许可证

MIT