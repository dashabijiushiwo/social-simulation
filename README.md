# 🌐 多维社会模拟系统

一个基于智能体的多维社会模拟系统，用于研究社会结构演化和群体行为模式。

## 🚀 在线体验

**立即访问**: [https://social-simulation.streamlit.app](https://social-simulation.streamlit.app)

> 无需安装，直接在浏览器中体验完整功能！

## ✨ 功能特点

- 🧠 **智能体行为模拟** - 基于复杂系统理论的个体行为建模
- 📊 **实时数据可视化** - 动态图表展示模拟过程
- 🔄 **多维度对比分析** - 不同参数设置的对比研究
- 📈 **社会结构演化追踪** - 长期趋势和模式识别
- 🎯 **交互式参数调节** - 实时调整模拟参数
- 📱 **响应式设计** - 支持桌面和移动设备

## 🚀 快速开始

### 方法一：自动启动（推荐）
1. 双击运行 `social9.0/自动启动器.bat`
2. 系统会自动检测Python环境并安装依赖
3. 启动成功后会自动打开浏览器

### 方法二：手动启动
1. 双击运行 `social9.0/手动启动器.bat`
2. 根据提示选择安装依赖的方式
3. 启动成功后访问显示的网址

### 方法三：命令行启动
```bash
cd social9.0
pip install -r ../requirements.txt
streamlit run main.py
```

## 📁 项目结构

```
social9.0/
├── README.md                 # 项目说明文件
├── requirements.txt          # 依赖包列表
├── 手动安装指南.md           # 详细安装指南
└── social9.0/               # 主程序目录
    ├── main.py              # 主程序入口
    ├── 自动启动器.bat        # 自动安装并启动
    ├── 手动启动器.bat        # 手动启动选项
    ├── 使用说明.md          # 使用说明
    ├── .streamlit/          # Streamlit配置
    │   └── config.toml
    ├── core/                # 核心模拟逻辑
    │   ├── agent.py         # 个体代理类
    │   ├── society.py       # 社会状态管理
    │   └── simulation.py    # 模拟引擎
    └── ui/                  # 用户界面组件
        ├── config_panel.py      # 配置面板
        ├── macro_dashboard.py   # 宏观仪表盘
        ├── comparison_panel.py  # 对比面板
        ├── elite_panel.py       # 精英分析面板
        └── rules_panel.py       # 规则面板
```

## 🔧 系统要求

- **Python版本**: 3.8 - 3.11 (推荐3.9)
- **操作系统**: Windows 10/11
- **内存**: 建议4GB以上
- **网络**: 首次运行需要网络连接下载依赖

## 📦 核心依赖

- `streamlit` - Web界面框架
- `numpy` - 数值计算
- `pandas` - 数据处理
- `plotly` - 交互式图表

## ⚠️ 常见问题

### 1. 依赖安装失败
**现象**: 出现编译错误或网络超时
**解决**: 查看 `手动安装指南.md` 获取详细解决方案

### 2. 端口被占用
**现象**: 提示端口8501被占用
**解决**: 启动器会自动寻找可用端口(8501-8510)

### 3. Python环境问题
**现象**: 找不到Python命令
**解决**: 
- 确保Python已正确安装
- 检查环境变量PATH设置
- 尝试使用自动启动器的Python安装功能

### 4. 权限问题
**现象**: 拒绝访问或权限不足
**解决**: 以管理员身份运行启动器

## 🛠️ 手动安装依赖

如果自动安装失败，可以手动安装：

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装核心包（避免编译错误）
python -m pip install --upgrade --only-binary=all numpy pandas

# 安装其他依赖
python -m pip install streamlit plotly
```

## 🌐 使用镜像源（中国用户）

```bash
# 清华大学镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 阿里云镜像
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

## 📞 技术支持

如果遇到问题：
1. 首先查看 `手动安装指南.md`
2. 检查Python版本和环境配置
3. 尝试使用不同的启动方式
4. 提供错误信息截图以获得更好的帮助

## 📄 许可证

本项目仅供学习和研究使用。

---

**提示**: 首次运行建议使用 `自动启动器.bat`，它会自动处理大部分环境配置问题。