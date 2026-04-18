# 🚀 不认命 App - 部署指南

**版本:** 1.0.0  
**更新时间:** 2026-04-16  
**目标:** 快速部署上线

---

## 📋 部署清单

### 阶段 1: 准备工作
- [ ] 购买域名
- [ ] 购买云服务器
- [ ] 配置 DNS
- [ ] 准备 API 凭证（飞书、高德地图等）

### 阶段 2: 服务器部署
- [ ] 安装 Python 3.9+
- [ ] 安装 PostgreSQL
- [ ] 安装 Nginx
- [ ] 配置 SSL 证书

### 阶段 3: 应用部署
- [ ] 上传代码
- [ ] 安装依赖
- [ ] 配置环境变量
- [ ] 启动服务

### 阶段 4: 前端部署
- [ ] 部署到 Vercel
- [ ] 绑定域名
- [ ] 配置 API 地址

### 阶段 5: 测试上线
- [ ] 功能测试
- [ ] 性能测试
- [ ] 正式上线

---

## 🛒 采购清单

### 域名（约 50 元/年）
推荐选项：
1. `buming.app` - 简洁好记
2. `buminglife.com` - 含义明确
3. `5ming.com` - 简短
4. `buming8.com` - 吉利数字

**购买平台:**
- 阿里云：https://wanwang.aliyun.com/domain
- 腾讯云：https://cloud.tencent.com/product/domain
- GoDaddy：https://www.godaddy.com

### 云服务器（约 100 元/月）
**推荐配置:**
- CPU: 2 核
- 内存：4GB
- 硬盘：40GB SSD
- 带宽：3Mbps

**推荐平台:**
- 阿里云 ECS：https://www.aliyun.com/product/ecs
  - 入门级：约 99 元/月
- 腾讯云 CVM：https://cloud.tencent.com/product/cvm
  - 入门级：约 88 元/月
- 华为云：https://www.huaweicloud.com/product/ecs.html
  - 入门级：约 95 元/月

### 其他服务（免费）
- Vercel 前端托管：免费版足够
- Let's Encrypt SSL 证书：免费
- 高德地图 API：免费额度足够

---

## 💻 服务器配置

### 系统要求
- 操作系统：Ubuntu 20.04 LTS 或 CentOS 7+
- Python: 3.9+
- PostgreSQL: 12+
- Nginx: 1.18+

### 安装步骤

#### 1. 基础环境
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.9
sudo apt install python3.9 python3.9-venv python3-pip -y

# 安装 PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# 安装 Nginx
sudo apt install nginx -y

# 安装 Git
sudo apt install git -y
```

#### 2. 配置 PostgreSQL
```bash
# 启动 PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 创建数据库
sudo -u postgres psql
CREATE DATABASE buming;
CREATE USER buming_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE buming TO buming_user;
\q
```

#### 3. 部署应用
```bash
# 创建应用目录
mkdir -p /var/www/buming
cd /var/www/buming

# 克隆代码（或上传）
git clone <your_repo_url> .

# 创建虚拟环境
python3.9 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 4. 配置 Nginx
```nginx
server {
    listen 80;
    server_name buming.app www.buming.app;
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /var/www/buming/static;
    }
}
```

#### 5. 配置 SSL（Let's Encrypt）
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d buming.app -d www.buming.app

# 自动续期
sudo certbot renew --dry-run
```

#### 6. 启动服务
```bash
# 使用 systemd 管理服务
sudo nano /etc/systemd/system/buming.service
```

```ini
[Unit]
Description=BuMing App API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/buming
ExecStart=/var/www/buming/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl start buming
sudo systemctl enable buming
sudo systemctl status buming
```

---

## 🌐 Vercel 前端部署

### 1. 注册 Vercel
访问：https://vercel.com/signup

### 2. 连接 GitHub
- 登录 Vercel
- 点击 "New Project"
- 选择 GitHub 仓库

### 3. 配置项目
```
Name: buming-app
Framework: Other
Build Command: 留空
Output Directory: web_test
Install Command: 留空
```

### 4. 环境变量
```
API_URL=https://api.buming.app
```

### 5. 部署
- 点击 "Deploy"
- 等待部署完成
- 绑定自定义域名

---

## 📊 性能优化

### 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_temples_province ON temples(province);
CREATE INDEX idx_temples_type ON temples(type);
CREATE INDEX idx_temples_rating ON temples(rating);
```

### 缓存配置（Redis）
```bash
# 安装 Redis
sudo apt install redis-server -y

# 配置缓存
# 在 app.py 中添加 Redis 缓存
```

### CDN 加速
- 使用 Cloudflare 免费 CDN
- 静态资源托管到 CDN

---

## 🔒 安全配置

### 防火墙
```bash
# 配置 UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 定期备份
```bash
# 创建备份脚本
#!/bin/bash
pg_dump -U buming_user buming > /backup/buming_$(date +%Y%m%d).sql
```

### 监控告警
- 使用 Uptime Robot 监控网站可用性
- 配置邮件告警

---

## 📱 上线检查清单

### 功能测试
- [ ] 八字计算正常
- [ ] 寺庙匹配正常
- [ ] 法器推荐正常
- [ ] 地图显示正常
- [ ] 收藏功能正常

### 性能测试
- [ ] 页面加载 < 3 秒
- [ ] API 响应 < 1 秒
- [ ] 并发支持 100+ 用户

### 兼容性测试
- [ ] Chrome 浏览器
- [ ] Safari 浏览器
- [ ] Firefox 浏览器
- [ ] 移动端适配

### 合规检查
- [ ] 免责声明已添加
- [ ] 用户协议已添加
- [ ] 隐私政策已添加
- [ ] ICP 备案（如需要）

---

## 💰 成本预估

| 项目 | 费用 | 周期 |
|------|------|------|
| 域名 | 50 元 | 1 年 |
| 云服务器 | 100 元 | 1 月 |
| SSL 证书 | 0 元 | 永久 |
| Vercel | 0 元 | 永久 |
| CDN | 0 元 | 免费额度 |
| **首月总计** | **150 元** | - |
| **后续每月** | **100 元** | - |

---

## 📞 技术支持

遇到问题？
- 查看日志：`journalctl -u buming -f`
- 重启服务：`sudo systemctl restart buming`
- 查看状态：`sudo systemctl status buming`

---

**程序虾 🦐🔧** 2026-04-16
