import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def render_elite_panel(simulation_data: Dict[str, Any]):
    """
    渲染核心圈演变分析面板
    
    Args:
        simulation_data: 模拟数据字典
    """
    if not simulation_data or 'rounds' not in simulation_data or len(simulation_data['rounds']) < 2:
        st.warning("📊 请先运行模拟以查看核心圈演变数据")
        return
    
    st.header("👑 核心圈演变分析")
    st.markdown("专门剖析社会权力顶层的动态变化，揭示规则变革的驱动引擎")
    
    rounds_data = simulation_data['rounds']
    
    # 准备核心圈演变数据
    elite_df = prepare_elite_evolution_data(rounds_data)
    
    if elite_df.empty:
        st.warning("核心圈数据不足，无法进行演变分析")
        return
    
    # 核心圈组成演变图
    render_elite_composition_evolution(elite_df)
    
    # 政策杠杆变迁图
    render_policy_levers_evolution(rounds_data)
    
    # 权力集中度分析
    render_power_concentration_analysis(elite_df)
    
    # 核心圈稳定性分析
    render_elite_stability_analysis(rounds_data)

def prepare_elite_evolution_data(rounds_data: List[Dict]) -> pd.DataFrame:
    """准备核心圈演变数据"""
    data = []
    
    for round_num, round_data in enumerate(rounds_data):
        core_circle = round_data.get('core_decision_circle', [])
        
        if not core_circle:
            # 如果没有核心圈数据，跳过或使用默认值
            continue
        
        # 统计性别构成
        male_count = sum(1 for member in core_circle if member.get('gender') == 'male')
        female_count = sum(1 for member in core_circle if member.get('gender') == 'female')
        total_members = len(core_circle)
        
        # 统计意识形态构成
        f_count = sum(1 for member in core_circle if member.get('ideology') == 'F')
        p_count = sum(1 for member in core_circle if member.get('ideology') == 'P')
        u_count = sum(1 for member in core_circle if member.get('ideology') == 'U')
        
        # 统计阶层构成
        low_count = sum(1 for member in core_circle if member.get('class_level') == 'low')
        middle_count = sum(1 for member in core_circle if member.get('class_level') == 'middle')
        high_count = sum(1 for member in core_circle if member.get('class_level') == 'high')
        
        # 计算平均指标
        avg_power = np.mean([member.get('power', 0) for member in core_circle]) if core_circle else 0
        avg_wealth = np.mean([member.get('wealth', 0) for member in core_circle]) if core_circle else 0
        avg_care_skill = np.mean([member.get('care_skill', 0) for member in core_circle]) if core_circle else 0
        avg_competition_skill = np.mean([member.get('competition_skill', 0) for member in core_circle]) if core_circle else 0
        
        row = {
            'round': round_num,
            'total_members': total_members,
            
            # 性别构成
            'male_count': male_count,
            'female_count': female_count,
            'male_ratio': male_count / total_members if total_members > 0 else 0,
            'female_ratio': female_count / total_members if total_members > 0 else 0,
            
            # 意识形态构成
            'f_count': f_count,
            'p_count': p_count,
            'u_count': u_count,
            'f_ratio': f_count / total_members if total_members > 0 else 0,
            'p_ratio': p_count / total_members if total_members > 0 else 0,
            'u_ratio': u_count / total_members if total_members > 0 else 0,
            
            # 阶层构成
            'low_count': low_count,
            'middle_count': middle_count,
            'high_count': high_count,
            'low_ratio': low_count / total_members if total_members > 0 else 0,
            'middle_ratio': middle_count / total_members if total_members > 0 else 0,
            'high_ratio': high_count / total_members if total_members > 0 else 0,
            
            # 平均指标
            'avg_power': avg_power,
            'avg_wealth': avg_wealth,
            'avg_care_skill': avg_care_skill,
            'avg_competition_skill': avg_competition_skill
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

def render_elite_composition_evolution(elite_df: pd.DataFrame):
    """渲染核心圈组成演变图"""
    st.subheader("📊 核心圈组成演变")
    
    # 选择分析维度
    analysis_dimension = st.selectbox(
        "选择分析维度",
        ["性别构成", "意识形态构成", "阶层构成"],
        help="选择要分析的核心圈构成维度"
    )
    
    if analysis_dimension == "性别构成":
        render_gender_composition_chart(elite_df)
    elif analysis_dimension == "意识形态构成":
        render_ideology_composition_chart(elite_df)
    else:
        render_class_composition_chart(elite_df)
    
    # 核心圈规模变化
    render_elite_size_evolution(elite_df)

def render_gender_composition_chart(elite_df: pd.DataFrame):
    """渲染性别构成演变图"""
    st.markdown("#### 👥 性别构成演变")
    
    fig = go.Figure()
    
    # 男性比例
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['male_ratio'],
        fill='tonexty',
        mode='none',
        name='男性',
        fillcolor='rgba(135, 206, 250, 0.7)',
        hovertemplate='轮次: %{x}<br>男性比例: %{y:.1%}<extra></extra>'
    ))
    
    # 女性比例
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['male_ratio'] + elite_df['female_ratio'],
        fill='tonexty',
        mode='none',
        name='女性',
        fillcolor='rgba(255, 182, 193, 0.7)',
        hovertemplate='轮次: %{x}<br>女性比例: %{y:.1%}<extra></extra>'
    ))
    
    # 添加边界线
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['male_ratio'],
        mode='lines',
        line=dict(color='#4169E1', width=2),
        name='男性边界',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['male_ratio'] + elite_df['female_ratio'],
        mode='lines',
        line=dict(color='#FF69B4', width=2),
        name='女性边界',
        showlegend=False
    ))
    
    # 添加平等线
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", 
                  annotation_text="性别平等线")
    
    fig.update_layout(
        title="核心圈性别构成演变",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="比例",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 性别构成分析
    analyze_gender_evolution(elite_df)

def render_ideology_composition_chart(elite_df: pd.DataFrame):
    """渲染意识形态构成演变图"""
    st.markdown("#### 🧠 意识形态构成演变")
    
    fig = go.Figure()
    
    # 女性主义
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['f_ratio'],
        fill='tonexty',
        mode='none',
        name='女性主义 (F)',
        fillcolor='rgba(255, 182, 193, 0.7)',
        hovertemplate='轮次: %{x}<br>女性主义比例: %{y:.1%}<extra></extra>'
    ))
    
    # 父权捍卫
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['f_ratio'] + elite_df['p_ratio'],
        fill='tonexty',
        mode='none',
        name='父权捍卫 (P)',
        fillcolor='rgba(135, 206, 250, 0.7)',
        hovertemplate='轮次: %{x}<br>父权捍卫比例: %{y:.1%}<extra></extra>'
    ))
    
    # 功利主义
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['f_ratio'] + elite_df['p_ratio'] + elite_df['u_ratio'],
        fill='tonexty',
        mode='none',
        name='功利主义 (U)',
        fillcolor='rgba(144, 238, 144, 0.7)',
        hovertemplate='轮次: %{x}<br>功利主义比例: %{y:.1%}<extra></extra>'
    ))
    
    # 添加边界线
    colors = ['#FF69B4', '#4169E1', '#32CD32']
    ratios = ['f_ratio', 'p_ratio', 'u_ratio']
    
    for i, (ratio, color) in enumerate(zip(ratios, colors)):
        if i == 0:
            y_data = elite_df[ratio]
        elif i == 1:
            y_data = elite_df['f_ratio'] + elite_df[ratio]
        else:
            y_data = elite_df['f_ratio'] + elite_df['p_ratio'] + elite_df[ratio]
            
        fig.add_trace(go.Scatter(
            x=elite_df['round'],
            y=y_data,
            mode='lines',
            line=dict(color=color, width=2),
            name=f'{ratio} 边界',
            showlegend=False
        ))
    
    fig.update_layout(
        title="核心圈意识形态构成演变",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="比例",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 意识形态演变分析
    analyze_ideology_evolution(elite_df)

def render_class_composition_chart(elite_df: pd.DataFrame):
    """渲染阶层构成演变图"""
    st.markdown("#### 🏛️ 阶层构成演变")
    
    fig = go.Figure()
    
    # 低阶层
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['low_ratio'],
        fill='tonexty',
        mode='none',
        name='低阶层',
        fillcolor='rgba(255, 160, 122, 0.7)',
        hovertemplate='轮次: %{x}<br>低阶层比例: %{y:.1%}<extra></extra>'
    ))
    
    # 中阶层
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['low_ratio'] + elite_df['middle_ratio'],
        fill='tonexty',
        mode='none',
        name='中阶层',
        fillcolor='rgba(255, 255, 224, 0.7)',
        hovertemplate='轮次: %{x}<br>中阶层比例: %{y:.1%}<extra></extra>'
    ))
    
    # 高阶层
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['low_ratio'] + elite_df['middle_ratio'] + elite_df['high_ratio'],
        fill='tonexty',
        mode='none',
        name='高阶层',
        fillcolor='rgba(144, 238, 144, 0.7)',
        hovertemplate='轮次: %{x}<br>高阶层比例: %{y:.1%}<extra></extra>'
    ))
    
    fig.update_layout(
        title="核心圈阶层构成演变",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="比例",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_elite_size_evolution(elite_df: pd.DataFrame):
    """渲染核心圈规模演变"""
    st.markdown("#### 📏 核心圈规模演变")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=elite_df['round'],
        y=elite_df['total_members'],
        mode='lines+markers',
        name='核心圈规模',
        line=dict(color='#2E8B57', width=3),
        marker=dict(size=6),
        hovertemplate='轮次: %{x}<br>核心圈规模: %{y}人<extra></extra>'
    ))
    
    # 添加平均线
    avg_size = elite_df['total_members'].mean()
    fig.add_hline(y=avg_size, line_dash="dash", line_color="gray", 
                  annotation_text=f"平均规模: {avg_size:.1f}人")
    
    fig.update_layout(
        title="核心圈规模变化趋势",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="核心圈成员数量",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_policy_levers_evolution(rounds_data: List[Dict]):
    """渲染政策杠杆变迁图"""
    st.subheader("🎛️ 政策杠杆变迁")
    
    # 准备政策数据
    policy_data = []
    
    for round_num, round_data in enumerate(rounds_data):
        policy_levers = round_data.get('policy_levers', {})
        
        row = {
            'round': round_num,
            'competition_reward': policy_levers.get('competition_reward', 1.0),
            'care_reward': policy_levers.get('care_reward', 1.0),
            'tax_redistribution': policy_levers.get('tax_redistribution', 0.2),
            'attribution_bias': policy_levers.get('attribution_bias', 0.0),
            'social_sanction': policy_levers.get('social_sanction', 0.3)
        }
        
        policy_data.append(row)
    
    if not policy_data:
        st.warning("缺少政策杠杆数据")
        return
    
    policy_df = pd.DataFrame(policy_data)
    
    # 创建多线图
    fig = go.Figure()
    
    # 政策线条配置
    policies = [
        ('competition_reward', '竞争回报', '#FF6B6B'),
        ('care_reward', '关怀回报', '#4ECDC4'),
        ('tax_redistribution', '税收再分配', '#45B7D1'),
        ('attribution_bias', '功劳归因偏置', '#96CEB4'),
        ('social_sanction', '社会制裁强度', '#FFEAA7')
    ]
    
    for policy_key, policy_name, color in policies:
        if policy_key in policy_df.columns:
            fig.add_trace(go.Scatter(
                x=policy_df['round'],
                y=policy_df[policy_key],
                mode='lines+markers',
                name=policy_name,
                line=dict(color=color, width=2),
                marker=dict(size=4),
                hovertemplate=f'轮次: %{{x}}<br>{policy_name}: %{{y:.3f}}<extra></extra>'
            ))
    
    fig.update_layout(
        title="政策杠杆数值变化趋势",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="政策数值",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 政策变化分析
    analyze_policy_changes(policy_df)

def render_power_concentration_analysis(elite_df: pd.DataFrame):
    """渲染权力集中度分析"""
    st.subheader("⚡ 权力集中度分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 核心圈平均权力趋势
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=elite_df['round'],
            y=elite_df['avg_power'],
            mode='lines+markers',
            name='核心圈平均权力',
            line=dict(color='#DC143C', width=3),
            marker=dict(size=6),
            hovertemplate='轮次: %{x}<br>平均权力: %{y:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="核心圈平均权力演变",
            title_x=0.5,
            xaxis_title="模拟轮次",
            yaxis_title="平均权力",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 核心圈平均财富趋势
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=elite_df['round'],
            y=elite_df['avg_wealth'],
            mode='lines+markers',
            name='核心圈平均财富',
            line=dict(color='#FF8C00', width=3),
            marker=dict(size=6),
            hovertemplate='轮次: %{x}<br>平均财富: %{y:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="核心圈平均财富演变",
            title_x=0.5,
            xaxis_title="模拟轮次",
            yaxis_title="平均财富",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 技能构成分析
    render_elite_skills_analysis(elite_df)

def render_elite_skills_analysis(elite_df: pd.DataFrame):
    """渲染核心圈技能分析"""
    st.markdown("#### 🎯 核心圈技能构成")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('关怀技能演变', '竞争技能演变'),
        shared_xaxes=True
    )
    
    # 关怀技能
    fig.add_trace(
        go.Scatter(
            x=elite_df['round'],
            y=elite_df['avg_care_skill'],
            mode='lines+markers',
            name='平均关怀技能',
            line=dict(color='#FF69B4', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # 竞争技能
    fig.add_trace(
        go.Scatter(
            x=elite_df['round'],
            y=elite_df['avg_competition_skill'],
            mode='lines+markers',
            name='平均竞争技能',
            line=dict(color='#4169E1', width=2),
            marker=dict(size=4)
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="核心圈技能构成演变",
        title_x=0.5,
        height=400,
        showlegend=False
    )
    
    fig.update_xaxes(title_text="模拟轮次")
    fig.update_yaxes(title_text="技能水平")
    
    st.plotly_chart(fig, use_container_width=True)

def render_elite_stability_analysis(rounds_data: List[Dict]):
    """渲染核心圈稳定性分析"""
    with st.expander("🔄 核心圈稳定性分析", expanded=False):
        st.subheader("核心圈成员变动分析")
        
        # 计算成员变动率
        stability_data = calculate_elite_stability(rounds_data)
        
        if stability_data:
            stability_df = pd.DataFrame(stability_data)
            
            # 成员变动率图表
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=stability_df['round'],
                y=stability_df['turnover_rate'],
                mode='lines+markers',
                name='成员变动率',
                line=dict(color='#9370DB', width=2),
                marker=dict(size=6),
                hovertemplate='轮次: %{x}<br>变动率: %{y:.1%}<extra></extra>'
            ))
            
            fig.update_layout(
                title="核心圈成员变动率",
                title_x=0.5,
                xaxis_title="模拟轮次",
                yaxis_title="变动率",
                yaxis=dict(tickformat='.0%'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 稳定性统计
            avg_turnover = stability_df['turnover_rate'].mean()
            max_turnover = stability_df['turnover_rate'].max()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("平均变动率", f"{avg_turnover:.1%}")
            
            with col2:
                st.metric("最大变动率", f"{max_turnover:.1%}")
        else:
            st.info("核心圈稳定性数据不足")

def analyze_gender_evolution(elite_df: pd.DataFrame):
    """分析性别构成演变"""
    with st.expander("👥 性别构成分析", expanded=False):
        if len(elite_df) < 5:
            st.warning("数据不足，无法进行详细分析")
            return
        
        # 计算性别比例变化
        initial_female_ratio = elite_df['female_ratio'].iloc[0]
        final_female_ratio = elite_df['female_ratio'].iloc[-1]
        female_ratio_change = final_female_ratio - initial_female_ratio
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("初始女性比例", f"{initial_female_ratio:.1%}")
        
        with col2:
            st.metric("最终女性比例", f"{final_female_ratio:.1%}")
        
        with col3:
            st.metric(
                "变化幅度", 
                f"{female_ratio_change:+.1%}",
                delta="女性进步" if female_ratio_change > 0 else "女性退步" if female_ratio_change < 0 else "基本稳定"
            )
        
        # 关键发现
        if female_ratio_change > 0.1:
            st.success("🎉 女性在核心圈中的地位显著提升")
        elif female_ratio_change < -0.1:
            st.error("⚠️ 女性在核心圈中的地位显著下降")
        else:
            st.info("ℹ️ 核心圈性别构成相对稳定")

def analyze_ideology_evolution(elite_df: pd.DataFrame):
    """分析意识形态演变"""
    with st.expander("🧠 意识形态演变分析", expanded=False):
        if len(elite_df) < 5:
            return
        
        # 计算各意识形态变化
        ideology_changes = {
            '女性主义': elite_df['f_ratio'].iloc[-1] - elite_df['f_ratio'].iloc[0],
            '父权捍卫': elite_df['p_ratio'].iloc[-1] - elite_df['p_ratio'].iloc[0],
            '功利主义': elite_df['u_ratio'].iloc[-1] - elite_df['u_ratio'].iloc[0]
        }
        
        col1, col2, col3 = st.columns(3)
        
        for i, (ideology, change) in enumerate(ideology_changes.items()):
            with [col1, col2, col3][i]:
                st.metric(
                    ideology,
                    f"{change:+.1%}",
                    delta="势力增强" if change > 0 else "势力减弱" if change < 0 else "基本稳定"
                )
        
        # 主导意识形态
        final_ratios = {
            '女性主义': elite_df['f_ratio'].iloc[-1],
            '父权捍卫': elite_df['p_ratio'].iloc[-1],
            '功利主义': elite_df['u_ratio'].iloc[-1]
        }
        
        dominant_ideology = max(final_ratios, key=final_ratios.get)
        dominant_ratio = final_ratios[dominant_ideology]
        
        st.info(f"💡 **核心圈主导意识形态**: {dominant_ideology} ({dominant_ratio:.1%})")

def analyze_policy_changes(policy_df: pd.DataFrame):
    """分析政策变化"""
    with st.expander("📊 政策变化分析", expanded=False):
        if len(policy_df) < 5:
            return
        
        # 计算各政策的变化幅度
        policy_changes = {}
        policy_names = {
            'competition_reward': '竞争回报',
            'care_reward': '关怀回报',
            'tax_redistribution': '税收再分配',
            'attribution_bias': '功劳归因偏置',
            'social_sanction': '社会制裁强度'
        }
        
        for policy_key, policy_name in policy_names.items():
            if policy_key in policy_df.columns:
                initial_value = policy_df[policy_key].iloc[0]
                final_value = policy_df[policy_key].iloc[-1]
                change = final_value - initial_value
                policy_changes[policy_name] = {
                    'initial': initial_value,
                    'final': final_value,
                    'change': change
                }
        
        # 显示政策变化
        for policy_name, data in policy_changes.items():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(f"{policy_name} - 初始", f"{data['initial']:.3f}")
            
            with col2:
                st.metric(f"{policy_name} - 最终", f"{data['final']:.3f}")
            
            with col3:
                st.metric(
                    f"{policy_name} - 变化",
                    f"{data['change']:+.3f}",
                    delta="政策调整" if abs(data['change']) > 0.05 else "基本稳定"
                )

def calculate_elite_stability(rounds_data: List[Dict]) -> List[Dict]:
    """计算核心圈稳定性"""
    stability_data = []
    
    for i in range(1, len(rounds_data)):
        prev_circle = rounds_data[i-1].get('core_decision_circle', [])
        curr_circle = rounds_data[i].get('core_decision_circle', [])
        
        if not prev_circle or not curr_circle:
            continue
        
        # 提取成员ID
        prev_ids = set(member.get('id', f"agent_{j}") for j, member in enumerate(prev_circle))
        curr_ids = set(member.get('id', f"agent_{j}") for j, member in enumerate(curr_circle))
        
        # 计算变动率
        if prev_ids:
            common_members = len(prev_ids & curr_ids)
            turnover_rate = 1 - (common_members / len(prev_ids))
        else:
            turnover_rate = 1.0
        
        stability_data.append({
            'round': i,
            'turnover_rate': turnover_rate,
            'new_members': len(curr_ids - prev_ids),
            'departed_members': len(prev_ids - curr_ids)
        })
    
    return stability_data