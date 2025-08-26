import numpy as np
import random
from typing import List, Dict, Any, Tuple
from .agent import Agent
from .society import SocietyState

class SocialSimulation:
    """社会模拟核心类，实现所有模拟逻辑"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化模拟系统
        
        Args:
            config: 配置参数字典
        """
        self.config = config
        self.agents = []
        self.society = None
        self.simulation_data = {
            'rounds': [],
            'config': config.copy()
        }
        
        # 初始化社会
        self._initialize_society()
        
    def _initialize_society(self):
        """初始化社会和个体"""
        total_population = self.config['total_population']
        
        # 计算各群体数量
        male_count = int(total_population * 0.5)
        female_count = total_population - male_count
        
        # 阶层分布
        low_count = int(total_population * 0.6)
        middle_count = int(total_population * 0.3)
        high_count = total_population - low_count - middle_count
        
        # 创建个体
        self.agents = []
        
        # 分配性别和阶层
        gender_class_combinations = []
        
        # 为每个阶层分配性别
        for class_level, class_count in [('low', low_count), ('middle', middle_count), ('high', high_count)]:
            class_male = int(class_count * 0.5)
            class_female = class_count - class_male
            
            gender_class_combinations.extend([('male', class_level)] * class_male)
            gender_class_combinations.extend([('female', class_level)] * class_female)
            
        # 随机打乱
        random.shuffle(gender_class_combinations)
        
        # 创建Agent
        for gender, class_level in gender_class_combinations:
            agent = Agent(gender, class_level, self.config)
            self.agents.append(agent)
            
        # 创建社会状态
        self.society = SocietyState(self.agents, self.config)
        
        # 记录初始状态
        self.simulation_data['rounds'].append(self.society.to_dict())
        
    def run_simulation(self, max_rounds: int = 200, progress_callback=None) -> Dict[str, Any]:
        """运行完整模拟"""
        for round_num in range(1, max_rounds + 1):
            self.society.current_round = round_num
            
            # 执行单轮模拟
            self._run_single_round()
            
            # 记录当前轮状态
            self.simulation_data['rounds'].append(self.society.to_dict())
            
            # 更新进度
            if progress_callback:
                progress_callback(round_num, max_rounds)
                
            # 每10轮执行特殊操作
            if round_num % 10 == 0:
                self._run_periodic_operations()
                
        return self.simulation_data
        
    def _run_single_round(self):
        """执行单轮模拟"""
        # 1. 核心决策圈投票
        self._core_circle_voting()
        
        # 2. 触发和执行事件
        event = self._trigger_event()
        if event:
            self._execute_event(event)
            
        # 3. 应用功劳归因偏置
        self._apply_attribution_bias()
        
        # 4. 执行税收再分配
        self._execute_tax_redistribution()
        
        # 5. 更新财富和权力
        self._update_wealth_power()
        
        # 6. 执行社会制裁
        self._execute_social_sanctions()
        
        # 7. 更新统计数据
        self.society.update_statistics()
        
    def _core_circle_voting(self):
        """核心决策圈投票"""
        # 随机选择1-2个政策议题
        policy_names = list(self.society.policy_levers.keys())
        num_issues = random.randint(1, 2)
        selected_policies = random.sample(policy_names, num_issues)
        
        for policy_name in selected_policies:
            new_value = self.society.vote_on_policy(policy_name)
            old_value = self.society.policy_levers[policy_name]
            
            if abs(new_value - old_value) > 0.01:  # 有显著变化才记录
                self.society.policy_levers[policy_name] = new_value
                
                # 记录政策变化事件
                self.society.add_event({
                    'type': 'policy_change',
                    'policy': policy_name,
                    'old_value': old_value,
                    'new_value': new_value,
                    'change': new_value - old_value
                })
                
    def _trigger_event(self) -> Dict[str, Any]:
        """触发随机事件"""
        # 计算事件概率
        social_event_prob = 0.4 + 0.2 * self.society.social_equality
        
        if random.random() < social_event_prob:
            return {'type': 'social', 'name': '社会合作事件'}
        else:
            return {'type': 'economic', 'name': '经济竞争事件'}
            
    def _execute_event(self, event: Dict[str, Any]):
        """执行事件"""
        if event['type'] == 'social':
            self._execute_social_event(event)
        else:
            self._execute_economic_event(event)
            
        # 记录事件
        self.society.add_event(event)
        
    def _execute_social_event(self, event: Dict[str, Any]):
        """执行社会事件"""
        # 计算全社会关怀技能总和
        total_care_skill = sum(agent.care_skill for agent in self.agents)
        
        # 动态成功标准（基于社会规模和平等程度）
        success_threshold = len(self.agents) * 0.5 * (1 + self.society.social_equality)
        
        if total_care_skill >= success_threshold:
            # 事件成功
            event['success'] = True
            event['total_care_skill'] = total_care_skill
            event['threshold'] = success_threshold
            
            # 给予关怀技能高的个体奖励
            care_reward = self.society.policy_levers['care_reward']
            
            for agent in self.agents:
                if agent.care_skill > 0.6:  # 关怀技能较高
                    power_bonus = 0.05 * care_reward * agent.care_skill
                    wealth_bonus = 0.03 * care_reward * agent.care_skill
                    
                    agent.power += power_bonus
                    agent.wealth += wealth_bonus
        else:
            # 事件失败
            event['success'] = False
            event['total_care_skill'] = total_care_skill
            event['threshold'] = success_threshold
            
    def _execute_economic_event(self, event: Dict[str, Any]):
        """执行经济事件"""
        # 基于个体竞争技能的个人表现
        competition_reward = self.society.policy_levers['competition_reward']
        
        winners = []
        for agent in self.agents:
            # 个人成功概率基于竞争技能
            success_prob = agent.competition_skill * 0.8
            
            if random.random() < success_prob:
                # 个人成功
                power_bonus = 0.04 * competition_reward * agent.competition_skill
                wealth_bonus = 0.06 * competition_reward * agent.competition_skill
                
                agent.power += power_bonus
                agent.wealth += wealth_bonus
                winners.append(agent.id)
                
        event['success'] = True
        event['winners_count'] = len(winners)
        event['total_participants'] = len(self.agents)
        
    def _apply_attribution_bias(self):
        """应用功劳归因偏置"""
        attribution_bias = self.society.policy_levers['attribution_bias']
        
        # 偏置系数
        M = 0.2  # 男性偏置系数
        F = 0.3  # 女性偏置系数
        P = 0.1  # 权力偏置系数
        
        for agent in self.agents:
            # 计算相对权力优势
            relative_power_advantage = (
                (agent.power - self.society.average_power) / 
                max(0.001, self.society.average_power)
            )
            
            # 应用偏置
            if agent.gender == 'male':
                bias_factor = (1 + M * attribution_bias) * (1 + P * relative_power_advantage)
            else:
                bias_factor = (1 - F * attribution_bias) * (1 + P * relative_power_advantage)
                
            # 调整权力（但不能为负）
            agent.power = max(0, agent.power * bias_factor)
            
    def _execute_tax_redistribution(self):
        """执行税收再分配"""
        tax_rate = self.society.policy_levers['tax_redistribution']
        
        if tax_rate <= 0:
            return
            
        total_tax = 0
        
        # 收税
        for agent in self.agents:
            if agent.wealth > self.society.average_wealth * 0.5:
                tax_multiplier = max(0, (agent.wealth / self.society.average_wealth - 0.5))
                tax_amount = agent.wealth * tax_rate * tax_multiplier
                
                agent.wealth -= tax_amount
                total_tax += tax_amount
                
        # 分配
        if total_tax > 0:
            redistribution_per_person = total_tax / len(self.agents)
            for agent in self.agents:
                agent.wealth += redistribution_per_person
                
    def _update_wealth_power(self):
        """更新财富和权力"""
        base_growth_rate = self.config.get('base_growth_rate', 0.01)
        
        for agent in self.agents:
            # 财富增长
            skill_bonus = 0.02 * (agent.competition_skill + agent.care_skill) / 2
            growth_rate = base_growth_rate + skill_bonus
            
            new_wealth = agent.wealth * (1 + growth_rate)
            
            # 应用制裁效果
            sanction_effects = agent.get_total_sanction_effects()
            new_wealth -= sanction_effects['wealth_loss']
            
            # 财富边界处理
            if new_wealth > 0.9:
                new_wealth *= 0.98  # 2%衰减
                
            agent.update_wealth(new_wealth)
            
            # 更新权力
            agent.update_power()
            
            # 应用权力制裁
            agent.power = max(0, agent.power - sanction_effects['power_loss'])
            
            # 更新制裁效果
            agent.update_sanction_effects(self.society.current_round)
            
    def _execute_social_sanctions(self):
        """执行社会制裁"""
        sanction_lever = self.society.policy_levers['social_sanction']
        threshold = self.config.get('sanction_trigger_threshold', 0.4)
        
        for agent in self.agents:
            # 检查是否触发制裁
            deviation = abs(agent.ideology_value - self.society.average_ideology)
            
            if deviation > threshold:
                # 计算制裁强度
                sanction_intensity = sanction_lever * (deviation ** 2)
                
                # 应用制裁
                agent.add_sanction_effect(sanction_intensity, self.society.current_round)
                
    def _run_periodic_operations(self):
        """每10轮执行的操作"""
        # 1. 学习与模仿
        self._execute_learning_imitation()
        
        # 2. 意识形态转换
        self._execute_ideology_conversion()
        
        # 3. 核心决策圈重组
        self.society.update_core_decision_circle()
        
        # 4. 阶层流动检查
        self._check_class_mobility()
        
    def _execute_learning_imitation(self):
        """执行学习模仿机制"""
        learning_rate = self.config.get('learning_rate', 0.1)
        
        # 识别成功者（权力前20%）
        success_threshold = int(len(self.agents) * 0.2)
        successful_agents = sorted(self.agents, key=lambda x: x.power, reverse=True)[:success_threshold]
        
        if not successful_agents:
            return
            
        for agent in self.agents:
            if agent in successful_agents:
                continue
                
            # 寻找学习对象
            learning_target = self._find_learning_target(agent, successful_agents)
            
            if learning_target:
                agent.learn_from_successful_agent(learning_target, learning_rate)
                
    def _find_learning_target(self, agent: Agent, successful_agents: List[Agent]) -> Agent:
        """为个体寻找学习对象"""
        # 优先级：同性别 > 同阶层 > 其他
        
        # 1. 同性别同阶层
        candidates = [a for a in successful_agents 
                     if a.gender == agent.gender and a.class_level == agent.class_level]
        if candidates:
            return random.choice(candidates)
            
        # 2. 同性别
        candidates = [a for a in successful_agents if a.gender == agent.gender]
        if candidates:
            return random.choice(candidates)
            
        # 3. 同阶层
        candidates = [a for a in successful_agents if a.class_level == agent.class_level]
        if candidates:
            return random.choice(candidates)
            
        # 4. 任意成功者
        return random.choice(successful_agents) if successful_agents else None
        
    def _execute_ideology_conversion(self):
        """执行意识形态转换"""
        for agent in self.agents:
            # 检查转换冷却期
            if self.society.current_round - agent.last_ideology_change < 3:
                continue
                
            # 计算个人收益（简化版）
            personal_benefit = (agent.wealth - 0.5) + (agent.power - 0.5)
            
            # 挫败转换 (P/F → U)
            if agent.ideology in ['P', 'F'] and personal_benefit < -0.2:
                if random.random() < 0.3:  # 30%概率转换
                    agent.change_ideology('U', self.society.current_round)
                    continue
                    
            # 理性选择转换 (U → P/F)
            if agent.ideology == 'U':
                # 基于性别和阶层的理想政策点
                if agent.gender == 'male' and agent.class_level in ['middle', 'high']:
                    target_ideology = 'P'
                elif agent.gender == 'female':
                    target_ideology = 'F'
                else:
                    continue
                    
                # 计算期望收益（简化）
                if random.random() < 0.2:  # 20%概率转换
                    agent.change_ideology(target_ideology, self.society.current_round)
                    continue
                    
            # 认知失调转换 (P ↔ F)
            if agent.ideology in ['P', 'F']:
                # 检查政策差距和个人收益下降
                if personal_benefit < -0.1 and random.random() < 0.1:  # 10%概率
                    new_ideology = 'F' if agent.ideology == 'P' else 'P'
                    agent.change_ideology(new_ideology, self.society.current_round)
                    
    def _check_class_mobility(self):
        """检查阶层流动"""
        # 计算各阶层平均财富
        class_averages = {
            'low': self.society.class_stats['low']['avg_wealth'],
            'middle': self.society.class_stats['middle']['avg_wealth'],
            'high': self.society.class_stats['high']['avg_wealth']
        }
        
        mobility_changes = []
        
        for agent in self.agents:
            new_class = agent.check_class_mobility(class_averages)
            
            if new_class != agent.class_level:
                old_class = agent.class_level
                agent.class_level = new_class
                
                mobility_changes.append({
                    'agent_id': agent.id,
                    'from_class': old_class,
                    'to_class': new_class,
                    'wealth': agent.wealth
                })
                
        if mobility_changes:
            self.society.add_event({
                'type': 'class_mobility',
                'changes': mobility_changes,
                'total_changes': len(mobility_changes)
            })
            
    def get_simulation_summary(self) -> Dict[str, Any]:
        """获取模拟总结"""
        if not self.simulation_data['rounds']:
            return {}
            
        initial_state = self.simulation_data['rounds'][0]
        final_state = self.simulation_data['rounds'][-1]
        
        return {
            'total_rounds': len(self.simulation_data['rounds']) - 1,
            'initial_equality': initial_state['social_equality'],
            'final_equality': final_state['social_equality'],
            'equality_change': final_state['social_equality'] - initial_state['social_equality'],
            'initial_gender_power_gap': initial_state['gender_stats']['power_gap'],
            'final_gender_power_gap': final_state['gender_stats']['power_gap'],
            'initial_gender_wealth_gap': initial_state['gender_stats']['wealth_gap'],
            'final_gender_wealth_gap': final_state['gender_stats']['wealth_gap'],
            'total_events': len(final_state['event_history']),
            'final_ideology_distribution': final_state['ideology_stats']
        }