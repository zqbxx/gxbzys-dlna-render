# YourPlayer DLNA Render
YourPlayer的一个插件，支持接收DLNA投屏

# 使用方法
1. 下载YourPlayer，解压到安装目录
2. 打开plugin.conf，写入插件配置，保存文件
```json
[
  {
    "name": "dlna_render",
    "class": "render.DLNARenderPlugin"
  }
]
```
3. 启动YourPlayer，使用投屏软件搜索并投屏