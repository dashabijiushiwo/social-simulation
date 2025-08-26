import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime

# 导入自定义模块
from core.agent import Agent
from core.society import SocietyState
from core.simulation import SocialSimulation
from ui.config_panel import render_config_panel
from ui.macro_dashboard import render_macro_dashboard
from ui.comparison_panel import render_comparison_panel
from ui.elite_panel import render_elite_panel
from ui.rules_panel import render_rules_panel

# 页面配置
st.set_page_config(
    page_title="多维社会模拟实验",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主标题
st.title("🏛️ 多维社会模拟实验系统")
st.markdown("---")

# 侧边栏导航
st.sidebar.title("📊 导航面板")
page = st.sidebar.selectbox(
    "选择功能模块",
    ["规则介绍", "参数配置", "宏观趋势仪表盘", "实时对比面板", "核心圈演变分析"]
)

# 初始化session state
if 'simulation' not in st.session_state:
    st.session_state.simulation = None
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = None
if 'config' not in st.session_state:
    st.session_state.config = None

# 渲染对应页面
if page == "规则介绍":
    render_rules_panel()
    
elif page == "参数配置":
    render_config_panel()
    
elif page == "宏观趋势仪表盘":
    if st.session_state.simulation_data is None:
        st.warning("⚠️ 请先在参数配置页面运行模拟实验")
    else:
        render_macro_dashboard(st.session_state.simulation_data)
        
elif page == "实时对比面板":
    if st.session_state.simulation_data is None:
        st.warning("⚠️ 请先在参数配置页面运行模拟实验")
    else:
        render_comparison_panel(st.session_state.simulation_data)
        
elif page == "核心圈演变分析":
    if st.session_state.simulation_data is None:
        st.warning("⚠️ 请先在参数配置页面运行模拟实验")
    else:
        render_elite_panel(st.session_state.simulation_data)

# 页脚信息
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 系统信息")
if st.session_state.simulation_data is not None:
    data = st.session_state.simulation_data
    st.sidebar.info(f"""
    **模拟状态**: 已完成
    **总轮数**: {len(data['rounds']) - 1}
    **社会人数**: {len(data['rounds'][0]['agents'])}
    **最终平等指数**: {data['rounds'][-1]['social_equality']:.3f}
    """)
else:
    st.sidebar.info("**模拟状态**: 未运行")

if __name__ == "__main__":
    pass