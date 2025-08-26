import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def render_comparison_panel(simulation_data: Dict[str, Any]):
    """
    渲染实时对比面板
    
    Args:
        simulation_data: 模拟数据字典
    """
    if not simulation_data or 'rounds' not in simulation_data or len(simulation_data['rounds']) < 2:
        st.warning("📊 请先运行模拟以查看对比数据")
        return
    
    st.header("🔍 实时对比面板")
    st.markdown("对任意轮次的社会状态进行精细的群体间横向对比")
    
    rounds_data = simulation_data['rounds']
    max_round = len(rounds_data) - 1
    
    # 轮次选择器
    selected_round = render_round_selector(max_round)
    
    if selected_round is None or selected_round >= len(rounds_data):
        st.error("选择的轮次无效")
        return
    
    # 获取选中轮次的数据
    round_data = rounds_data[selected_round]
    
    # 群体指标对比卡
    render_group_comparison_cards(round_data)
    
    # 群体内部分布图
    render_group_distribution_charts(round_data)
    
    # 核心圈构成分析
    render_core_circle_analysis(round_data)
    
    # 详细统计表
    render_detailed_statistics(round_data)

def render_round_selector(max_round: int) -> int:
    """渲染轮次选择器"""
    st.subheader("🎯 轮次选择")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_round = st.slider(
            "选择要分析的轮次",
            min_value=0,
            max_value=max_round,
            value=max_round,
            step=1,
            help="拖动滑块或使用方向键选择轮次"
        )
    
    with col2:
        # 数字输入框
        input_round = st.number_input(
            "直接输入轮次",
            min_value=0,
            max_value=max_round,
            value=selected_round,
            step=1
        )
        
        if input_round != selected_round:
            selected_round = input_round
            st.rerun()
    
    # 快速跳转按钮
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📍 初始状态", use_container_width=True):
            st.session_state.selected_round = 0
            st.rerun()
    
    with col2:
        if st.button("📊 25%进度", use_container_width=True):
            st.session_state.selected_round = max_round // 4
            st.rerun()
    
    with col3:
        if st.button("🎯 50%进度", use_container_width=True):
            st.session_state.selected_round = max_round // 2
            st.rerun()
    
    with col4:
        if st.button("🏁 最终状态", use_container_width=True):
            st.session_state.selected_round = max_round
            st.rerun()
    
    # 检查session state
    if 'selected_round' in st.session_state:
        selected_round = st.session_state.selected_round
        del st.session_state.selected_round
    
    return selected_round

def render_group_comparison_cards(round_data: Dict[str, Any]):
    """渲染群体指标对比卡"""
    st.subheader("👥 群体指标对比")
    
    gender_stats = round_data.get('gender_stats', {})
    
    if not gender_stats:
        st.warning("缺少性别统计数据")
        return
    
    # 创建对比卡片
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨 男性群体")
        male_stats = gender_stats.get('male', {})
        
        # 男性指标
        male_metrics = [
            ("平均权力", male_stats.get('avg_power', 0), "💪"),
            ("平均财富", male_stats.get('avg_wealth', 0), "💰"),
            ("平均关怀技能", male_stats.get('avg_care_skill', 0), "❤️"),
            ("平均竞争技能", male_stats.get('avg_competition_skill', 0), "⚔️")
        ]
        
        for label, value, icon in male_metrics:
            st.metric(
                f"{icon} {label}",
                f"{value:.3f}",
                help=f"男性群体的{label}"
            )
    
    with col2:
        st.markdown("### 👩 女性群体")
        female_stats = gender_stats.get('female', {})
        
        # 女性指标
        female_metrics = [
            ("平均权力", female_stats.get('avg_power', 0), "💪"),
            ("平均财富", female_stats.get('avg_wealth', 0), "💰"),
            ("平均关怀技能", female_stats.get('avg_care_skill', 0), "❤️"),
            ("平均竞争技能", female_stats.get('avg_competition_skill', 0), "⚔️")
        ]
        
        for label, value, icon in female_metrics:
            st.metric(
                f"{icon} {label}",
                f"{value:.3f}",
                help=f"女性群体的{label}"
            )
    
    # 差距分析
    st.markdown("### 📊 性别差距分析")
    
    col1, col2, col3, col4 = st.columns(4)
    
    gaps = {
        "权力差距": male_stats.get('avg_power', 0) - female_stats.get('avg_power', 0),
        "财富差距": male_stats.get('avg_wealth', 0) - female_stats.get('avg_wealth', 0),
        "关怀技能差距": male_stats.get('avg_care_skill', 0) - female_stats.get('avg_care_skill', 0),
        "竞争技能差距": male_stats.get('avg_competition_skill', 0) - female_stats.get('avg_competition_skill', 0)
    }
    
    for i, (gap_name, gap_value) in enumerate(gaps.items()):
        with [col1, col2, col3, col4][i]:
            delta_color = "inverse" if gap_value > 0 and "权力" in gap_name or "财富" in gap_name else "normal"
            st.metric(
                gap_name,
                f"{gap_value:+.3f}",
                delta="男性优势" if gap_value > 0 else "女性优势" if gap_value < 0 else "基本平等",
                delta_color=delta_color
            )

def render_group_distribution_charts(round_data: Dict[str, Any]):
    """渲染群体内部分布图"""
    st.subheader("📈 群体内部分布分析")
    
    # 准备个体数据
    agents_data = round_data.get('agents', [])
    
    if not agents_data:
        st.warning("缺少个体数据")
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(agents_data)
    
    if df.empty:
        st.warning("个体数据为空")
        return
    
    # 权力分布对比
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💪 权力分布对比")
        render_violin_plot(df, 'power', '权力分布')
    
    with col2:
        st.markdown("#### 💰 财富分布对比")
        render_violin_plot(df, 'wealth', '财富分布')
    
    # 技能分布对比
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ❤️ 关怀技能分布")
        render_violin_plot(df, 'care_skill', '关怀技能分布')
    
    with col2:
        st.markdown("#### ⚔️ 竞争技能分布")
        render_violin_plot(df, 'competition_skill', '竞争技能分布')
    
    # 分布统计摘要
    render_distribution_summary(df)

def render_violin_plot(df: pd.DataFrame, column: str, title: str):
    """渲染小提琴图"""
    fig = go.Figure()
    
    # 男性分布
    male_data = df[df['gender'] == 'male'][column]
    fig.add_trace(go.Violin(
        y=male_data,
        name='男性',
        side='negative',
        fillcolor='lightblue',
        line_color='blue',
        box_visible=True,
        meanline_visible=True
    ))
    
    # 女性分布
    female_data = df[df['gender'] == 'female'][column]
    fig.add_trace(go.Violin(
        y=female_data,
        name='女性',
        side='positive',
        fillcolor='lightpink',
        line_color='red',
        box_visible=True,
        meanline_visible=True
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title=column,
        violinmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_distribution_summary(df: pd.DataFrame):
    """渲染分布统计摘要"""
    st.markdown("#### 📊 分布统计摘要")
    
    # 计算统计指标
    stats_data = []
    
    for gender in ['male', 'female']:
        gender_df = df[df['gender'] == gender]
        
        for column in ['power', 'wealth', 'care_skill', 'competition_skill']:
            if column in gender_df.columns:
                data = gender_df[column]
                stats_data.append({
                    '性别': '男性' if gender == 'male' else '女性',
                    '指标': column,
                    '均值': data.mean(),
                    '中位数': data.median(),
                    '标准差': data.std(),
                    '最小值': data.min(),
                    '最大值': data.max(),
                    '四分位距': data.quantile(0.75) - data.quantile(0.25)
                })
    
    if stats_data:
        stats_df = pd.DataFrame(stats_data)
        
        # 格式化数值
        numeric_columns = ['均值', '中位数', '标准差', '最小值', '最大值', '四分位距']
        for col in numeric_columns:
            stats_df[col] = stats_df[col].round(3)
        
        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True
        )

def render_core_circle_analysis(round_data: Dict[str, Any]):
    """渲染核心圈构成分析"""
    st.subheader("👑 核心决策圈构成")
    
    core_circle = round_data.get('core_decision_circle', [])
    
    if not core_circle:
        st.warning("核心决策圈数据缺失")
        return
    
    # 统计核心圈构成
    gender_count = {'male': 0, 'female': 0}
    ideology_count = {'F': 0, 'P': 0, 'U': 0}
    class_count = {'low': 0, 'middle': 0, 'high': 0}
    
    for member in core_circle:
        gender_count[member.get('gender', 'unknown')] += 1
        ideology_count[member.get('ideology', 'U')] += 1
        class_count[member.get('class_level', 'middle')] += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 性别构成饼图
        st.markdown("##### 👥 性别构成")
        
        fig_gender = go.Figure(data=[go.Pie(
            labels=['男性', '女性'],
            values=[gender_count['male'], gender_count['female']],
            hole=0.4,
            marker_colors=['lightblue', 'lightpink']
        )])
        
        fig_gender.update_layout(
            title="核心圈性别比例",
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # 意识形态构成饼图
        st.markdown("##### 🧠 意识形态构成")
        
        ideology_labels = ['女性主义', '父权捍卫', '功利主义']
        ideology_values = [ideology_count['F'], ideology_count['P'], ideology_count['U']]
        
        fig_ideology = go.Figure(data=[go.Pie(
            labels=ideology_labels,
            values=ideology_values,
            hole=0.4,
            marker_colors=['pink', 'lightblue', 'lightgreen']
        )])
        
        fig_ideology.update_layout(
            title="核心圈意识形态分布",
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_ideology, use_container_width=True)
    
    # 阶层构成条形图
    st.markdown("##### 🏛️ 阶层构成")
    
    class_labels = ['低阶层', '中阶层', '高阶层']
    class_values = [class_count['low'], class_count['middle'], class_count['high']]
    
    fig_class = go.Figure(data=[go.Bar(
        x=class_labels,
        y=class_values,
        marker_color=['lightcoral', 'lightyellow', 'lightgreen']
    )])
    
    fig_class.update_layout(
        title="核心圈阶层分布",
        xaxis_title="阶层",
        yaxis_title="人数",
        height=300
    )
    
    st.plotly_chart(fig_class, use_container_width=True)
    
    # 核心圈成员详情
    with st.expander("👑 核心圈成员详情", expanded=False):
        render_core_circle_details(core_circle)

def render_core_circle_details(core_circle: List[Dict]):
    """渲染核心圈成员详情"""
    if not core_circle:
        st.info("核心圈为空")
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(core_circle)
    
    # 选择要显示的列
    display_columns = ['gender', 'class_level', 'ideology', 'power', 'wealth', 'care_skill', 'competition_skill']
    available_columns = [col for col in display_columns if col in df.columns]
    
    if available_columns:
        # 重命名列
        column_names = {
            'gender': '性别',
            'class_level': '阶层',
            'ideology': '意识形态',
            'power': '权力',
            'wealth': '财富',
            'care_skill': '关怀技能',
            'competition_skill': '竞争技能'
        }
        
        display_df = df[available_columns].copy()
        
        # 转换性别显示
        if 'gender' in display_df.columns:
            display_df['gender'] = display_df['gender'].map({'male': '男性', 'female': '女性'})
        
        # 转换阶层显示
        if 'class_level' in display_df.columns:
            display_df['class_level'] = display_df['class_level'].map({
                'low': '低阶层', 'middle': '中阶层', 'high': '高阶层'
            })
        
        # 重命名列
        display_df = display_df.rename(columns=column_names)
        
        # 格式化数值列
        numeric_columns = ['权力', '财富', '关怀技能', '竞争技能']
        for col in numeric_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].round(3)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("核心圈数据格式异常")

def render_detailed_statistics(round_data: Dict[str, Any]):
    """渲染详细统计信息"""
    with st.expander("📋 详细统计信息", expanded=False):
        st.subheader("📊 当前轮次统计摘要")
        
        # 基本统计
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("当前轮次", round_data.get('current_round', 0))
            st.metric("社会平等指数", f"{round_data.get('social_equality', 0):.3f}")
        
        with col2:
            st.metric("平均权力", f"{round_data.get('average_power', 0):.3f}")
            st.metric("平均财富", f"{round_data.get('average_wealth', 0):.3f}")
        
        with col3:
            st.metric("平均意识形态", f"{round_data.get('average_ideology', 0):.3f}")
            core_circle_size = len(round_data.get('core_decision_circle', []))
            st.metric("核心圈规模", core_circle_size)
        
        # 政策杠杆状态
        st.subheader("🎛️ 当前政策杠杆")
        
        policy_levers = round_data.get('policy_levers', {})
        if policy_levers:
            policy_df = pd.DataFrame([
                {'政策': '竞争回报', '数值': policy_levers.get('competition_reward', 0)},
                {'政策': '关怀回报', '数值': policy_levers.get('care_reward', 0)},
                {'政策': '税收再分配', '数值': policy_levers.get('tax_redistribution', 0)},
                {'政策': '功劳归因偏置', '数值': policy_levers.get('attribution_bias', 0)},
                {'政策': '社会制裁强度', '数值': policy_levers.get('social_sanction', 0)}
            ])
            
            policy_df['数值'] = policy_df['数值'].round(3)
            
            st.dataframe(
                policy_df,
                use_container_width=True,
                hide_index=True
            )
        
        # 意识形态统计
        st.subheader("🧠 意识形态分布")
        
        ideology_stats = round_data.get('ideology_stats', {})
        if ideology_stats:
            ideology_data = []
            for ideology, stats in ideology_stats.items():
                ideology_name = {'F': '女性主义', 'P': '父权捍卫', 'U': '功利主义'}.get(ideology, ideology)
                ideology_data.append({
                    '意识形态': ideology_name,
                    '人数': stats.get('count', 0),
                    '比例': f"{stats.get('ratio', 0):.1%}",
                    '平均权力': f"{stats.get('avg_power', 0):.3f}",
                    '平均财富': f"{stats.get('avg_wealth', 0):.3f}"
                })
            
            ideology_df = pd.DataFrame(ideology_data)
            
            st.dataframe(
                ideology_df,
                use_container_width=True,
                hide_index=True
            )