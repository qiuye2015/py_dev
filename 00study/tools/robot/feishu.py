import json

import requests

webhook_token = '2a9a08e9-cb8a-47c3-be0a-3d4104124c58'
webhook_url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_token}"  # 替换为你的 webhook URL


def send_card_message_v1(title, content):
    headers = {"Content-Type": "application/json"}

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"content": title, "tag": "plain_text"}},
            "elements": [{"tag": "div", "text": {"content": content, "tag": "lark_md"}}],
        },
    }

    response = requests.post(webhook_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Card message sent successfully.")
    else:
        print("Failed to send card message. Error:", response.text)


msg = json.dumps(
    {
        "elements": [
            {"tag": "markdown", "content": "**个人审批效率总览**"},
            {
                "tag": "column_set",
                "flex_mode": "bisect",
                "background_style": "grey",
                "horizontal_spacing": "default",
                "columns": [
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [
                            {
                                "tag": "markdown",
                                "text_align": "center",
                                "content": "已审批单量\n**29单**\n<font color='green'>领先团队59%</font>",
                            }
                        ],
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [
                            {
                                "tag": "markdown",
                                "text_align": "center",
                                "content": "平均审批耗时\n**0.9小时**\n<font color='green'>领先团队100%</font>",
                            }
                        ],
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [
                            {
                                "tag": "markdown",
                                "text_align": "center",
                                "content": "待批率\n**25%**\n<font color='red'>落后团队29%</font>",
                            }
                        ],
                    },
                ],
            },
            {"tag": "hr"},
            {"tag": "markdown", "content": "**团队审批效率总览**"},
            {
                "tag": "column_set",
                "flex_mode": "none",
                "background_style": "default",
                "horizontal_spacing": "default",
                "columns": [
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [{"tag": "markdown", "content": "**审批人**\n王大明\n张军\n李小方"}],
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [{"tag": "markdown", "content": "**审批时长**\n小于1小时\n2小时\n3小时"}],
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "weight": 1,
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": "**对比上周变化**\n<font color='green'>↓12%</font>\n<font color='red'>↑5%</font>\n<font color='green'>↓25%</font>",
                            }
                        ],
                    },
                ],
            },
        ]
    }
)
# 调用示例
send_card_message_v1("Sample Card", msg)


def send_card_message(title, table_data):
    headers = {"Content-Type": "application/json"}

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"content": title, "tag": "plain_text"}},
            "elements": [{"tag": "lark_md", "content": generate_table_content(table_data)}],
        },
    }

    response = requests.post(webhook_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Card message sent successfully.")
    else:
        print("Failed to send card message. Error:", response.text)


def generate_table_content(table_data):
    table_content = "| " + " | ".join(table_data[0]) + " |\n"
    table_content += "| " + " | ".join(["---"] * len(table_data[0])) + " |\n"

    for row in table_data[1:]:
        table_content += "| " + " | ".join(row) + " |\n"

    return table_content


# 调用示例
table_data = [["Name", "Age", "Country"], ["John", "30", "USA"], ["Alice", "25", "Canada"], ["Bob", "35", "UK"]]
# send_card_message("Table Card", table_data)
