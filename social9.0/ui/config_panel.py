import streamlit as st
import json
from typing import Dict, Any

def render_config_panel() -> Dict[str, Any]:
    """
    渲染参数配置面板
    
    Returns:
        配置参数字典
    """
    st.header("🔧 参数配置面板")
    st.markdown("调节社会模拟的初始设定和核心机制参数")
    
    # 创建配置字典
    config = {}
    
    # 社会规模与分布
    with st.expander("👥 社会规模与分布", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            config['total_population'] = st.slider(
                "总人数",
                min_value=50,
                max_value=500,
                value=200,
                step=10,
                help="社会总人口数量，影响模拟复杂度和统计稳定性"
            )
            
        with col2:
            config['gender_ratio'] = st.slider(
                "性别比例 (男性比例)",
                min_value=0.3,
                max_value=0.7,
                value=0.5,
                step=0.05,
                help="男性在总人口中的比例"
            )
            
        st.subheader("阶层分布")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            low_class_ratio = st.slider(
                "低阶层比例",
                min_value=0.4,
                max_value=0.8,
                value=0.6,
                step=0.05
            )
            
        with col2:
            middle_class_ratio = st.slider(
                "中阶层比例",
                min_value=0.1,
                max_value=0.4,
                value=0.3,
                step=0.05
            )
            
        with col3:
            high_class_ratio = 1.0 - low_class_ratio - middle_class_ratio
            st.metric("高阶层比例", f"{high_class_ratio:.2f}")
            
        config['class_distribution'] = {
            'low': low_class_ratio,
            'middle': middle_class_ratio,
            'high': high_class_ratio
        }
    
    # 初始社会平等程度
    with st.expander("⚖️ 初始社会平等程度", expanded=True):
        config['initial_social_equality'] = st.slider(
            "社会平等指数",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="初始社会平等程度，0=极不平等，1=完全平等"
        )
        
        st.info(f"当前设定：{'高度平等' if config['initial_social_equality'] > 0.7 else '中等平等' if config['initial_social_equality'] > 0.3 else '低度平等'}社会")
    
    # 技能初始分布
    with st.expander("🎯 技能初始分布", expanded=True):
        st.subheader("男性技能分布")
        col1, col2 = st.columns(2)
        
        with col1:
            config['male_care_skill_mean'] = st.slider(
                "男性关怀技能均值",
                min_value=0.1,
                max_value=0.9,
                value=0.4,
                step=0.05
            )
            
        with col2:
            config['male_competition_skill_mean'] = st.slider(
                "男性竞争技能均值",
                min_value=0.1,
                max_value=0.9,
                value=0.6,
                step=0.05
            )
            
        st.subheader("女性技能分布")
        col1, col2 = st.columns(2)
        
        with col1:
            config['female_care_skill_mean'] = st.slider(
                "女性关怀技能均值",
                min_value=0.1,
                max_value=0.9,
                value=0.6,
                step=0.05
            )
            
        with col2:
            config['female_competition_skill_mean'] = st.slider(
                "女性竞争技能均值",
                min_value=0.1,
                max_value=0.9,
                value=0.4,
                step=0.05
            )
            
        config['skill_std_dev'] = st.slider(
            "技能标准差",
            min_value=0.05,
            max_value=0.3,
            value=0.15,
            step=0.01,
            help="技能分布的标准差，值越大个体差异越大"
        )
    
    # 政策杠杆初始值
    with st.expander("🎛️ 政策杠杆初始值", expanded=True):
        st.markdown("这些参数将影响社会运行的核心机制")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config['competition_reward'] = st.slider(
                "竞争回报系数",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="竞争性事件的奖励倍数"
            )
            
            config['tax_redistribution'] = st.slider(
                "税收再分配率",
                min_value=0.0,
                max_value=0.5,
                value=0.2,
                step=0.05,
                help="财富再分配的税率"
            )
            
            config['social_sanction'] = st.slider(
                "社会制裁强度",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05,
                help="对意识形态偏离者的制裁强度"
            )
            
        with col2:
            config['care_reward'] = st.slider(
                "关怀回报系数",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="关怀性事件的奖励倍数"
            )
            
            config['attribution_bias'] = st.slider(
                "功劳归因偏置",
                min_value=-1.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                help="正值偏向男性，负值偏向女性"
            )
    
    # 其他机制数值
    with st.expander("⚙️ 其他机制数值", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            config['base_growth_rate'] = st.slider(
                "基础财富增长率",
                min_value=0.0,
                max_value=0.05,
                value=0.01,
                step=0.001,
                format="%.3f",
                help="每轮基础财富增长率"
            )
            
            config['learning_rate'] = st.slider(
                "学习速率",
                min_value=0.01,
                max_value=0.3,
                value=0.1,
                step=0.01,
                help="个体学习技能的速度"
            )
            
        with col2:
            config['sanction_trigger_threshold'] = st.slider(
                "制裁触发阈值",
                min_value=0.1,
                max_value=0.8,
                value=0.4,
                step=0.05,
                help="触发社会制裁的意识形态偏离阈值"
            )
            
            config['class_mobility_threshold'] = st.slider(
                "阶层流动阈值",
                min_value=0.1,
                max_value=0.5,
                value=0.3,
                step=0.05,
                help="触发阶层流动的财富差异阈值"
            )
    
    # 模拟设置
    with st.expander("🎮 模拟设置", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            config['max_rounds'] = st.number_input(
                "最大模拟轮数",
                min_value=50,
                max_value=1000,
                value=200,
                step=10,
                help="模拟运行的最大轮数"
            )
            
        with col2:
            config['random_seed'] = st.number_input(
                "随机种子 (可选)",
                min_value=0,
                max_value=99999,
                value=42,
                help="设置随机种子以确保结果可重现"
            )
    
    # 配置预设
    st.subheader("📋 配置预设")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏛️ 传统父权社会", use_container_width=True):
            st.session_state.config_preset = 'patriarchal'
            st.rerun()
            
    with col2:
        if st.button("⚖️ 平等主义社会", use_container_width=True):
            st.session_state.config_preset = 'egalitarian'
            st.rerun()
            
    with col3:
        if st.button("🔄 重置为默认", use_container_width=True):
            st.session_state.config_preset = 'default'
            st.rerun()
    
    # 应用预设
    if 'config_preset' in st.session_state:
        config = apply_preset(config, st.session_state.config_preset)
        del st.session_state.config_preset
        st.rerun()
    
    # 配置验证
    validation_errors = validate_config(config)
    if validation_errors:
        st.error("配置验证失败：")
        for error in validation_errors:
            st.error(f"• {error}")
        return None
    
    # 显示配置摘要
    with st.expander("📊 配置摘要", expanded=False):
        display_config_summary(config)
    
    # 运行模拟按钮
    st.markdown("---")
    st.subheader("🚀 运行模拟")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 开始模拟实验", use_container_width=True, type="primary"):
            # 保存配置到session state
            st.session_state.config = config
            
            # 显示进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 导入模拟类
                from core.simulation import SocialSimulation
                
                status_text.text("正在初始化模拟...")
                progress_bar.progress(10)
                
                # 创建模拟实例
                simulation = SocialSimulation(config)
                st.session_state.simulation = simulation
                
                status_text.text("正在运行模拟...")
                progress_bar.progress(30)
                
                # 运行模拟
                simulation_data = simulation.run_simulation(max_rounds=config['max_rounds'])
                
                status_text.text("正在保存结果...")
                progress_bar.progress(90)
                
                # 保存模拟数据到session state
                st.session_state.simulation_data = simulation_data
                
                progress_bar.progress(100)
                status_text.text("模拟完成！")
                
                # 显示成功消息
                st.success(f"🎉 模拟实验完成！共运行了 {len(simulation_data['rounds'])-1} 轮")
                st.info("💡 现在可以切换到其他面板查看分析结果")
                
            except Exception as e:
                st.error(f"模拟运行失败：{str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # 显示当前模拟状态
    if st.session_state.simulation_data is not None:
        st.markdown("---")
        st.subheader("📊 当前模拟状态")
        data = st.session_state.simulation_data
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("模拟轮数", len(data['rounds']) - 1)
        with col2:
            st.metric("社会人数", len(data['rounds'][0]['agents']))
        with col3:
            st.metric("最终平等指数", f"{data['rounds'][-1]['social_equality']:.3f}")
        with col4:
            final_power_gap = data['rounds'][-1]['gender_stats']['power_gap']
            st.metric("最终权力差距", f"{final_power_gap:.3f}")
    
    return config

def apply_preset(config: Dict[str, Any], preset: str) -> Dict[str, Any]:
    """应用配置预设"""
    if preset == 'patriarchal':
        # 传统父权社会设置
        config.update({
            'initial_social_equality': 0.2,
            'male_care_skill_mean': 0.3,
            'male_competition_skill_mean': 0.7,
            'female_care_skill_mean': 0.7,
            'female_competition_skill_mean': 0.3,
            'competition_reward': 1.5,
            'care_reward': 0.5,
            'attribution_bias': 0.3,
            'tax_redistribution': 0.1,
            'social_sanction': 0.5
        })
    elif preset == 'egalitarian':
        # 平等主义社会设置
        config.update({
            'initial_social_equality': 0.8,
            'male_care_skill_mean': 0.5,
            'male_competition_skill_mean': 0.5,
            'female_care_skill_mean': 0.5,
            'female_competition_skill_mean': 0.5,
            'competition_reward': 1.0,
            'care_reward': 1.0,
            'attribution_bias': 0.0,
            'tax_redistribution': 0.3,
            'social_sanction': 0.2
        })
    # 默认设置已经在slider中定义
    
    return config

def validate_config(config: Dict[str, Any]) -> list:
    """验证配置参数"""
    errors = []
    
    # 检查阶层分布总和
    class_sum = sum(config['class_distribution'].values())
    if abs(class_sum - 1.0) > 0.01:
        errors.append(f"阶层分布总和必须为1.0，当前为{class_sum:.2f}")
    
    # 检查人口数量
    if config['total_population'] < 50:
        errors.append("总人口数量不能少于50人")
    
    # 检查技能均值合理性
    if config['male_care_skill_mean'] + config['male_competition_skill_mean'] > 1.8:
        errors.append("男性技能总和过高，可能导致不平衡")
        
    if config['female_care_skill_mean'] + config['female_competition_skill_mean'] > 1.8:
        errors.append("女性技能总和过高，可能导致不平衡")
    
    return errors

def display_config_summary(config: Dict[str, Any]):
    """显示配置摘要"""
    st.json({
        "社会规模": {
            "总人数": config['total_population'],
            "性别比例": f"男性{config['gender_ratio']:.1%}, 女性{1-config['gender_ratio']:.1%}",
            "阶层分布": f"低{config['class_distribution']['low']:.1%}, 中{config['class_distribution']['middle']:.1%}, 高{config['class_distribution']['high']:.1%}"
        },
        "社会特征": {
            "初始平等程度": f"{config['initial_social_equality']:.2f}",
            "竞争vs关怀回报": f"{config['competition_reward']:.1f} vs {config['care_reward']:.1f}",
            "归因偏置": f"{config['attribution_bias']:+.1f}",
            "税收再分配率": f"{config['tax_redistribution']:.1%}"
        },
        "模拟设置": {
            "最大轮数": config['max_rounds'],
            "随机种子": config['random_seed']
        }
    })

def export_config(config: Dict[str, Any]) -> str:
    """导出配置为JSON字符串"""
    return json.dumps(config, indent=2, ensure_ascii=False)

def import_config(config_json: str) -> Dict[str, Any]:
    """从JSON字符串导入配置"""
    try:
        return json.loads(config_json)
    except json.JSONDecodeError as e:
        st.error(f"配置导入失败：JSON格式错误")
        return None