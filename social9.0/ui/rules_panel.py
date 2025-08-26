import streamlit as st
import pandas as pd

def render_rules_panel():
    """渲染规则介绍面板"""
    
    st.header("📖 多维社会模拟实验 - 规则介绍")
    st.markdown("---")
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏗️ 实体定义", 
        "⚙️ 核心机制", 
        "🗳️ 决策机制", 
        "📚 学习机制", 
        "🔄 模拟流程", 
        "📊 参数表"
    ])
    
    with tab1:
        render_entity_definitions()
    
    with tab2:
        render_core_mechanisms()
    
    with tab3:
        render_decision_mechanisms()
    
    with tab4:
        render_learning_mechanisms()
    
    with tab5:
        render_simulation_flow()
    
    with tab6:
        render_parameter_table()

def render_entity_definitions():
    """渲染实体定义部分"""
    
    st.subheader("🧑‍🤝‍🧑 主体 (Agent) 属性")
    
    # 基本属性表格
    basic_attrs = {
        "属性名": ["id", "gender", "class", "wealth", "power", "care_skill", "competition_skill", "ideology", "ideology_value"],
        "类型": ["String", "Enum", "Enum", "Float", "Float", "Float", "Float", "Enum", "Float"],
        "范围/值": ["唯一标识符", "'male', 'female'", "'low', 'middle', 'high'", "[0.01, 1.0]", "[0, 1.0]", "[0, 1.0]", "[0, 1.0]", "'P', 'F', 'U'", "P=1, F=-1, U=0"],
        "说明": ["个体唯一ID", "性别", "社会阶层(可变)", "财富水平", "权力水平", "关怀技能", "竞争技能", "意识形态", "数值化意识形态"]
    }
    
    df_attrs = pd.DataFrame(basic_attrs)
    st.dataframe(df_attrs, use_container_width=True)
    
    st.subheader("📊 初始值设定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**社会规模与分布**")
        st.info("""
        • 总人数：1000人
        • 性别比例：1:1 (500男性，500女性)
        • 阶层分布：低阶层60%(600人)，中阶层30%(300人)，高阶层10%(100人)
        """)
        
        st.markdown("**财富初始分布**")
        st.info("""
        • 低阶层：均值0.2，标准差0.1，范围[0.05, 0.35]
        • 中阶层：均值0.5，标准差0.15，范围[0.2, 0.8]
        • 高阶层：均值0.8，标准差0.1，范围[0.6, 1.0]
        """)
    
    with col2:
        st.markdown("**技能初始分布**")
        st.info("""
        • 女性关怀技能：均值0.65，标准差0.15
        • 男性关怀技能：均值0.45，标准差0.15
        • 男性竞争技能：均值0.65，标准差0.15
        • 女性竞争技能：均值0.45，标准差0.15
        """)
        
        st.markdown("**权力计算公式**")
        st.code("power = 0.5 × wealth + 0.25 × competition_skill + 0.25 × care_skill")
    
    st.subheader("🏛️ 社会状态 (SocietyState)")
    
    society_attrs = {
        "属性名": ["current_round", "social_equality", "average_wealth", "average_power", "average_ideology", "policy_levers", "core_decision_circle"],
        "类型": ["Int", "Float", "Float", "Float", "Float", "Dict", "List[Agent]"],
        "说明": ["当前轮数", "社会平等程度[0,1]", "社会平均财富", "社会平均权力", "社会平均意识形态", "五个政策杠杆", "核心决策圈成员"]
    }
    
    df_society = pd.DataFrame(society_attrs)
    st.dataframe(df_society, use_container_width=True)

def render_core_mechanisms():
    """渲染核心机制部分"""
    
    st.subheader("📈 社会平等程度计算")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**基尼系数计算**")
        st.code("Gini = (Σ|Wi - Wj|) / (2n²W̄)")
        st.caption("Wi为个体i的财富，W̄为平均财富，n为总人数")
    
    with col2:
        st.markdown("**社会平等程度**")
        st.code("social_equality = 1 - Gini")
        st.caption("边界处理：限制在[0, 1]范围内")
    
    st.subheader("🎲 事件系统")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**事件概率计算**")
        st.code("""
social_event_probability = 0.4 + 0.2 × social_equality
economic_event_probability = 1 - social_event_probability
        """)
    
    with col2:
        st.markdown("**事件成功标准**")
        st.info("""
        • **社会事件**：全社会关怀技能总和 ≥ 动态标准
        • **经济事件**：基于个体竞争技能的个人表现
        """)
    
    st.subheader("⚖️ 功劳归因偏置算法")
    
    st.markdown("**双因子偏置公式**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**男性实际获得权力**")
        st.code("""
actual_power_male = theoretical_power × 
    (1 + M × attribution_bias) × 
    (1 + P × relative_power_advantage)
        """)
    
    with col2:
        st.markdown("**女性实际获得权力**")
        st.code("""
actual_power_female = theoretical_power × 
    (1 - F × attribution_bias) × 
    (1 + P × relative_power_advantage)
        """)
    
    st.markdown("**系数定义**")
    coeffs = {
        "系数": ["M (男性性别偏置)", "F (女性性别偏置)", "P (权力偏置)"],
        "值": ["0.2", "0.3", "0.1"],
        "说明": ["男性获得额外权力的比例", "女性失去权力的比例", "基于相对权力优势的额外偏置"]
    }
    df_coeffs = pd.DataFrame(coeffs)
    st.dataframe(df_coeffs, use_container_width=True)
    
    st.subheader("💰 税收再分配算法")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**个人税额计算**")
        st.code("""
tax_amount = personal_wealth × tax_lever × 
    max(0, (personal_wealth/average_wealth - 0.5))
        """)
    
    with col2:
        st.markdown("**税收分配**")
        st.code("""
redistribution_per_person = 
    total_tax_collected / total_population
        """)
    
    st.subheader("🚫 社会制裁机制")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**制裁触发条件**")
        st.code("""
|individual_ideology_value - 
 society_average_ideology| > 0.4
        """)
    
    with col2:
        st.markdown("**制裁强度计算**")
        st.code("""
sanction_intensity = 
    social_sanction_lever × (deviation)²
        """)
    
    with col3:
        st.markdown("**制裁效果实施**")
        st.code("""
power_loss = sanction_intensity × 0.08
wealth_loss = sanction_intensity × 0.03
        """)
    
    st.info("💡 **制裁持续与衰减**：制裁效果持续3轮，每轮强度衰减50%")

def render_decision_mechanisms():
    """渲染决策机制部分"""
    
    st.subheader("👥 核心决策圈")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**组成规则**")
        st.info("""
        • 成员数量：权力值最高的前5% (50人)
        • 重组频率：每10轮根据最新权力排名重组
        """)
        
        st.markdown("**投票机制**")
        st.info("""
        • 议题选择：每轮随机选择1-2个政策杠杆
        • 投票规则：简单多数决
        • 平票处理：维持现状
        • 调整幅度：每轮最大±20%
        """)
    
    with col2:
        st.markdown("**边界处理机制**")
        st.code("""
new_value = boundary_value + 
    (excess_amount) × 0.1
        """)
        st.caption("当调整后的值超出边界时的软化处理")
    
    st.subheader("🎛️ 政策杠杆定义")
    
    policy_levers = {
        "政策杠杆": ["competition_reward", "care_reward", "tax_redistribution", "attribution_bias", "social_sanction"],
        "功能": ["经济事件获胜奖励乘数", "社会事件成功权力奖励乘数", "财富重新分配税率", "按原有权力分配奖励的比例", "违反意识形态规范的惩罚强度"],
        "边界范围": ["[0.5, 2.0]", "[0.5, 2.0]", "[0, 0.8]", "[0, 1]", "[0, 1]"],
        "初始值": ["1.5", "1.0", "0.3", "0.6", "0.4"]
    }
    
    df_policy = pd.DataFrame(policy_levers)
    st.dataframe(df_policy, use_container_width=True)
    
    st.subheader("🔄 意识形态转换机制")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**P/F → U 转换 (挫败转换)**")
        st.info("""
        • 触发条件：个人收益低于挫败阈值(0.2)
        • 滞后带：0.05
        • 转换概率：基于挫败程度
        """)
    
    with col2:
        st.markdown("**U → P/F 转换 (理性选择)**")
        st.info("""
        • 基于期望收益函数
        • 个人理想点基于性别和阶层组合确定
        """)
        st.code("f(政策值) = 1/(1+exp(-5×(政策值-个人理想点)))")
    
    with col3:
        st.markdown("**P ↔ F 转换 (认知失调)**")
        st.info("""
        • 触发条件：政策差距>0.3且个人收益连续下降2轮
        """)
    
    st.markdown("**社会氛围影响**")
    st.code("""
final_conversion_probability = base_probability × 
    (same_class_target_ratio × 0.7 + society_target_ratio × 0.3)
    """)
    
    st.warning("⏰ **转换限制**：转换后3轮冷却期，固定转换成本：0.02")

def render_learning_mechanisms():
    """渲染学习机制部分"""
    
    st.subheader("🎯 成功者识别")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**成功者标准**")
        st.info("权力值前20%的个体")
        
        st.markdown("**学习对象选择优先级**")
        st.info("""
        1. 性别匹配：同性别 > 异性别
        2. 阶层匹配：同阶层 > 相邻阶层 > 跨越阶层
        """)
    
    with col2:
        st.markdown("**学习失败处理**")
        st.info("""
        当无符合条件的成功者时：
        1. 扩大成功者范围至前30%
        2. 移除阶层限制
        3. 移除性别限制
        """)
    
    st.subheader("📚 技能学习")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**学习公式**")
        st.code("new_skill = old_skill + 0.1 × (target_skill - old_skill)")
    
    with col2:
        st.markdown("**学习频率**")
        st.info("每10轮进行一次学习")
    
    st.subheader("📊 阶层流动机制")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**流动检查频率**")
        st.info("每10轮检查一次")
    
    with col2:
        st.markdown("**上升条件**")
        st.info("财富超过目标阶层平均值1.5倍，持续3轮")
    
    with col3:
        st.markdown("**下降条件**")
        st.info("财富低于当前阶层平均值0.6倍，持续3轮")

def render_simulation_flow():
    """渲染模拟流程部分"""
    
    st.subheader("🔄 主循环流程")
    
    st.markdown("**每轮执行步骤**")
    
    steps = [
        "🗳️ 核心决策圈投票 - 随机选择议题，成员投票，政策杠杆调整",
        "🎲 事件触发与执行 - 计算事件概率，随机触发事件，执行事件逻辑，分配奖励",
        "💰 收益分配 - 应用功劳归因偏置，执行税收再分配",
        "📊 财富权力更新 - 更新个体财富，重新计算权力，边界处理",
        "🚫 社会制裁执行 - 检查制裁触发条件，计算制裁强度，应用制裁效果",
        "📈 状态更新 - 更新社会平等程度，更新平均值统计，记录历史数据"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"**{i}.** {step}")
    
    st.markdown("**每10轮执行步骤**")
    
    periodic_steps = [
        "📚 学习与模仿 - 识别成功者，技能学习，意识形态转换",
        "👥 核心决策圈重组 - 重新排序权力值，更新决策圈成员",
        "📊 阶层流动检查 - 检查流动条件，执行阶层调整"
    ]
    
    for i, step in enumerate(periodic_steps, 1):
        st.markdown(f"**{i}.** {step}")
    
    st.subheader("🛑 终止条件")
    
    termination_conditions = [
        "达到预设轮数上限",
        "系统达到稳定状态",
        "用户手动终止"
    ]
    
    for condition in termination_conditions:
        st.markdown(f"• {condition}")

def render_parameter_table():
    """渲染参数表部分"""
    
    st.subheader("📊 已确认参数表")
    
    # 创建参数表格
    parameters = {
        "参数名": [
            "total_population", "gender_ratio", "class_distribution", "initial_social_equality",
            "male_care_skill_mean", "female_care_skill_mean", "male_competition_skill_mean", "female_competition_skill_mean",
            "skill_std_dev", "base_growth_rate", "skill_growth_bonus", "wealth_lower_bound",
            "wealth_decay_threshold", "wealth_decay_rate", "power_wealth_weight", "power_skill_weight",
            "male_bias_coefficient", "female_bias_coefficient", "power_bias_coefficient", "core_circle_percentage",
            "policy_adjustment_limit", "success_threshold_percentage", "learning_rate", "learning_frequency",
            "sanction_trigger_threshold", "sanction_power_coefficient", "sanction_wealth_coefficient", "sanction_duration",
            "ideology_conversion_cooldown", "ideology_conversion_cost", "frustration_threshold", "cognitive_dissonance_threshold"
        ],
        "值/范围": [
            "1000", "1:1", "60%:30%:10%", "0.3",
            "0.45", "0.65", "0.65", "0.45",
            "0.15", "0.01", "0.02", "0.01",
            "0.9", "0.02", "0.5", "0.25",
            "0.2", "0.3", "0.1", "0.05",
            "0.2", "0.2", "0.1", "10",
            "0.4", "0.08", "0.03", "3",
            "3", "0.02", "0.2", "0.3"
        ],
        "说明": [
            "社会总人数", "男女比例", "低:中:高阶层分布", "社会平等指数初始值",
            "男性关怀技能均值", "女性关怀技能均值", "男性竞争技能均值", "女性竞争技能均值",
            "技能分布标准差", "基础财富增长率", "技能增长奖励系数", "财富下限",
            "财富衰减阈值", "财富衰减率", "权力计算中财富权重", "权力计算中技能权重",
            "男性性别偏置系数", "女性性别偏置系数", "权力偏置系数", "核心决策圈比例",
            "政策调整幅度限制", "成功者识别阈值", "技能学习速率", "学习频率(轮)",
            "制裁触发阈值", "制裁权力损失系数", "制裁财富损失系数", "制裁持续轮数",
            "意识形态转换冷却期", "意识形态转换成本", "挫败阈值", "认知失调阈值"
        ]
    }
    
    df_params = pd.DataFrame(parameters)
    st.dataframe(df_params, use_container_width=True)
    
    st.subheader("🔧 可调节参数建议")
    
    st.markdown("**社会规模与分布**")
    adjustable_params1 = {
        "参数名": ["总人数", "性别比例", "阶层分布", "初始社会平等指数"],
        "默认值": ["1000", "1:1", "60%:30%:10%", "0.3"],
        "建议范围": ["[100, 5000]", "[0.1:0.9 ~ 0.9:0.1]", "任意比例总和100%", "[0,1]"],
        "调节建议": ["增大以模拟更大社会，减小以加速计算", "调整以测试不同性别失衡的影响", "增加高阶层比例以模拟更不平等社会", "设置为0.5以模拟中等平等社会"]
    }
    df_adj1 = pd.DataFrame(adjustable_params1)
    st.dataframe(df_adj1, use_container_width=True)
    
    st.markdown("**政策杠杆初始值**")
    adjustable_params2 = {
        "参数名": ["竞争回报", "关怀回报", "税收再分配率", "功劳归因偏置", "社会制裁强度"],
        "默认值": ["1.5", "1.0", "0.3", "0.6", "0.4"],
        "建议范围": ["[0.5,2.0]", "[0.5,2.0]", "[0,0.8]", "[0,1]", "[0,1]"],
        "调节建议": ["降低到1.0以减少竞争优势", "提高到1.5以强调关怀价值", "提高到0.5以促进平等", "降低到0.3以减少偏置", "调整到0.6以加强社会压力"]
    }
    df_adj2 = pd.DataFrame(adjustable_params2)
    st.dataframe(df_adj2, use_container_width=True)
    
    st.info("💡 **提示**：这些参数可以在'参数配置'页面中进行调整，以探索不同的社会模拟场景。")