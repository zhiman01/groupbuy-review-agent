"""
团购复盘诊断 Agent 测试用例 Demo
面试前运行此脚本，验证完整流程并截图保存关键输出。

运行方式：
    python test_case.py
"""

import json
import os
import sys

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tools.groupbuy_review_tool import _call_groupbuy_review_workflow


# ============================================================
# 测试用例：辣子川香火锅店
# ============================================================

TEST_CASE = {
    "shop_info": {
        "shop_name": "辣子川香",
        "category": "火锅",
        "location": "北京望京",
        "avg_price": 120,
        "open_months": 18,
    },
    "deal_info": {
        "deal_name": "双人套餐【含4荤5素+锅底+小料】",
        "original_price": 299,
        "deal_price": 168,
        "discount_rate": 0.56,
        "start_date": "2025-12-01",
        "end_date": "2025-12-07",
        "duration_days": 7,
    },
    "metrics": {
        "impression": 12580,
        "click": 847,
        "purchase": 89,
        "verified": 67,
        "review_count": 23,
    },
    "comparisons": {
        "same_category_ctr": 0.095,
        "same_category_cvr": 0.12,
        "last_week_ctr": 0.085,
        "last_week_cvr": 0.105,
    },
}


def build_prompt(test_case: dict) -> str:
    """将测试用例构造为运营提问"""
    shop = test_case["shop_info"]
    deal = test_case["deal_info"]
    metrics = test_case["metrics"]
    comp = test_case["comparisons"]

    return (
        f"帮我复盘一下{shop['shop_name']}（{shop['category']}，{shop['location']}）"
        f"最近一周（{deal['start_date']}至{deal['end_date']}）的团购经营情况。"
        f"套餐是{deal['deal_name']}，原价{deal['original_price']}元，团购价{deal['deal_price']}元（{deal['discount_rate']*100:.0f}折）。"
        f"关键数据：曝光{metrics['impression']}、点击{metrics['click']}、下单{metrics['purchase']}、"
        f"核销{metrics['verified']}、评价{metrics['review_count']}条。"
        f"同品类平均CTR {comp['same_category_ctr']*100:.1f}%，本店上周CTR {comp['last_week_ctr']*100:.1f}%；"
        f"同品类平均转化率{comp['same_category_cvr']*100:.1f}%，本店上周转化率{comp['last_week_cvr']*100:.1f}%。"
    )


def print_section(title: str, content: str, separator: str = "="):
    """格式化打印分隔区块"""
    width = 60
    print(f"\n{separator * width}")
    print(f"  {title}")
    print(f"{separator * width}")
    print(content)


def main():
    print("\n" + "🧪" + " 团购复盘诊断 Agent — 测试用例 Demo")
    print("=" * 60)

    # 1. 构造提问
    user_input = build_prompt(TEST_CASE)
    print_section("📋 运营提问", user_input, "-")

    # 2. 调用 Workflow
    print("\n⏳ 正在调用团购复盘诊断工作流...")
    result = _call_groupbuy_review_workflow(
        user_input=user_input,
        conversation_name="辣子川香复盘Demo",
    )

    # 3. 输出结果
    print_section("📊 诊断结果", result, "=")

    # 4. 保存结果到文件（便于面试截图）
    output_path = os.path.join(os.path.dirname(__file__), "assets", "test_output.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "test_case": TEST_CASE,
                "user_input": user_input,
                "diagnosis_result": result,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\n💾 结果已保存到: {output_path}")

    # 5. 追问演示说明
    print_section("🔍 追问演示说明", "", "-")
    print("追问场景建议在 Agent 对话界面演示（而非直接调 Workflow），因为：")
    print("  - Workflow 是批量节点，需要商家 ID + 周期作为结构化入参")
    print("  - Agent 支持多轮对话，能理解上下文并动态追问")
    print()
    print("  推荐追问 1：「封面图怎么改？」→ Agent 给出具体可执行建议")
    print("  推荐追问 2：「转化率诊断的置信度如何？」→ Agent 主动声明信息缺口")
    print()
    print("  详见 docs/test_case_demo.md 中的完整追问对话示例。")

    print("\n✅ 测试完成！")


if __name__ == "__main__":
    main()
