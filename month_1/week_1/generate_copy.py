#！/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI营销文案生产器
功能：根据产品卖点，自动生成3条营销文案
"""

import requests
import time
from typing import List, Dict

class MarketCopyGenerator:
    """营销文案生成器类"""

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com") -> None:
        """
        初始化API客户端
        Args:
            api_key
            base_url
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate_copy(self,
        product_feature : str,
        tone: str = "professional",
        target_audience: str = "general",
        temperature: float = 0.8,
        max_tokens: int = 500) -> List[str]:
        """
        生成营销文案
        Args:
            product_feature: 产品卖点描述
            tone: 文案风格（professional, casual, enthusiastic, luxurious）
            target_audience: 目标受众
            temperature: 生成文本的创造性程度，范围0-1，值越高生成的文本越有创意
            max_tokens: 最大生成token数

        Returns:
            生成3条营销文案列表
        """

        # 构建提示语
        prompt = self._build_prompt(product_feature, tone, target_audience)

        # 调用api
        try:
            response = self._call_api(prompt, temperature, max_tokens)
            copies = self._parse_response(response)
            return copies
        except Exception as e:
            print(f"Error generating copy: {e}")
            return []

    def _build_prompt(self, product_feature: str, tone: str, target_audience: str) -> str:
        """构建提示语"""
        
        tone_map = {
            "professional": "专业",
            "casual": "随意",
            "enthusiastic": "热情",
            "luxurious": "奢华"
        }

        audience_map = {
            "general": "大众",
            "young": "年轻人",
            "business": "商务人士",
            "premium": "高端用户"
            }

        prompt = f"""你是一位资深的营销文案专家。请根据以下产品卖点，生成3条不同类型的营销文案。
            【产品卖点】
            {product_feature}

            【写作要求】
            - 语气风格：{tone_map.get(tone, "专业")}
            - 目标受众：{audience_map.get(target_audience, "大众")}
            - 每条文案长度控制在100字以内
            - 突出产品核心价值
            - 包含明确的行动号召

            【三条文案类型】
            1. 痛点切入型：强调用户的痛点，展示产品如何解决问题。
            2. 情感共鸣型：通过情感共鸣引起用户兴趣，展示产品带来的美好体验。
            3. 价值展示型：直接突出产品的核心优势和独特卖点，吸引注重实用性的用户。

            请根据以上要求生成3条营销文案，每条文案前面标注类型,用[文案1]、[文案2]、[文案3]进行区分，每条文案之间空一行。"""
        return prompt

    def _call_api(self, prompt: str, temperature: float, max_tokens: int) -> Dict:
        """调用API生成文案"""
        endpoint = f"{self.base_url}/chat/completions"

        payload = {
            "model": "deepseek-v4-flash",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.95,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }
        print("正在调用API生成文案...")
        print(f" - 创造性参数：{temperature}")
        print(f" - 最大token数：{max_tokens}")

        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 响应内容: {response.text}")

    def _parse_response(self, response: Dict) -> List[str]:
        """解析API返回的数据"""

        try:
            # 提取生成的文本
            content = response['choices'][0]['message']['content']

            # 打印token使用情况
            usage = response.get('usage', {})
            if usage:
                print("\n Token使用统计：")
                print(f"    - 输入tokens: {usage.get('prompt_tokens', 0)}")
                print(f"    - 输出tokens: {usage.get('completion_tokens', 0)}")
                print(f"    - 总计tokens: {usage.get('total_tokens', 0)}")

            copies = []
            lines = content.strip().split('\n')
            for line in lines:
                print(line)
            current_copy = []
            for line in lines:
                if line.startswith("文案") or (line.startswith("1. ") and "文案" in line):
                    if current_copy:
                        copies.append('\n'.join(current_copy).strip())
                        current_copy = []
                    else:
                        if line.strip():
                            current_copy.append(line.strip())
                if current_copy:
                    copies.append('\n'.join(current_copy).strip())

                if len(copies) < 3:
                    copies = [content]
                return copies[:3]
        except Exception as e:
            print(f"解析失败： {e}")
            return [response.get('choices')[0].get('message', {}).get('content', '生成失败')]

    def save_to_file(self, copies: List[str], filename: str = "marketing_copies.txt") -> None:
        """保存文案到文件"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("AI生成营销文案\n")
            f.write(f"生成时间：{time.strftime('%Y-%m-%d %H-%M-%S')}\n")
            f.write("=" * 60 + "\n")

            for i, copy in enumerate(copies, 1):
                f.write("【文案{i}】\n")
                f.write(copy)
                f.write("\n\n" + "-" * 40 + "\n\n")

            print(f"文案已保存到：{filename}")



def main():
    """主函数：交互式文案生成"""

    print("=" * 60)
    print("AI营销文案生成器")
    print("=" * 60)

    # 获取API密钥
    print("\n请先获取Deepseek API密钥：")
    print("注册地址：https://platform.deepseek.com/")
    api_key = input("\n请输入你的API密钥：").strip()

    if not api_key:
        print("错误：API密钥不能为空！")
        return

    generator = MarketCopyGenerator(api_key)

    # 输入产品卖点
    print("\n" + "=" * 60)
    print("请输入产品卖点信息")
    print("提示：越详细越好，例如：智能手表-24小时心率监测、10天超长续航、50米防水")
    print("-" * 60)
    product_feature = input("\n产品卖点：").strip()
    if not product_feature:
        print("错误：产品卖点不能为空")
        return

    # 输入文案风格
    print("\n" + "=" * 60)
    print("请选择文案风格：")
    print("1. 专业正式（适合B2B、企业服务）")
    print("2. 轻松亲切（适合日常消费品）")
    print("3. 热情活力（适合年轻产品、运动品牌）")
    print("4. 高端奢华（适合奢侈品、高端服务）")
    tone_choice = input("\n请选择（1-4，默认2）：").strip()
    tone_map = {"1" : "professional", "2": "casual", "3": "enthusiastic", "4": "luxurious"}
    tone = tone_map.get(tone_choice, "casual")

    # 输入文案风格
    print("\n" + "=" * 60)
    print("请选择目标受众：")
    print("1. 大众消费者")
    print("2. 年轻人群")
    print("3. 商务人士")
    print("4. 高端用户")
    audience_choice = input("\n请选择（1-4，默认1）：").strip()
    audience_map = {"1" : "general", "2": "young", "3": "business", "4": "premium"}
    taget_audience = audience_map.get(audience_choice, "general")

    # 高级参数设置
    print("\n" + "=" * 60)
    print("高级参数设置（直接回车使用默认值）")
    temp_input = input("创造性参数 0-1（默认0.8，越高越有创意）：").strip()
    temperature = float(temp_input) if temp_input else 0.8
    temperature = max(0, min(temperature, 1))

    max_input = input("最大生成长度（默认500tokens）:").strip()
    max_tokens = min(int(max_input) if max_input else 500, 1000)

    # 生成文案
    print("\n" + "=" * 60)
    print("开始生成营销文案...")
    print("-" * 60)

    copies = generator.generate_copy(
        product_feature=product_feature,
        tone=tone,
        target_audience=taget_audience,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if copies:
        print("\n" + "=" * 60)
        print("生成的营销文案：")
        print("=" * 60 + "\n")

        for i, copy in enumerate(copies, 1):
            print(f"文案{i}")
            print(copy)
            print("\n" + "-" * 40 + "\n")

        save_choice = input("\n是否保存到文件？（y/n,默认y）:").strip().lower()
        if save_choice != "n":
            generator.save_to_file(copies)

        print("文案生成完成！")
    else:
            print("\n 生成失败，请检查网络连接和API密钥")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n 程序已退出")
    except Exception as e:
        print(f"\n 发生错误 {e}")
        print("请检查网络连接或API密钥是否正确")
