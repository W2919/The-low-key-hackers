
# realTimeMap开发指南

### 地图规划界面独立开发

地图规划界面支持独立运行，便于快速开发和测试：

#### 快速启动
```bash
# 1. 独立开发地图功能
# 主目录下
# 正常快速运行
python "./controller/map.py"

# 添加日志信息
export MOD_MAP_EDIT_MOD="mod_dev"
python "./controller/map.py"
```


## 代码结构说明

### 项目结构
```
项目根目录/
├── controller/
│   ├── map.py              # PyQt5地图应用主程序（可独立运行）
│   └── realTimeMapSrc.html # 高德地图Web界面
├── docs/
|   └── realTimeMap.md       #项目说明文档（本文件）
```

### 文件说明

#### 1. map.py - PyQt5桌面应用
**功能特性：**
- 基于PyQt5的桌面地图应用程序
- 嵌入高德地图Web页面进行路径规划
- 支持地理位置权限管理
- 可独立运行

**核心类说明：**

**CustomWebEnginePage类**
- 继承自QWebEnginePage
- 处理JavaScript控制台消息和权限请求
- 地理位置权限的自动授权处理

**RealTimeMapApp类**
- 主窗口类，继承自QMainWindow
- 管理WebEngineView和地图界面
- 提供临时文件管理和资源清理

**主要方法：**
- `create_temp_html()`: 创建临时HTML文件
- `init_ui()`: 初始化用户界面
- `load_map()`: 加载地图内容
- `configure_web_settings()`: 配置Web引擎设置
- `inject_enhancement_script()`: 注入JavaScript增强功能

#### 2. realTimeMapSrc.html - 高德地图Web界面
**功能特性：**
- 响应式高德地图Web应用
- 路径规划和实时定位功能
- 美观的UI设计

**核心功能模块：**
- 地图初始化(`initMap()`)
- 当前位置获取(`getCurrentLocation()`)
- 路径规划(`routePlan()`)
- 路线清除(`clearRoute()`)

### 注意事项
- 需要有效的网络连接加载高德地图API


## 故障排除

### 常见问题
1. **地图界面无法独立运行**
   - 检查依赖是否完整安装
   - 验证环境变量设置是否正确
   - 查看控制器初始化逻辑

2. **调试信息不显示**
   - 确认环境变量名称正确
   - 检查环境变量是否成功设置
   - 验证调试代码逻辑

---

* 最后更新: 2025年11月27
* 文档版本: v1.0