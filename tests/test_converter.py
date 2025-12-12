def format_time(seconds):
    """Конвертирует секунды в формат SRT времени (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def split_text_to_segments(text, chars_per_segment=50):
    """Разбивает текст на сегменты по словам"""
    words = text.split()
    segments = []
    current_segment = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > chars_per_segment and current_segment:
            segments.append(" ".join(current_segment))
            current_segment = [word]
            current_length = len(word)
        else:
            current_segment.append(word)
            current_length += len(word) + 1

    if current_segment:
        segments.append(" ".join(current_segment))

    return segments


def create_srt(text, duration, chars_per_segment=50):
    """Создает SRT контент из текста"""
    segments = split_text_to_segments(text, chars_per_segment)

    if not segments:
        return ""

    segment_duration = duration / len(segments)
    srt_content = []

    for i, segment_text in enumerate(segments, 1):
        start_time = (i - 1) * segment_duration
        end_time = i * segment_duration

        srt_content.append(f"{i}")
        srt_content.append(f"{format_time(start_time)} --> {format_time(end_time)}")
        srt_content.append(segment_text)
        srt_content.append("")

    return "\n".join(srt_content)
