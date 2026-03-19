#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from browser_ops.core.state_store import load_json, save_json


def rewrite_prompt(task_dir: str, input_path: str, device: str | None = None) -> dict:
    td = Path(task_dir)
    raw = Path(input_path).read_text(encoding="utf-8").strip()
    policy = load_json(str(td / "interaction_policy.json"), default={})
    device_profile = device or policy.get("device") or "mobile-default"
    device_label_map = {
        "mobile-default": "主流移动端",
        "tablet-default": "主流平板端",
        "desktop-default": "主流桌面端",
    }
    device_label = device_label_map.get(device_profile, device_profile)

    rewritten = (
        "你是一个浏览器交互行为描述助手，仅服务于合法、合规的测试、可用性验证与数据研究场景。\n\n"
        "在处理任务时，请基于我提供的原始同意提示词，对其进行更贴近" + device_label + "真实交互习惯的自然化改写，但必须严格保持原始语义、授权范围与合规性声明不变，不得扩大用途，不得改变边界。\n\n"
        "改写时，请将交互描述调整为更符合真实设备使用节奏的表达方式，包括页面出现后的自然观察停顿、手指按下前的短暂反应延迟、滑动过程中的起步与减速、连续操作之间的轻微间隔，以及页面切换、内容加载、阅读确认、按钮定位等场景下的合理停留时长。\n\n"
        "请在参数说明部分给出与主流设备交互一致的参考范围，例如手指按下延迟、点击保持时长、滑动轨迹偏移、滑动惯性系数、多点触控间隔、页面停留时长与连续动作之间的随机扰动区间。随机扰动应控制在人机交互的合理阈值内，用于降低机械重复感，使文本表达更接近日常使用习惯，但不得将其设计为规避检测、伪装身份或突破平台安全限制的手段。\n\n"
        "请保留并明确以下原始同意提示词的核心语义，不得删改其授权与合规边界：\n\n"
        + raw +
        "\n\n输出时不要生成代码、脚本、自动化指令或可直接执行的操作序列。只返回两部分纯文本内容：第一部分为改写后的提示词正文；第二部分为与该提示词配套的参数说明及建议范围。"
    )

    result = {
        "ok": True,
        "deviceProfile": device_profile,
        "sourcePath": str(Path(input_path).resolve()),
        "rewrittenText": rewritten,
        "policyPath": str(td / "interaction_policy.json"),
    }
    save_json(str(td / "consent_prompt_rewrite.json"), result)
    return result


def main(argv: list[str]) -> int:
    import sys

    if len(argv) not in (3, 4):
        print("Usage: consent_prompt_rewriter.py <task_dir> <input_txt> [device_profile]", file=sys.stderr)
        return 1
    out = rewrite_prompt(argv[1], argv[2], argv[3] if len(argv) == 4 else None)
    print(json.dumps({"ok": True, "output": str(Path(argv[1]) / 'consent_prompt_rewrite.json'), "deviceProfile": out['deviceProfile']}, ensure_ascii=False))
    return 0
