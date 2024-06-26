import cv2
import pytesseract
from fuzzywuzzy import fuzz
import sqlite3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def analisar_ocr(imagem_path, banco):
    img = cv2.imread(imagem_path)

    img_inv = cv2.bitwise_not(img)
    img_gray = cv2.cvtColor(img_inv, cv2.COLOR_BGR2GRAY)

    img_blur = cv2.GaussianBlur(img_gray, (1, 1), 0)
    img_processed = cv2.threshold(
        img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    text_detected = pytesseract.image_to_string(
        img_processed, lang="por", config="--psm 6"
    )
    text_cleaned = text_detected.strip().replace("\n", " ")

    if text_cleaned:
        results = []
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        cursor.execute('SELECT pergunta, resposta FROM perguntas_respostas')
        rows = cursor.fetchall()
        
        for row in rows:
            question = row[0]
            answers = row[1:]
            question_cleaned = question.strip().replace("\n", " ")

            for sim_limit in range(68, 81):
                similarity = fuzz.ratio(
                    question_cleaned.lower(), text_cleaned.lower()
                )

                if similarity > sim_limit:
                    results.append(
                        (question, ", ".join(answers), similarity)
                    )

        conn.close()

        results.sort(key=lambda x: x[2], reverse=True)

        if results:
            question, answers, similarity = results[0]
            return question, answers
        else:
            return text_cleaned, "Resposta não encontrada."
    else:
        return "Nenhum texto detectado.", ""
