import numpy as np
from typing import List, Dict, Any
from .agent import Agent

class SocietyState:
    """社会状态类，管理整个社会的状态和统计数据"""
    
    def __init__(self, agents: List[Agent], config: Dict[str, Any]):
        """
        初始化社会状态
        
        Args:
            agents: 社会中的所有个体
            config: 配置参数
        """
        self.agents = agents
        self.config = config
        self.current_round = 0
        
        # 初始化政策杠杆
        self.policy_levers = {
            'competition_reward': config.get('competition_reward', 1.5),
            'care_reward': config.get('care_reward', 1.0),
            'tax_redistribution': config.get('tax_redistribution', 0.3),
            'attribution_bias': config.get('attribution_bias', 0.6),
            'social_sanction': config.get('social_sanction', 0.4)
        }
        
        # 核心决策圈
        self.core_decision_circle = []
        self.update_core_decision_circle()
        
        # 事件历史
        self.event_history = []
        
        # 统计数据
        self.social_equality = 0.0
        self.average_wealth = 0.0
        self.average_power = 0.0
        self.average_ideology = 0.0
        
        # 性别统计
        self.gender_stats = {}
        self.ideology_stats = {}
        self.class_stats = {}
        
        # 更新初始统计
        self.update_statistics()
        
    def update_statistics(self):
        """更新所有统计数据"""
        self._update_basic_stats()
        self._update_gender_stats()
        self._update_ideology_stats()
        self._update_class_stats()
        self._calculate_social_equality()
        
    def _update_basic_stats(self):
        """更新基础统计数据"""
        if not self.agents:
            return
            
        wealths = [agent.wealth for agent in self.agents]
        powers = [agent.power for agent in self.agents]
        ideologies = [agent.ideology_value for agent in self.agents]
        
        self.average_wealth = np.mean(wealths)
        self.average_power = np.mean(powers)
        self.average_ideology = np.mean(ideologies)
        
    def _update_gender_stats(self):
        """更新性别统计数据"""
        male_agents = [a for a in self.agents if a.gender == 'male']
        female_agents = [a for a in self.agents if a.gender == 'female']
        
        self.gender_stats = {
            'male': {
                'count': len(male_agents),
                'avg_wealth': np.mean([a.wealth for a in male_agents]) if male_agents else 0,
                'avg_power': np.mean([a.power for a in male_agents]) if male_agents else 0,
                'avg_care_skill': np.mean([a.care_skill for a in male_agents]) if male_agents else 0,
                'avg_competition_skill': np.mean([a.competition_skill for a in male_agents]) if male_agents else 0,
                'wealth_std': np.std([a.wealth for a in male_agents]) if male_agents else 0,
                'power_std': np.std([a.power for a in male_agents]) if male_agents else 0
            },
            'female': {
                'count': len(female_agents),
                'avg_wealth': np.mean([a.wealth for a in female_agents]) if female_agents else 0,
                'avg_power': np.mean([a.power for a in female_agents]) if female_agents else 0,
                'avg_care_skill': np.mean([a.care_skill for a in female_agents]) if female_agents else 0,
                'avg_competition_skill': np.mean([a.competition_skill for a in female_agents]) if female_agents else 0,
                'wealth_std': np.std([a.wealth for a in female_agents]) if female_agents else 0,
                'power_std': np.std([a.power for a in female_agents]) if female_agents else 0
            }
        }
        
        # 计算性别差距
        self.gender_stats['power_gap'] = (
            self.gender_stats['male']['avg_power'] - 
            self.gender_stats['female']['avg_power']
        )
        self.gender_stats['wealth_gap'] = (
            self.gender_stats['male']['avg_wealth'] - 
            self.gender_stats['female']['avg_wealth']
        )
        
    def _update_ideology_stats(self):
        """更新意识形态统计数据"""
        ideology_counts = {'P': 0, 'F': 0, 'U': 0}
        
        for agent in self.agents:
            ideology_counts[agent.ideology] += 1
            
        total = len(self.agents)
        self.ideology_stats = {
            'P': {
                'count': ideology_counts['P'],
                'percentage': ideology_counts['P'] / total if total > 0 else 0
            },
            'F': {
                'count': ideology_counts['F'],
                'percentage': ideology_counts['F'] / total if total > 0 else 0
            },
            'U': {
                'count': ideology_counts['U'],
                'percentage': ideology_counts['U'] / total if total > 0 else 0
            }
        }
        
    def _update_class_stats(self):
        """更新阶层统计数据"""
        class_groups = {'low': [], 'middle': [], 'high': []}
        
        for agent in self.agents:
            class_groups[agent.class_level].append(agent)
            
        self.class_stats = {}
        for class_level, agents in class_groups.items():
            if agents:
                self.class_stats[class_level] = {
                    'count': len(agents),
                    'avg_wealth': np.mean([a.wealth for a in agents]),
                    'avg_power': np.mean([a.power for a in agents]),
                    'male_count': len([a for a in agents if a.gender == 'male']),
                    'female_count': len([a for a in agents if a.gender == 'female'])
                }
            else:
                self.class_stats[class_level] = {
                    'count': 0, 'avg_wealth': 0, 'avg_power': 0,
                    'male_count': 0, 'female_count': 0
                }
                
    def _calculate_social_equality(self):
        """计算社会平等程度（基于基尼系数）"""
        if not self.agents:
            self.social_equality = 0
            return
            
        wealths = [agent.wealth for agent in self.agents]
        gini = self._calculate_gini_coefficient(wealths)
        self.social_equality = max(0, min(1, 1 - gini))
        
    def _calculate_gini_coefficient(self, wealths: List[float]) -> float:
        """计算基尼系数"""
        if not wealths or len(wealths) < 2:
            return 0
            
        n = len(wealths)
        mean_wealth = np.mean(wealths)
        
        if mean_wealth == 0:
            return 0
            
        total_diff = 0
        for i in range(n):
            for j in range(n):
                total_diff += abs(wealths[i] - wealths[j])
                
        gini = total_diff / (2 * n * n * mean_wealth)
        return min(1.0, gini)  # 确保不超过1
        
    def update_core_decision_circle(self):
        """更新核心决策圈（权力最高的5%）"""
        circle_size = max(1, int(len(self.agents) * 0.05))
        sorted_agents = sorted(self.agents, key=lambda x: x.power, reverse=True)
        self.core_decision_circle = sorted_agents[:circle_size]
        
    def get_core_circle_composition(self) -> Dict[str, Any]:
        """获取核心圈构成分析"""
        if not self.core_decision_circle:
            return {'gender': {}, 'ideology': {}, 'class': {}}
            
        total = len(self.core_decision_circle)
        
        # 性别构成
        male_count = len([a for a in self.core_decision_circle if a.gender == 'male'])
        female_count = total - male_count
        
        # 意识形态构成
        ideology_counts = {'P': 0, 'F': 0, 'U': 0}
        for agent in self.core_decision_circle:
            ideology_counts[agent.ideology] += 1
            
        # 阶层构成
        class_counts = {'low': 0, 'middle': 0, 'high': 0}
        for agent in self.core_decision_circle:
            class_counts[agent.class_level] += 1
            
        return {
            'gender': {
                'male': {'count': male_count, 'percentage': male_count / total},
                'female': {'count': female_count, 'percentage': female_count / total}
            },
            'ideology': {
                ideology: {'count': count, 'percentage': count / total}
                for ideology, count in ideology_counts.items()
            },
            'class': {
                class_level: {'count': count, 'percentage': count / total}
                for class_level, count in class_counts.items()
            }
        }
        
    def vote_on_policy(self, policy_name: str) -> float:
        """核心决策圈对政策进行投票"""
        if not self.core_decision_circle:
            return self.policy_levers[policy_name]
            
        # 简化的投票机制：基于意识形态倾向
        votes_increase = 0
        votes_decrease = 0
        votes_maintain = 0
        
        for agent in self.core_decision_circle:
            # 根据意识形态和政策类型决定投票倾向
            vote = self._get_policy_preference(agent, policy_name)
            
            if vote > 0:
                votes_increase += 1
            elif vote < 0:
                votes_decrease += 1
            else:
                votes_maintain += 1
                
        # 简单多数决
        current_value = self.policy_levers[policy_name]
        
        if votes_increase > votes_decrease and votes_increase > votes_maintain:
            # 增加政策值
            adjustment = min(0.2, np.random.uniform(0.05, 0.2))
            new_value = current_value * (1 + adjustment)
        elif votes_decrease > votes_increase and votes_decrease > votes_maintain:
            # 减少政策值
            adjustment = min(0.2, np.random.uniform(0.05, 0.2))
            new_value = current_value * (1 - adjustment)
        else:
            # 维持现状
            new_value = current_value
            
        # 边界处理
        policy_bounds = {
            'competition_reward': (0.5, 2.0),
            'care_reward': (0.5, 2.0),
            'tax_redistribution': (0, 0.8),
            'attribution_bias': (0, 1),
            'social_sanction': (0, 1)
        }
        
        min_val, max_val = policy_bounds[policy_name]
        if new_value > max_val:
            new_value = max_val + (new_value - max_val) * 0.1
        elif new_value < min_val:
            new_value = min_val + (min_val - new_value) * 0.1
            
        return max(min_val, min(max_val, new_value))
        
    def _get_policy_preference(self, agent: Agent, policy_name: str) -> int:
        """获取个体对特定政策的偏好（1=支持增加，-1=支持减少，0=中性）"""
        # 简化的偏好模型
        if policy_name == 'competition_reward':
            if agent.ideology == 'P' or agent.competition_skill > 0.6:
                return 1
            elif agent.ideology == 'F' or agent.care_skill > 0.6:
                return -1
        elif policy_name == 'care_reward':
            if agent.ideology == 'F' or agent.care_skill > 0.6:
                return 1
            elif agent.ideology == 'P' or agent.competition_skill > 0.6:
                return -1
        elif policy_name == 'tax_redistribution':
            if agent.ideology == 'F' or agent.wealth < self.average_wealth:
                return 1
            elif agent.ideology == 'P' or agent.wealth > self.average_wealth * 1.5:
                return -1
        elif policy_name == 'attribution_bias':
            if agent.ideology == 'P' or (agent.gender == 'male' and agent.power > self.average_power):
                return 1
            elif agent.ideology == 'F' or (agent.gender == 'female'):
                return -1
        elif policy_name == 'social_sanction':
            if abs(agent.ideology_value - self.average_ideology) < 0.2:
                return 1
            else:
                return -1
                
        return 0
        
    def add_event(self, event: Dict[str, Any]):
        """添加事件到历史记录"""
        event['round'] = self.current_round
        self.event_history.append(event)
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'current_round': self.current_round,
            'social_equality': self.social_equality,
            'average_wealth': self.average_wealth,
            'average_power': self.average_power,
            'average_ideology': self.average_ideology,
            'policy_levers': self.policy_levers.copy(),
            'gender_stats': self.gender_stats,
            'ideology_stats': self.ideology_stats,
            'class_stats': self.class_stats,
            'core_circle_composition': self.get_core_circle_composition(),
            'core_decision_circle': [agent.to_dict() for agent in self.core_decision_circle],
            'event_history': self.event_history.copy(),
            'agents': [agent.to_dict() for agent in self.agents]
        }