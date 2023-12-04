# generate.py - Flaskアプリケーション
from flask import Flask, request, render_template
from openai import OpenAI
import base64
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    image_processing = False  # 画像処理中のフラグ

    if request.method == "POST":
        prompt = request.form["prompt"]

        image_processing = True  # 画像処理開始
        print("image_processing:", image_processing)  # コンソールに出力
        # 受け取ったプロンプトをコンソールに出力
        print("受け取ったプロンプト:", prompt)

        # ここでOpenAI APIを呼び出す
        client = OpenAI(api_key="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")
        response = client.images.generate(
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
            filename = f"./dall-e-3_{int(time.time())}_{i}.png"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(d.b64_json))

        # 画像データをBase64文字列として取得
        image_data = response.data[0].b64_json    

        # return "画像が生成されました！"
    return render_template("prompt.html", image_data=image_data, image_processing=image_processing)

if __name__ == "__main__":
    app.run(debug=True)
