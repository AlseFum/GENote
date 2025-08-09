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
