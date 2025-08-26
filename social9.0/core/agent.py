import numpy as np
from typing import List, Dict, Any
import uuid

class Agent:
    """社会个体类，包含所有个体属性和行为"""
    
    def __init__(self, gender: str, class_level: str, config: Dict[str, Any]):
        """
        初始化个体
        
        Args:
            gender: 性别 ('male' or 'female')
            class_level: 阶层 ('low', 'middle', 'high')
            config: 配置参数字典
        """
        self.id = str(uuid.uuid4())
        self.gender = gender
        self.class_level = class_level
        
        # 初始化技能
        self._initialize_skills(config)
        
        # 初始化财富
        self._initialize_wealth(config)
        
        # 初始化权力（基于财富和技能）
        self.power = self._calculate_power()
        
        # 初始化意识形态
        self._initialize_ideology()
        
        # 制裁相关
        self.sanction_effects = []  # 当前受到的制裁效果
        self.last_ideology_change = 0  # 上次意识形态转换的轮数
        
        # 历史记录
        self.wealth_history = [self.wealth]
        self.power_history = [self.power]
        self.ideology_history = [self.ideology]
        
    def _initialize_skills(self, config: Dict[str, Any]):
        """初始化技能值"""
        if self.gender == 'male':
            care_mean = config['male_care_skill_mean']
            comp_mean = config['male_competition_skill_mean']
        else:
            care_mean = config['female_care_skill_mean']
            comp_mean = config['female_competition_skill_mean']
            
        std_dev = config['skill_std_dev']
        
        # 生成正态分布的技能值并截断
        self.care_skill = np.clip(
            np.random.normal(care_mean, std_dev),
            0.1 if self.gender == 'male' else 0.2,
            0.9 if self.gender == 'male' else 1.0
        )
        
        self.competition_skill = np.clip(
            np.random.normal(comp_mean, std_dev),
            0.1 if self.gender == 'female' else 0.2,
            0.9 if self.gender == 'female' else 1.0
        )
        
    def _initialize_wealth(self, config: Dict[str, Any]):
        """初始化财富值"""
        if self.class_level == 'low':
            mean, std, min_val, max_val = 0.2, 0.1, 0.05, 0.35
        elif self.class_level == 'middle':
            mean, std, min_val, max_val = 0.5, 0.15, 0.2, 0.8
        else:  # high
            mean, std, min_val, max_val = 0.8, 0.1, 0.6, 1.0
            
        self.wealth = np.clip(
            np.random.normal(mean, std),
            min_val, max_val
        )
        
    def _calculate_power(self) -> float:
        """计算权力值"""
        return (
            0.5 * self.wealth + 
            0.25 * self.competition_skill + 
            0.25 * self.care_skill
        )
        
    def _initialize_ideology(self):
        """初始化意识形态"""
        ideologies = ['P', 'F', 'U']  # 父权主义、女性主义、功利主义
        self.ideology = np.random.choice(ideologies)
        
        # 数值化意识形态
        ideology_values = {'P': 1, 'F': -1, 'U': 0}
        self.ideology_value = ideology_values[self.ideology]
        
    def update_wealth(self, new_wealth: float):
        """更新财富值"""
        self.wealth = max(0.01, new_wealth)  # 确保财富不低于下限
        self.wealth_history.append(self.wealth)
        
    def update_power(self):
        """重新计算并更新权力值"""
        self.power = self._calculate_power()
        self.power_history.append(self.power)
        
    def change_ideology(self, new_ideology: str, current_round: int):
        """改变意识形态"""
        if current_round - self.last_ideology_change >= 3:  # 冷却期检查
            self.ideology = new_ideology
            ideology_values = {'P': 1, 'F': -1, 'U': 0}
            self.ideology_value = ideology_values[new_ideology]
            self.last_ideology_change = current_round
            self.ideology_history.append(new_ideology)
            return True
        return False
        
    def add_sanction_effect(self, intensity: float, current_round: int):
        """添加制裁效果"""
        effect = {
            'intensity': intensity,
            'start_round': current_round,
            'duration': 3,
            'power_loss': intensity * 0.08,
            'wealth_loss': intensity * 0.03
        }
        self.sanction_effects.append(effect)
        
    def update_sanction_effects(self, current_round: int):
        """更新制裁效果（衰减和移除过期效果）"""
        active_effects = []
        
        for effect in self.sanction_effects:
            rounds_passed = current_round - effect['start_round']
            if rounds_passed < effect['duration']:
                # 每轮衰减50%
                decay_factor = 0.5 ** rounds_passed
                effect['current_intensity'] = effect['intensity'] * decay_factor
                effect['current_power_loss'] = effect['power_loss'] * decay_factor
                effect['current_wealth_loss'] = effect['wealth_loss'] * decay_factor
                active_effects.append(effect)
                
        self.sanction_effects = active_effects
        
    def get_total_sanction_effects(self) -> Dict[str, float]:
        """获取当前总制裁效果"""
        total_power_loss = sum(effect.get('current_power_loss', 0) 
                              for effect in self.sanction_effects)
        total_wealth_loss = sum(effect.get('current_wealth_loss', 0) 
                               for effect in self.sanction_effects)
        
        return {
            'power_loss': total_power_loss,
            'wealth_loss': total_wealth_loss
        }
        
    def learn_from_successful_agent(self, successful_agent: 'Agent', learning_rate: float = 0.1):
        """从成功者学习技能"""
        # 学习关怀技能
        skill_diff = successful_agent.care_skill - self.care_skill
        self.care_skill += learning_rate * skill_diff
        self.care_skill = np.clip(self.care_skill, 0, 1.0)
        
        # 学习竞争技能
        skill_diff = successful_agent.competition_skill - self.competition_skill
        self.competition_skill += learning_rate * skill_diff
        self.competition_skill = np.clip(self.competition_skill, 0, 1.0)
        
    def check_class_mobility(self, class_averages: Dict[str, float]) -> str:
        """检查阶层流动条件"""
        current_class = self.class_level
        
        # 上升条件检查
        if current_class == 'low' and self.wealth > class_averages['middle'] * 1.5:
            return 'middle'
        elif current_class == 'middle' and self.wealth > class_averages['high'] * 1.5:
            return 'high'
            
        # 下降条件检查
        elif current_class == 'high' and self.wealth < class_averages['high'] * 0.6:
            return 'middle'
        elif current_class == 'middle' and self.wealth < class_averages['middle'] * 0.6:
            return 'low'
            
        return current_class
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，用于数据保存和分析"""
        return {
            'id': self.id,
            'gender': self.gender,
            'class_level': self.class_level,
            'wealth': self.wealth,
            'power': self.power,
            'care_skill': self.care_skill,
            'competition_skill': self.competition_skill,
            'ideology': self.ideology,
            'ideology_value': self.ideology_value,
            'sanction_effects_count': len(self.sanction_effects),
            'last_ideology_change': self.last_ideology_change
        }
        
    def __repr__(self):
        return f"Agent(id={self.id[:8]}, gender={self.gender}, class={self.class_level}, wealth={self.wealth:.3f}, power={self.power:.3f})"