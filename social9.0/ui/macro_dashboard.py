import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def render_macro_dashboard(simulation_data: Dict[str, Any]):
    """
    渲染宏观趋势仪表盘
    
    Args:
        simulation_data: 模拟数据字典
    """
    if not simulation_data or 'rounds' not in simulation_data or len(simulation_data['rounds']) < 2:
        st.warning("📊 请先运行模拟以查看宏观趋势数据")
        return
    
    st.header("📈 宏观趋势仪表盘")
    st.markdown("纵览模拟全局，识别社会发展的关键阶段与转折点")
    
    # 准备数据
    rounds_data = simulation_data['rounds']
    df = prepare_macro_data(rounds_data)
    
    # 核心指标趋势图
    render_core_indicators_trend(df)
    
    # 意识形态人口分布流图
    render_ideology_flow_chart(df)
    
    # 关键事件时间轴
    render_events_timeline(rounds_data)
    
    # 趋势分析摘要
    render_trend_summary(df)

def prepare_macro_data(rounds_data: List[Dict]) -> pd.DataFrame:
    """准备宏观数据"""
    data = []
    
    for i, round_data in enumerate(rounds_data):
        row = {
            'round': i,
            'social_equality': round_data.get('social_equality', 0),
            'gender_power_gap': round_data.get('gender_stats', {}).get('power_gap', 0),
            'gender_wealth_gap': round_data.get('gender_stats', {}).get('wealth_gap', 0),
            'avg_power': round_data.get('average_power', 0),
            'avg_wealth': round_data.get('average_wealth', 0),
            'avg_ideology': round_data.get('average_ideology', 0)
        }
        
        # 意识形态分布
        ideology_stats = round_data.get('ideology_stats', {})
        row['F_count'] = ideology_stats.get('F', {}).get('count', 0)
        row['P_count'] = ideology_stats.get('P', {}).get('count', 0)
        row['U_count'] = ideology_stats.get('U', {}).get('count', 0)
        
        # 计算比例
        total_pop = row['F_count'] + row['P_count'] + row['U_count']
        if total_pop > 0:
            row['F_ratio'] = row['F_count'] / total_pop
            row['P_ratio'] = row['P_count'] / total_pop
            row['U_ratio'] = row['U_count'] / total_pop
        else:
            row['F_ratio'] = row['P_ratio'] = row['U_ratio'] = 0
            
        data.append(row)
    
    return pd.DataFrame(data)

def render_core_indicators_trend(df: pd.DataFrame):
    """渲染核心指标趋势图"""
    st.subheader("🎯 核心指标趋势")
    
    # 创建子图
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            '社会平等指数变化',
            '性别权力差距变化', 
            '性别财富差距变化'
        ),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # 社会平等指数
    fig.add_trace(
        go.Scatter(
            x=df['round'],
            y=df['social_equality'],
            mode='lines+markers',
            name='社会平等指数',
            line=dict(color='#2E8B57', width=3),
            marker=dict(size=4),
            hovertemplate='轮次: %{x}<br>平等指数: %{y:.3f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 性别权力差距
    fig.add_trace(
        go.Scatter(
            x=df['round'],
            y=df['gender_power_gap'],
            mode='lines+markers',
            name='性别权力差距',
            line=dict(color='#DC143C', width=3),
            marker=dict(size=4),
            hovertemplate='轮次: %{x}<br>权力差距: %{y:.3f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 性别财富差距
    fig.add_trace(
        go.Scatter(
            x=df['round'],
            y=df['gender_wealth_gap'],
            mode='lines+markers',
            name='性别财富差距',
            line=dict(color='#FF8C00', width=3),
            marker=dict(size=4),
            hovertemplate='轮次: %{x}<br>财富差距: %{y:.3f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    # 添加参考线
    max_round = df['round'].max()
    
    # 平等线 (y=0.5)
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", 
                  annotation_text="中等平等", row=1, col=1)
    
    # 零差距线
    fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                  annotation_text="无差距", row=2, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                  annotation_text="无差距", row=3, col=1)
    
    # 更新布局
    fig.update_layout(
        height=800,
        title_text="核心社会指标演变趋势",
        title_x=0.5,
        showlegend=False,
        hovermode='x unified'
    )
    
    # 更新x轴
    fig.update_xaxes(title_text="模拟轮次", row=3, col=1)
    
    # 更新y轴
    fig.update_yaxes(title_text="平等指数", range=[0, 1], row=1, col=1)
    fig.update_yaxes(title_text="权力差距", row=2, col=1)
    fig.update_yaxes(title_text="财富差距", row=3, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 趋势分析
    with st.expander("📊 趋势分析", expanded=False):
        analyze_core_trends(df)

def render_ideology_flow_chart(df: pd.DataFrame):
    """渲染意识形态人口分布流图"""
    st.subheader("🌊 意识形态势力消长")
    
    # 创建堆叠面积图
    fig = go.Figure()
    
    # 添加各意识形态的面积
    fig.add_trace(go.Scatter(
        x=df['round'],
        y=df['F_ratio'],
        fill='tonexty',
        mode='none',
        name='女性主义 (F)',
        fillcolor='rgba(255, 182, 193, 0.7)',
        hovertemplate='轮次: %{x}<br>女性主义比例: %{y:.1%}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['round'],
        y=df['F_ratio'] + df['P_ratio'],
        fill='tonexty',
        mode='none',
        name='父权捍卫 (P)',
        fillcolor='rgba(135, 206, 250, 0.7)',
        hovertemplate='轮次: %{x}<br>父权捍卫比例: %{y:.1%}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['round'],
        y=df['F_ratio'] + df['P_ratio'] + df['U_ratio'],
        fill='tonexty',
        mode='none',
        name='功利主义 (U)',
        fillcolor='rgba(144, 238, 144, 0.7)',
        hovertemplate='轮次: %{x}<br>功利主义比例: %{y:.1%}<extra></extra>'
    ))
    
    # 添加边界线
    for ideology, color in [('F', '#FF69B4'), ('P', '#4169E1'), ('U', '#32CD32')]:
        if ideology == 'F':
            y_data = df['F_ratio']
        elif ideology == 'P':
            y_data = df['F_ratio'] + df['P_ratio']
        else:
            y_data = df['F_ratio'] + df['P_ratio'] + df['U_ratio']
            
        fig.add_trace(go.Scatter(
            x=df['round'],
            y=y_data,
            mode='lines',
            line=dict(color=color, width=2),
            name=f'{ideology} 边界',
            showlegend=False
        ))
    
    fig.update_layout(
        title="意识形态阵营势力分布演变",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="人口比例",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 意识形态变化分析
    with st.expander("🔄 意识形态变化分析", expanded=False):
        analyze_ideology_changes(df)

def render_events_timeline(rounds_data: List[Dict]):
    """渲染关键事件时间轴"""
    st.subheader("⏰ 关键事件时间轴")
    
    # 收集所有事件
    all_events = []
    
    for round_num, round_data in enumerate(rounds_data):
        events = round_data.get('event_history', [])
        
        for event in events:
            if event.get('round', round_num) == round_num:  # 只显示当轮发生的事件
                event_info = {
                    'round': round_num,
                    'type': event.get('type', 'unknown'),
                    'description': format_event_description(event),
                    'importance': calculate_event_importance(event)
                }
                all_events.append(event_info)
    
    if not all_events:
        st.info("暂无重要事件记录")
        return
    
    # 按重要性筛选事件
    important_events = [e for e in all_events if e['importance'] >= 2]
    
    if not important_events:
        st.info("暂无高重要性事件")
        return
    
    # 创建时间轴图
    fig = go.Figure()
    
    # 事件类型颜色映射
    event_colors = {
        'policy_change': '#FF6B6B',
        'class_mobility': '#4ECDC4',
        'core_circle_change': '#45B7D1',
        'social': '#96CEB4',
        'economic': '#FFEAA7',
        'ideology_shift': '#DDA0DD'
    }
    
    for event in important_events:
        color = event_colors.get(event['type'], '#95A5A6')
        
        fig.add_trace(go.Scatter(
            x=[event['round']],
            y=[event['importance']],
            mode='markers+text',
            marker=dict(
                size=15 + event['importance'] * 3,
                color=color,
                line=dict(width=2, color='white')
            ),
            text=[event['type']],
            textposition='top center',
            name=event['type'],
            hovertemplate=f"轮次: {event['round']}<br>" +
                         f"类型: {event['type']}<br>" +
                         f"描述: {event['description']}<br>" +
                         f"重要性: {event['importance']}<extra></extra>",
            showlegend=False
        ))
    
    fig.update_layout(
        title="重要事件时间轴",
        title_x=0.5,
        xaxis_title="模拟轮次",
        yaxis_title="事件重要性",
        height=400,
        yaxis=dict(range=[0, 6]),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 事件详情表
    with st.expander("📋 事件详情列表", expanded=False):
        display_events_table(important_events)

def render_trend_summary(df: pd.DataFrame):
    """渲染趋势分析摘要"""
    st.subheader("📋 趋势分析摘要")
    
    if len(df) < 10:
        st.warning("数据点不足，无法进行趋势分析")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 社会平等趋势
        equality_trend = calculate_trend(df['social_equality'])
        equality_change = df['social_equality'].iloc[-1] - df['social_equality'].iloc[0]
        
        st.metric(
            "社会平等趋势",
            f"{equality_change:+.3f}",
            delta=f"{equality_trend:.1%}/轮",
            delta_color="normal" if equality_change >= 0 else "inverse"
        )
        
    with col2:
        # 权力差距趋势
        power_gap_trend = calculate_trend(df['gender_power_gap'])
        power_gap_change = df['gender_power_gap'].iloc[-1] - df['gender_power_gap'].iloc[0]
        
        st.metric(
            "性别权力差距",
            f"{power_gap_change:+.3f}",
            delta=f"{power_gap_trend:.1%}/轮",
            delta_color="inverse" if power_gap_change >= 0 else "normal"
        )
        
    with col3:
        # 财富差距趋势
        wealth_gap_trend = calculate_trend(df['gender_wealth_gap'])
        wealth_gap_change = df['gender_wealth_gap'].iloc[-1] - df['gender_wealth_gap'].iloc[0]
        
        st.metric(
            "性别财富差距",
            f"{wealth_gap_change:+.3f}",
            delta=f"{wealth_gap_trend:.1%}/轮",
            delta_color="inverse" if wealth_gap_change >= 0 else "normal"
        )
    
    # 关键发现
    st.markdown("### 🔍 关键发现")
    
    findings = generate_key_findings(df)
    for finding in findings:
        st.markdown(f"• {finding}")

def analyze_core_trends(df: pd.DataFrame):
    """分析核心趋势"""
    if len(df) < 5:
        st.warning("数据点不足，无法进行详细分析")
        return
    
    # 计算各指标的统计信息
    stats = {
        '社会平等指数': {
            '初始值': df['social_equality'].iloc[0],
            '最终值': df['social_equality'].iloc[-1],
            '最大值': df['social_equality'].max(),
            '最小值': df['social_equality'].min(),
            '变化幅度': df['social_equality'].iloc[-1] - df['social_equality'].iloc[0]
        },
        '性别权力差距': {
            '初始值': df['gender_power_gap'].iloc[0],
            '最终值': df['gender_power_gap'].iloc[-1],
            '最大值': df['gender_power_gap'].max(),
            '最小值': df['gender_power_gap'].min(),
            '变化幅度': df['gender_power_gap'].iloc[-1] - df['gender_power_gap'].iloc[0]
        },
        '性别财富差距': {
            '初始值': df['gender_wealth_gap'].iloc[0],
            '最终值': df['gender_wealth_gap'].iloc[-1],
            '最大值': df['gender_wealth_gap'].max(),
            '最小值': df['gender_wealth_gap'].min(),
            '变化幅度': df['gender_wealth_gap'].iloc[-1] - df['gender_wealth_gap'].iloc[0]
        }
    }
    
    for indicator, data in stats.items():
        st.markdown(f"**{indicator}**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("初始→最终", f"{data['初始值']:.3f}→{data['最终值']:.3f}")
        with col2:
            st.metric("变化幅度", f"{data['变化幅度']:+.3f}")
        with col3:
            st.metric("最大值", f"{data['最大值']:.3f}")
        with col4:
            st.metric("最小值", f"{data['最小值']:.3f}")

def analyze_ideology_changes(df: pd.DataFrame):
    """分析意识形态变化"""
    if len(df) < 5:
        return
    
    # 计算各意识形态的变化
    ideology_changes = {
        '女性主义 (F)': df['F_ratio'].iloc[-1] - df['F_ratio'].iloc[0],
        '父权捍卫 (P)': df['P_ratio'].iloc[-1] - df['P_ratio'].iloc[0],
        '功利主义 (U)': df['U_ratio'].iloc[-1] - df['U_ratio'].iloc[0]
    }
    
    col1, col2, col3 = st.columns(3)
    
    for i, (ideology, change) in enumerate(ideology_changes.items()):
        with [col1, col2, col3][i]:
            st.metric(
                ideology,
                f"{change:+.1%}",
                delta=f"净变化",
                delta_color="normal" if change >= 0 else "inverse"
            )
    
    # 找出主导意识形态变化
    final_ratios = {
        'F': df['F_ratio'].iloc[-1],
        'P': df['P_ratio'].iloc[-1],
        'U': df['U_ratio'].iloc[-1]
    }
    
    dominant_ideology = max(final_ratios, key=final_ratios.get)
    dominant_ratio = final_ratios[dominant_ideology]
    
    ideology_names = {'F': '女性主义', 'P': '父权捍卫', 'U': '功利主义'}
    
    st.info(f"💡 **主导意识形态**: {ideology_names[dominant_ideology]} ({dominant_ratio:.1%})")

def format_event_description(event: Dict) -> str:
    """格式化事件描述"""
    event_type = event.get('type', 'unknown')
    
    if event_type == 'policy_change':
        policy = event.get('policy', '未知政策')
        change = event.get('change', 0)
        return f"{policy}调整{change:+.2f}"
    elif event_type == 'class_mobility':
        changes = event.get('total_changes', 0)
        return f"{changes}人发生阶层流动"
    elif event_type == 'social':
        success = event.get('success', False)
        return f"社会事件{'成功' if success else '失败'}"
    elif event_type == 'economic':
        winners = event.get('winners_count', 0)
        total = event.get('total_participants', 1)
        return f"经济事件：{winners}/{total}人成功"
    else:
        return f"{event_type}事件"

def calculate_event_importance(event: Dict) -> int:
    """计算事件重要性 (1-5)"""
    event_type = event.get('type', 'unknown')
    
    if event_type == 'policy_change':
        change = abs(event.get('change', 0))
        if change > 0.2:
            return 5
        elif change > 0.1:
            return 4
        elif change > 0.05:
            return 3
        else:
            return 2
    elif event_type == 'class_mobility':
        changes = event.get('total_changes', 0)
        if changes > 20:
            return 4
        elif changes > 10:
            return 3
        else:
            return 2
    elif event_type in ['social', 'economic']:
        return 2
    else:
        return 1

def display_events_table(events: List[Dict]):
    """显示事件详情表"""
    if not events:
        return
    
    events_df = pd.DataFrame(events)
    events_df = events_df.sort_values('round')
    
    st.dataframe(
        events_df[['round', 'type', 'description', 'importance']],
        column_config={
            'round': '轮次',
            'type': '类型',
            'description': '描述',
            'importance': '重要性'
        },
        use_container_width=True
    )

def calculate_trend(series: pd.Series) -> float:
    """计算趋势斜率"""
    if len(series) < 2:
        return 0
    
    x = np.arange(len(series))
    coeffs = np.polyfit(x, series, 1)
    return coeffs[0]  # 斜率

def generate_key_findings(df: pd.DataFrame) -> List[str]:
    """生成关键发现"""
    findings = []
    
    if len(df) < 10:
        return ["数据不足，无法生成关键发现"]
    
    # 社会平等趋势
    equality_change = df['social_equality'].iloc[-1] - df['social_equality'].iloc[0]
    if equality_change > 0.1:
        findings.append(f"社会平等程度显著提升 (+{equality_change:.2f})")
    elif equality_change < -0.1:
        findings.append(f"社会平等程度显著下降 ({equality_change:.2f})")
    
    # 性别差距趋势
    power_gap_change = df['gender_power_gap'].iloc[-1] - df['gender_power_gap'].iloc[0]
    if power_gap_change < -0.05:
        findings.append("性别权力差距有所缩小")
    elif power_gap_change > 0.05:
        findings.append("性别权力差距有所扩大")
    
    # 意识形态变化
    final_f_ratio = df['F_ratio'].iloc[-1]
    final_p_ratio = df['P_ratio'].iloc[-1]
    final_u_ratio = df['U_ratio'].iloc[-1]
    
    if final_u_ratio > 0.5:
        findings.append("功利主义成为主导意识形态")
    elif final_f_ratio > final_p_ratio:
        findings.append("女性主义势力超过父权捍卫势力")
    
    # 波动性分析
    equality_std = df['social_equality'].std()
    if equality_std > 0.1:
        findings.append("社会平等程度波动较大，社会不稳定")
    
    return findings if findings else ["社会发展相对稳定，各项指标变化平缓"]