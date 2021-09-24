# YourPlayer DLNA Render
YourPlayer的一个插件，支持接收DLNA投屏

# 使用方法
1. 下载YourPlayer，解压到安装目录
2. 下载[插件压缩包](https://github.com/zqbxx/gxbzys-dlna-render/releases)，解压后，将文件夹中文件和文件夹复制到YourPlayer根目录
3. 打开YourPlayer目录下的plugin.conf，写入插件配置，保存文件
```json
[
  {
    "name": "dlna_render",
    "class": "render.DLNARenderPlugin"
  }
]
```
4. 启动YourPlayer，使用投屏软件搜索并投屏