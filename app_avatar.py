# app_avatar.py
from flask import Flask, request, render_template, jsonify
import os
from openai import OpenAI
import base64
import time

app = Flask(__name__)

# ファイル保存用のディレクトリ設定
UPLOAD_FOLDER = 'uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OpenAIクライアントのインスタンス化
openai_client = OpenAI(api_key="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")  # APIキーを直接設定

# ホームページのルート
@app.route('/')
def home():
    return render_template('index.html')

# 画像アップロードのルート
@app.route('/upload', methods=['POST'])
def upload_image():
    # ...
    return "画像がアップロードされました"

# 画像解析のルート
@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    data = request.json
    image_url = data['image_url']
    print("Received image URL:", image_url)  # デバッグ出力

    # OpenAIのAPIを使用して画像を解析
    response = openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                       "text": "Describe the person in the image, noting glasses and beard, hair color, hair texture, and clothing and color from the chest up. Detail the hair in particular. Do not mention background elements, facial expressions or personal details."
                    #  "text": "what's in this image?."
                    # "text": "Describe the person in the image, noting glasses and beard, hair color, hair texture, and clothing and color from the chest up. Do not mention background elements or facial expressions."
                     },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url  # この部分を動的に設定
                        }
                    }
                ]
            }
        ],
        max_tokens=150
    )

    content = response.choices[0].message.content
    print(content)  # デバッグ出力

    # 解析結果をJSON形式で返す
    return jsonify(content)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json

    # 受け取ったデータをコンソールに出力
    print("受け取ったデータ:", data)

    prompt = data['prompt']

    if request.method == "POST":

        # ここでOpenAI APIを呼び出す
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json",
            quality="standard",
            style="vivid"
        )
    
        # 画像を保存
        for i, d in enumerate(response.data):
             # 'image' フォルダ内にファイルを保存
            filename = f"static/img/dall-e-3_{int(time.time())}_0.png"
            
            with open(filename, "wb") as f:
                f.write(base64.b64decode(d.b64_json))

    # 保存した画像のパスをテンプレートに渡す
    image_path = f"img/dall-e-3_{int(time.time())}_0.png"
    # return render_template("avatar.html", image_path=image_path)
    return jsonify({"image_path": image_path})

if __name__ == '__main__':
    app.run(debug=True)
