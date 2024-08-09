from transformers import BertForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset, load_metric
import pdfplumber
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
from transformers import AutoTokenizer
from deep_translator import GoogleTranslator


def extrair_texto_do_pdf(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

texto = extrair_texto_do_pdf('Documento sem título (1).pdf')

to_translate = texto
translated = GoogleTranslator(source='auto', target='en').translate(to_translate)

pergunta = "What is the value of the permit holder fee?"
resposta = qa_pipeline(question=pergunta, context=translated)
print(resposta)


