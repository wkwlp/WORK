import random
import pandas as pd
from pathlib import Path

# 生成 250 份问卷数据
num_responses = 250
data = []

for _ in range(num_responses):
    response = {}
    # 问题 1: 性别
    response['您的性别？'] = 1 if random.choice([0, 1]) == 0 else 2  # 1代表男，2代表女
    # 问题 2: 年龄
    age_choices = [1, 2, 3, 4]
    response['您的年龄？'] = random.choice(age_choices)  # 1-4分别代表四个年龄段
    # 问题 3: 职业
    occupation_choices = [1, 2, 3, 4, 5]
    response['您的职业？'] = random.choice(occupation_choices)  # 1-5分别代表五种职业
    # 问题 4: 月收入水平
    income_choices = [1, 2, 3, 4, 5]
    response['您的月收入水平？'] = random.choice(income_choices)  # 1-5分别代表五个收入段
    # 问题 5: 是否经常使用短视频平台
    uses_short_video_platform = random.choice([1, 2])  # 1代表是，2代表否
    response['您是否经常使用短视频平台？'] = uses_short_video_platform

    promotion_types = [1, 2, 3, 4, 5, 6]  # 定义推广类型编号
    benefits = [1, 2, 3, 4, 5, 6]  # 定义帮助编号

    if uses_short_video_platform == 1:
        response['您最常使用的短视频平台是？'] = random.choice([1, 2, 3, 4])  # 1-4分别代表抖音、快手、小红书、B站
        response['您每天平均观看短视频的时长是？'] = random.choice([1, 2, 3, 4])  # 1-4分别代表四个时间段
        has_seen_ad = random.choice([1, 2])  # 1代表是，2代表否
        response['您是否观看过谷雨护肤品在短视频平台上的推广内容？'] = has_seen_ad

        if has_seen_ad == 1:
            response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice([1, 2, 3, 4, 5])  # 1-5满意度评分
            num_choices = random.randint(1, len(promotion_types))
            selected_types = random.sample(promotion_types, num_choices)
            response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = ', '.join(
                map(str, selected_types))  # 类型编号
            num_benefits = random.randint(1, len(benefits))
            selected_benefits = random.sample(benefits, num_benefits)
            response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = ', '.join(
                map(str, selected_benefits))  # 帮助编号
            purchase_behavior = random.choice([1, 2, 3])
            response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = purchase_behavior  # 购买行为编号
            response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice(
                [1, 2, 3, 4, 5])  # 创意性评分
            interaction = random.choice([1, 2, 3])
            response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = interaction  # 互动频率编号
            cost_opinion = random.choice([1, 2, 3])
            response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = cost_opinion  # 成本观点编号
        else:
            response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice([1, 2, 3, 4, 5])
            response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = random.choice(promotion_types)
            response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = random.choice(benefits)
            purchase_behavior = random.choice([1, 2, 3])
            response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = purchase_behavior
            response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice([1, 2, 3, 4, 5])
            interaction = random.choice([1, 2, 3])
            response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = interaction
            cost_opinion = random.choice([1, 2, 3])
            response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = cost_opinion
    else:
        response['您最常使用的短视频平台是？'] = random.choice([1, 2, 3, 4])
        response['您每天平均观看短视频的时长是？'] = random.choice([1, 2, 3, 4])
        has_seen_ad = random.choice([1, 2])
        response['您是否观看过谷雨护肤品在短视频平台上的推广内容？'] = has_seen_ad
        response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice([1, 2, 3, 4, 5])
        response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = random.choice(promotion_types)
        response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = random.choice(benefits)
        purchase_behavior = random.choice([1, 2, 3])
        response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = purchase_behavior
        response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice([1, 2, 3, 4, 5])
        interaction = random.choice([1, 2, 3])
        response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = interaction
        cost_opinion = random.choice([1, 2, 3])
        response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = cost_opinion

    data.append(response)

df = pd.DataFrame(data)
desktop_path = Path.home() / 'Desktop'
file_path = desktop_path / 'guyu.xlsx'
df.to_excel(file_path, index=False)
print(f"数据已保存到 {file_path}")