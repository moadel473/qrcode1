from flask import Flask, render_template, request, jsonify, send_file
import qrcode
import os

app = Flask(__name__)

SAVE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "qrcode")
os.makedirs(SAVE_DIR, exist_ok=True)


@app.route("/")
def intro():
    return render_template("index.html")


@app.route("/generator")
def generator():
    return render_template("generator.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    url = data.get("url", "").strip()
    filename = data.get("filename", "qrcode").strip() or "qrcode"

    if not url:
        return jsonify({"success": False, "message": "الرابط مطلوب"}), 400

    # Sanitize filename
    safe_name = "".join(c for c in filename if c.isalnum() or c in "-_")
    if not safe_name:
        safe_name = "qrcode"

    file_path = os.path.join(SAVE_DIR, f"{safe_name}.png")

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)
        return jsonify({
            "success": True,
            "message": "تم حفظ صورة QR بنجاح! 🎉",
            "path": file_path
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"حدث خطأ: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
