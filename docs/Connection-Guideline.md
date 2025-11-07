# 本地Git连接GitHub私有仓库操作教程

## 一、前置准备

### 1. 安装Git
- 检查是否已安装：打开终端（Windows用PowerShell，Mac/Linux用Terminal），输入`git --version`，若显示版本号则已安装。
- 未安装：前往[Git官网](https://git-scm.com/)下载对应系统版本，按默认选项安装。

### 2. 获取仓库地址
1. 登录GitHub，进入项目私有仓库（如`concrete-video-classification`）。
2. 点击右上角「Code」按钮，复制仓库地址：
   - HTTPS格式：`https://github.com/用户名/仓库名.git`
   - SSH格式：`git@github.com:用户名/仓库名.git`（推荐长期使用）

### 3. 确认访问权限
- 联系仓库管理员，确保你的GitHub账号已被添加为「协作者」（仓库→Settings→Collaborators→添加用户名）。
- 无权限会导致`Permission denied`错误。

## 二、SSH连接
一次配置，长期使用，无需反复输入令牌。

### 步骤1：生成SSH密钥
1. 终端输入（替换为你的GitHub绑定邮箱）：
   ```bash
   ssh-keygen -t ed25519 -C "你的邮箱@example.com"
   ```
2. 连续按回车（默认路径、无密码），生成两个文件：
   - 私钥：`~/.ssh/id_ed25519`（勿泄露，勿删除）
   - 公钥：`~/.ssh/id_ed25519.pub`（需上传到GitHub）

### 步骤2：复制公钥内容
- 终端输入`cat ~/.ssh/id_ed25519.pub`，复制输出的完整字符串（以`ssh-ed25519`开头）。


### 步骤3：GitHub添加SSH公钥
1. 登录GitHub→头像→「Settings」→「SSH and GPG keys」→「New SSH key」。
2. 填写：
   - Title：输入设备标识（如`我的笔记本`）。
   - Key：粘贴步骤2复制的公钥内容。
3. 点击「Add SSH key」完成添加。

### 步骤4：克隆/关联仓库（使用SSH地址）
1. **克隆仓库（首次操作）**：
   ```bash
   git clone git@github.com:用户名/仓库名.git
   ```
   - 首次连接会提示确认，输入`yes`回车，无需密码即可克隆。

2. **本地已有项目？关联远程仓库**：
   ```bash
   cd 你的项目文件夹
   git init  # 若未初始化
   git remote add origin git@github.com:用户名/仓库名.git
   ```
   - 验证：`git remote -v`显示SSH地址即成功。


## 四、验证连接是否成功
执行以下命令测试能否访问远程仓库：
```bash
git fetch origin  # 拉取远程分支信息（无修改本地代码）
```
- 成功：显示`From github.com:用户名/仓库名`。
- 失败：参考「常见问题」排查。


## 五、常用操作命令
| 操作 | 命令 |
|------|------|
| 拉取远程develop分支最新代码 | `git pull origin develop` |
| 创建并切换到功能分支 | `git checkout -b feat/模块-功能名` |
| 提交本地修改 | `git add .` <br> `git commit -m "feat(模块): 描述内容"` |
| 推送本地分支到远程 | `git push origin 你的分支名` |
| 查看当前分支 | `git branch` |
| 切换到已有分支 | `git checkout 分支名` |


## 六、常见问题解决
1. **克隆时报错`Permission denied`**：
   - 检查是否被添加为仓库协作者。
   - SSH连接确认公钥已正确添加到GitHub（重新生成并添加）。


3. **SSH连接时报错`Host key verification failed`**：
   - 终端输入`ssh -T git@github.com`，按提示输入`yes`确认主机信息。

4. **忘记PAT或密钥丢失**：
   - PAT：在GitHub→「Personal access tokens」→删除旧令牌，重新生成。
   - SSH密钥：重新执行「步骤1-3」生成新密钥并添加。


## 七、注意事项
- 私有仓库代码请勿泄露，勿上传敏感信息（如数据库密码、API密钥）。
- 严格遵循项目分支规范（从`develop`创建功能分支，命名格式`feat/模块-功能`）。
- 提交信息需符合规范（如`feat(frontend): 添加视频上传组件`）。

---

如有其他问题，可在团队群内反馈，共同排查解决。
