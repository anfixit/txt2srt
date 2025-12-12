import io

from flask import Flask, render_template, request, send_file

from txt2srt.converter import create_srt

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    # Получаем текст либо из поля, либо из файла
    transcript = request.form.get("transcript", "").strip()
    uploaded_file = request.files.get("file")

    # Если загружен файл, читаем из него
    if uploaded_file and uploaded_file.filename:
        transcript = uploaded_file.read().decode("utf-8")

    if not transcript:
        return "Ошибка: нужно либо вставить текст, либо загрузить файл", 400

    # Получаем параметры
    hours = int(request.form.get("hours", 0))
    minutes = int(request.form.get("minutes", 0))
    seconds = int(request.form.get("seconds", 0))

    # Переводим в секунды
    duration = hours * 3600 + minutes * 60 + seconds

    if duration <= 0:
        return "Ошибка: длительность должна быть больше нуля", 400

    chars_per_segment = int(request.form.get("chars_per_segment", 50))

    # Создаём SRT
    srt_content = create_srt(transcript, duration, chars_per_segment)

    # Создаём файл в памяти
    srt_file = io.BytesIO()
    srt_file.write(srt_content.encode("utf-8"))
    srt_file.seek(0)

    return send_file(
        srt_file,
        mimetype="text/plain",
        as_attachment=True,
        download_name="subtitles.srt",
    )


if __name__ == "__main__":
    app.run(debug=True)
