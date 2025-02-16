import random
import pandas as pd # pip install pandas openpyxl
from pathlib import Path

# 生成 250 份问卷数据
num_responses = 250
data = []

for _ in range(num_responses):
    response = {}
    # 问题 1: 性别
    response['您的性别？'] = random.choice(['A. 男', 'B. 女'])
    # 问题 2: 年龄
    response['您的年龄？'] = random.choice(['A. 18岁以下', 'B. 18 - 25岁', 'C. 26 - 35岁', 'D. 35岁以上'])
    # 问题 3: 职业
    response['您的职业？'] = random.choice(
        ['A. 学生', 'B. 企业工作人员', 'C. 政府机关、事业单位工作人员', 'D. 个体户', 'E. 自由职业'])
    other_occupation = ['其他职业具体说明'] if random.random() < 0.1 else []
    if other_occupation:
        response['您的职业？'] = f"{response['您的职业？']} ({other_occupation[0]})"
    # 问题 4: 月收入水平
    response['您的月收入水平？'] = random.choice(
        ['A. 3000元以下', 'B. 3001 - 5000元', 'C. 5001 - 10000元', 'D. 10001 - 20000元', 'E. 20000元以上'])
    # 问题 5: 是否经常使用短视频平台
    response['您是否经常使用短视频平台？'] = random.choice(['A. 是', 'B. 否'])

    # 确保即使选择否，后面的问题也得到合理的答案
    if response['您是否经常使用短视频平台？'] == 'A. 是':
        response['您最常使用的短视频平台是？'] = random.choice(['A. 抖音', 'B. 快手', 'C. 小红书', 'D. B站'])
        other_platform = ['其他平台具体说明'] if random.random() < 0.1 else []
        if other_platform:
            response['您最常使用的短视频平台是？'] = f"{response['您最常使用的短视频平台是？']} ({other_platform[0]})"
        response['您每天平均观看短视频的时长是？'] = random.choice(
            ['A. 少于30分钟', 'B. 30分钟 - 1小时', 'C. 1 - 2小时', 'D. 2小时以上'])
        response['您是否观看过谷雨护肤品在短视频平台上的推广内容？'] = random.choice(['A. 是', 'B. 否'])

        if response['您是否观看过谷雨护肤品在短视频平台上的推广内容？'] == 'A. 是':
            response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice(
                ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
            promotion_types = ['A. 剧情植入类', 'B. 好物推荐类', 'C. 明星代言类', 'D. 美妆教学类', 'E. 直播片段类',
                               'F. 素人改造类']
            num_choices = random.randint(1, len(promotion_types))
            selected_types = random.sample(promotion_types, num_choices)
            response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = ', '.join(selected_types)
            other_promotion_type = ['其他推广类型具体说明'] if random.random() < 0.1 else []
            if other_promotion_type:
                response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] += f", {other_promotion_type[0]}"
            benefits = ['A. 了解产品背后的故事', 'B. 了解美妆新品', 'C. 掌握化妆技能', 'D. 了解自身肤质',
                        'E. 帮助选购所需的美妆产品', 'F. 节约选购时间']
            num_benefits = random.randint(1, len(benefits))
            selected_benefits = random.sample(benefits, num_benefits)
            response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = ', '.join(selected_benefits)
            other_benefit = ['其他帮助具体说明'] if random.random() < 0.1 else []
            if other_benefit:
                response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] += f", {other_benefit[0]}"
            response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = random.choice(
                ['A. 经常购买', 'B. 偶尔购买', 'C. 没有购买过'])
            response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice(
                ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
            response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = random.choice(
                ['A. 经常', 'B. 偶尔', 'C. 从不'])
            response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = random.choice(
                ['A. 是', 'B. 否', 'C. 不确定'])
        else:
            response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice(
                ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
            response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = random.choice(promotion_types)
            response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = random.choice(benefits)
            response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = random.choice(
                ['A. 经常购买', 'B. 偶尔购买', 'C. 没有购买过'])
            response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice(
                ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
            response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = random.choice(
                ['A. 经常', 'B. 偶尔', 'C. 从不'])
            response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = random.choice(
                ['A. 是', 'B. 否', 'C. 不确定'])
    else:
        # 如果选择否，则随机生成关于其他问题的回答
        response['您最常使用的短视频平台是？'] = random.choice(['A. 抖音', 'B. 快手', 'C. 小红书', 'D. B站'])
        response['您每天平均观看短视频的时长是？'] = random.choice(
            ['A. 少于30分钟', 'B. 30分钟 - 1小时', 'C. 1 - 2小时', 'D. 2小时以上'])
        response['您是否观看过谷雨护肤品在短视频平台上的推广内容？'] = random.choice(['A. 是', 'B. 否'])
        response['您对谷雨护肤品在短视频平台上的推广内容印象如何？'] = random.choice(
            ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
        promotion_types = ['A. 剧情植入类', 'B. 好物推荐类', 'C. 明星代言类', 'D. 美妆教学类', 'E. 直播片段类',
                           'F. 素人改造类']
        response['您认为谷雨护肤品在短视频平台上哪种类型的推广内容更吸引您？'] = random.choice(promotion_types)
        benefits = ['A. 了解产品背后的故事', 'B. 了解美妆新品', 'C. 掌握化妆技能', 'D. 了解自身肤质',
                    'E. 帮助选购所需的美妆产品', 'F. 节约选购时间']
        response['您认为观看谷雨护肤品在短视频平台上的推广内容对您有何帮助？'] = random.choice(benefits)
        response['您是否因为观看谷雨护肤品在短视频平台上的推广内容而购买过其产品？'] = random.choice(
            ['A. 经常购买', 'B. 偶尔购买', 'C. 没有购买过'])
        response['您对谷雨护肤品在短视频平台上推广内容的创意性和专业性有何评价？'] = random.choice(
            ['A. 非常满意', 'B. 比较满意', 'C. 一般', 'D. 不太满意', 'E. 非常不满意'])
        response['您是否经常点赞、评论或转发谷雨护肤品在短视频平台上的推广内容？'] = random.choice(
            ['A. 经常', 'B. 偶尔', 'C. 从不'])
        response['您是否认为谷雨护肤品在短视频平台上与KOL合作的成本过高，导致产品价格上升？'] = random.choice(
            ['A. 是', 'B. 否', 'C. 不确定'])



    # 将响应数据添加到列表中
    data.append(response)

# 创建 DataFrame
df = pd.DataFrame(data)

# 保存为 Excel 文件到桌面
desktop_path = Path.home() / 'Desktop'
file_path = desktop_path / 'guyu.xlsx'
df.to_excel(file_path, index=False)

print(f"数据已保存到 {file_path}")