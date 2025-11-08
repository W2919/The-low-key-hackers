# 混凝土性能预期视频分类系统 - 协作规范与仓库管理指南

## 一、仓库结构说明
本仓库采用模块化隔离设计，各模块代码独立存放，共享资源集中管理。以下是核心目录结构及用途说明：

```
concrete-video-classification/  # 仓库根目录
├── frontend/                   # 前端（VUE）代码
│   ├── src/components/         # 可复用组件（视频上传、结果展示等）
│   ├── src/views/              # 页面视图（首页、分类页、管理页）
│   ├── src/api/                # 后端接口调用封装
│   └── （其他前端标准目录）
│
├── backend/                    # 后端（FastAPI）代码
│   ├── app/api/                # 接口路由定义
│   ├── app/core/               # 核心配置（数据库、日志等）
│   ├── app/crud/               # 数据库操作逻辑
│   └── （其他后端标准目录）
│
├── algorithm/                  # 算法（PyTorch）代码
│   ├── data/                   # 视频预处理脚本
│   ├── models/                 # 模型定义与加载
│   ├── inference/              # 推理功能实现
│   └── （其他算法相关目录）
│
├── docs/                       # 项目文档（会议纪要、接口文档等）
├── data_samples/               # 示例数据（小体积视频、标签样例）
├── .gitignore                  # 忽略文件配置
├── README.md                   # 仓库总说明
└── docker-compose.yml          # （后期）部署配置
```

**各模块负责人职责**：
- 前端：维护`frontend/`目录，确保组件复用性和页面兼容性
- 后端：维护`backend/`目录，保证接口稳定性和数据安全性
- 算法：维护`algorithm/`目录，优化模型性能和推理效率
- 全员：共同维护`docs/`目录，及时更新相关文档


# 代码提交指导规范

## 一、提交格式规范
采用 **Conventional Commits** 标准，格式为：  
`类型(作用域): 描述信息`

### 1. 提交类型说明
| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能开发 | `feat(frontend): 新增视频上传组件` |
| `fix` | 修复bug | `fix(algorithm): 修复帧提取黑边问题` |
| `docs` | 文档更新 | `docs(backend): 补充分类接口参数说明` |
| `style` | 代码格式调整 | `style: 统一变量命名规范` |
| `refactor` | 代码重构 | `refactor(backend): 优化文件处理逻辑` |
| `test` | 测试代码 | `test(algorithm): 添加模型准确率测试` |
| `chore` | 构建/依赖调整 | `chore: 升级PyTorch版本至1.13.0` |

### 2. 提交要求
- ✅ 描述信息简洁明了（≤50字），统一使用**中文**
- ✅ 每次提交只包含**一个逻辑变更**
- ✅ 提交前**必须本地测试通过**（前端无报错、后端接口可调用、算法脚本可运行）
- ❌ 禁止一次性提交多个不相关功能

## 二、分支管理规范
### 1. 分支创建

```bash
# 1. 同步最新develop代码
git checkout develop
git pull origin develop

# 2. 创建功能分支（命名规范：feat/模块-功能名）
git checkout -b feat/frontend-upload
```

### 2. 分支命名规则
| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 功能开发 | `feat/模块-功能名` | `feat/backend-auth` |
| Bug修复 | `fix/模块-问题描述` | `fix/algorithm-memory` |
| 文档更新 | `doc/文档类型` | `doc/api-spec` |
| 紧急修复 | `hotfix/问题描述` | `hotfix/login-crash` |

### 3. 关键原则
- ✅ **永远**从`develop`分支创建新分支
- ✅ 每日同步`develop`分支：`git pull origin develop`
- ❌ **禁止**直接在`develop`或`main`分支开发
- ❌ **禁止**从`main`分支拉取代码开发新功能

## 三、PR提交流程
### 1. 提交流程
```bash
# 1. 完成功能开发后
git add .
git commit -m "feat(frontend): 实现视频预览功能"

# 2. 推送到远程
git push -u origin feat/frontend-upload

# 3. 在GitHub创建PR（目标分支：develop）
```

### 2. PR必需信息
- **变更内容**：实现了什么功能/修复了什么问题
- **测试方式**：如何验证功能正确性（附测试截图/日志）
- **关联任务**：对应的任务ID或需求文档
- **审核人**：指定对应模块负责人（前端→前端负责人，后端→后端负责人）

### 3. PR审核要求
- 审核人**12小时内**完成审核
- 重点检查：代码规范、功能正确性、性能问题
- 审核通过后由审核人合并，不通过需明确修改意见

## 四、文件提交注意事项
### 1. 禁止提交内容
- ✅ **敏感信息**：数据库密码、API密钥（使用环境变量）
- ✅ **大文件**：视频数据集（>100MB）、模型权重（.pth文件）
- ✅ **构建产物**：`node_modules/`, `venv/`, `dist/`, `.env`
- ✅ **IDE配置**：`.idea/`, `.vscode/`, `.DS_Store`

### 2. 正确处理方式
| 文件类型 | 处理方式 |
|----------|----------|
| 环境变量 | 提交`.env.example`模板，值通过环境变量注入 |
| 模型权重 | 上传至Hugging Face Model Hub，代码中提供下载链接 |
| 视频数据 | 示例数据放`data_samples/`，完整数据通过团队云盘共享 |
| 配置文件 | 提交示例配置（如`config.example.yaml`），实际配置通过环境变量 |

### 3. 文档同步要求
- 功能/接口变更后，**同步更新** `docs/` 中对应文档
- 会议纪要需在**24小时内**上传至 `docs/meeting_notes/`

## 五、常见问题处理
### 1. 提交信息错误
- 未推送：`git commit --amend` 修改
- 已推送：提交修正commit `docs: 修正前次提交信息格式`

### 2. 合并冲突
```bash
# 1. 拉取目标分支最新代码
git pull origin develop

# 2. 手动解决冲突
# 3. 标记解决并提交
git add .
git commit -m "fix: resolve merge conflicts"
```

### 3. 紧急修复流程
```bash
# 1. 从main分支创建hotfix
git checkout main
git pull origin main
git checkout -b hotfix/login-crash

# 2. 修复后创建PR（目标分支：main）
# 3. 合并后同步到develop
git checkout develop
git pull origin develop
git merge main
```

> **重要原则**：代码质量 > 开发速度，规范提交 > 快速提交  
> 本规范最后更新：2025-11-08

请所有成员严格遵守以上规范，确保协作高效有序。如有疑问或建议，可在团队会议中提出讨论更新。

