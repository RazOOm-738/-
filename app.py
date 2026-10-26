from fileinput import filename

from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("website.html")

@app.route("/download", methods=["POST"])
def downloads_video():
    video_url = request.form.get("video_url")

    if not video_url:
        return render_template("website.html", error_msg="Вы не вставили ссылку!")

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

            filename = ydl.prepare_filename(info)

            if not os.path.exists(filename):
                base, _ = os.path.splitext(filename)
                for ex, in [".mp4", ".mvk", ".webm"]:
                    if os.path.exists(base + ex):
                        filename = base + ex
                        break

        return send_file(filename, as_attachment=True)

    except Exception as e:
             return render_template("website.html", error_msg=f"Ошибка: {e}")
if __name__ == "__main__":
    app.run(debug=True)