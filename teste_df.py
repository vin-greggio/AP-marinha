import polars as pl

df = pl.read_ndjson('hf://datasets/KbsdJames/Omni-MATH/test.jsonl')

q = df.with_columns([
    pl.col('difficulty').alias('proporcao de dificuldade')
    ])
print(q)

# with_columns, recebe uma lista e é tipo um mutate, cria algo novo com .alias('nome')
# is_in
