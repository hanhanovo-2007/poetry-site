# 诗词雅集 - Web 开发大作业

## 项目概述

"诗词雅集"是一个诗词创作爱好者交流社区网站，采用 Vue 3 + Django 6 + SQLite 全栈架构开发。

**选题背景**：高校《Web开发技术》课程期末大作业
**开发目标**：构建一个功能完整的诗词兴趣交流平台，涵盖用户管理、诗词作品 CRUD、评论互动、管理员后台等功能。

## 技术栈

| 层面 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue 3 (Vite) | ^3.5.34 |
| 路由 | vue-router | ^4.6.4 |
| HTTP 客户端 | axios | ^1.18.0 |
| 后端框架 | Django | 6.0.6 |
| 管理后台 | simpleui | latest |
| 数据库 | SQLite（后续可切换 MySQL） | - |
| 包管理 (前端) | pnpm | 11.5.3 |
| 包管理 (后端) | pip (venv) | - |

## 项目结构

`
诗词兴趣网站/
├── .venv/                        # Python 虚拟环境
├── manage.py                     # Django 管理脚本
├── db.sqlite3                    # SQLite 数据库
│
├── poetry_site/                  # Django 项目配置
│   ├── settings.py               # 项目配置（simpleui、中文语言、上海时区）
│   ├── urls.py                   # 根路由
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                        # 用户管理应用
│   ├── models.py                 # 用户模型（待设计）
│   ├── views.py                  # 用户视图（待开发）
│   └── migrations/
│
├── poetry/                       # 诗词作品应用
│   ├── models.py                 # 作品模型（待设计）
│   ├── views.py                  # 作品视图（待开发）
│   └── migrations/
│
└── frontend/                     # Vue 3 前端项目
    ├── src/
    │   ├── main.js               # 入口文件（挂载 Vue + Router）
    │   ├── App.vue               # 根组件（导航栏 + router-view + 页脚）
    │   ├── router/
    │   │   └── index.js          # 路由配置（5个页面路由）
    │   ├── views/
    │   │   ├── Home.vue          # 首页（轮播图、名句展示）
    │   │   ├── Publish.vue       # 发表作品
    │   │   ├── Gallery.vue       # 作品广场
    │   │   ├── Profile.vue       # 个人主页
    │   │   └── About.vue         # 关于我们
    │   ├── api/                  # API 请求层（待开发）
    │   └── style.css             # 全局样式
    ├── vite.config.js            # Vite 配置（含 API 代理）
    └── index.html                # HTML 入口
`

## 开发环境搭建

### 快速启动

`ash
# 1. 激活 Python 虚拟环境
.venv\Scripts\Activate.ps1

# 2. 启动 Django 后端（端口 8000）
python manage.py runserver 0.0.0.0:8000

# 3. 启动 Vue 前端（另一终端，端口 5173）
cd frontend
pnpm run dev
`

### 访问地址

- **Vue 前端**：http://localhost:5173
- **Django 后台管理**：http://localhost:8000/admin/
- **Django API 基础路径**：http://localhost:8000/api/

### 管理员账号

| 字段 | 值 |
|------|------|
| 用户名 | daizhiqi123 |
| 密码 | daizhiqi666 |
| 邮箱 | hanhanovo2007@gmail.com |
| 昵称 | 管理员戴智祺 |

## API 代理说明

前端开发服务器（:5173）已配置代理，将 /api、/admin、/static 前缀的请求转发到 Django 后端（:8000），避免开发时跨域问题。

## 开发状态（当前）

- [x] Django 项目创建 & 配置
- [x] 用户应用 users 创建
- [x] 诗词应用 poetry 创建
- [x] simpleui 后台美化
- [x] Vue 3 + Vite 前端脚手架搭建
- [x] vue-router 路由配置（5 页面）
- [x] Vite 代理配置
- [ ] 数据库模型设计
- [ ] 用户注册/登录 API
- [ ] 诗词 CRUD API
- [ ] 评论功能 API
- [ ] 前端页面内容填充
- [ ] 用户权限控制
- [ ] 文件上传（作品图片）
- [ ] 响应式适配
- [ ] 项目文档

## 功能模块规划

### 前端页面

| 路由 | 页面 | 功能 |
|------|------|------|
| / | 首页 | 滚动宣传图、千古名句展示、古诗词超链接 |
| /publish | 发表作品 | 表单提交诗词（标题+内容+图片） |
| /gallery | 作品广场 | 浏览他人作品、评论、访问他人主页 |
| /profile | 个人主页 | 我的账号 + 我的作品（CRUD + 数据统计） |
| /about | 关于我们 | 个人信息、联系方式、版权声明 |

### 后端 API（待开发）

- POST /api/register/ — 用户注册
- POST /api/login/ — 用户登录
- POST /api/logout/ — 用户登出
- GET/PUT /api/profile/ — 个人信息管理
- GET/POST /api/works/ — 作品列表 / 创建作品
- GET/PUT/DELETE /api/works/<id>/ — 作品详情 / 修改 / 删除
- POST /api/works/<id>/comment/ — 发表评论
- GET /api/works/<id>/comments/ — 获取评论列表

### 数据库表（待设计）

- 用户表（账号 + 密码 + 个人信息）
- 作品表（标题、内容、图片、作者、阅读量、点赞数）
- 评论表（作品、评论者、内容、时间）

## 代码约定

- Python 代码遵循 PEP 8
- Vue 组件使用 <script setup> 组合式 API
- API 返回统一 JSON 格式：{ code, message, data }
- 前端 API 调用封装在 src/api/ 目录下
- 前端页面组件放在 src/views/，可复用组件放 src/components/

## 依赖清单

### Python（虚拟环境）
`
django>=6.0
django-simpleui
`

### Node（frontend/）
`json
{
  "vue": "^3.5.34",
  "vue-router": "^4.6.4",
  "axios": "^1.18.0",
  "@vitejs/plugin-vue": "^6.0.6",
  "vite": "^8.0.12"
}
`

## 当前运行状态

- Django 后端已启动 ✅ (http://localhost:8000)
- Vue 前端已启动 ✅ (http://localhost:5173)
- 数据库已迁移 ✅
- 管理员已创建 ✅
