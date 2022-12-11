import functools
import itertools
import typing as t
import unicodedata
import re
import os
import numpy as np
from enum import unique, Enum
from keras_transformer import get_model, decode
import tensorflow as tf


class Token(str, Enum):
    PAD = "<PAD>"
    START = "<START>"
    END = "<END>"


@unique
class TranslatorBuilderMode(str, Enum):
    AUTO = "auto"
    LOAD = "load"
    TRAIN = "train"


Seq = t.List[t.Union[str, Token]]
Seqs = t.List[Seq]
Pair = t.Tuple[str, str]
Pairs = t.List[Pair]
Vector = t.List[int]
Vectors = t.List[Vector]
Vocabulary = t.Dict[str, int]
InvVocabulary = t.Dict[int, str]
Model = tf.keras.Model


path = os.path.dirname(os.path.abspath(__file__))


def to_ascii(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def normalize(s: str) -> str:
    s = to_ascii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s


def split_by_words(seq: str) -> Seq:
    return seq.split(" ")


def parse(path: str, sep: str = ",", reverse: bool = False) -> Pairs:
    with open(path, mode="r", encoding="utf-8-sig") as f:
        lines = f.read().split("\n")[:-1]

    pairs: Pairs = []

    for line in lines:
        source, target = line.split(sep)
        pairs.append((source, target) if not reverse else (target, source))

    return pairs


def preprocess(pairs: Pairs) -> t.Tuple[Seqs, Seqs]:
    # Se separan las secuencias en palabras.
    split = map(lambda pair: map(split_by_words, pair), pairs)

    # Agrupa los elementos de un mismo índice en una misma lista.
    # La estructura final es una lista de 2 listas: las secuencias de entradas
    # y las de salida.
    return tuple(map(list, zip(*split)))


def build_vocab(tokens: Seqs) -> Vocabulary:
    vocab: Vocabulary = {Token.PAD: 0, Token.START: 1, Token.END: 2}

    for token in itertools.chain(*tokens):
        if token not in vocab:
            vocab[token] = len(vocab)

    return vocab


def load(model: Model, path: str) -> None:
    model.load_weights(f"{path}/weights")  # type: ignore


def prepare(
    source_tokens: Seqs,
    target_tokens: Seqs,
    source_vocab: Vocabulary,
    target_vocab: Vocabulary,
) -> t.Tuple[Vectors, Vectors, t.List[Vectors]]:
    encode_tokens: Seqs = [[Token.START] + tokens + [Token.END] for tokens in source_tokens]
    decode_tokens: Seqs = [[Token.START] + tokens + [Token.END] for tokens in target_tokens]
    output_tokens: Seqs = [tokens + [Token.END, Token.PAD] for tokens in target_tokens]

    source_max_len = len(max(encode_tokens, key=len))
    target_max_len = len(max(decode_tokens, key=len))

    def pad(tokens: Seq, max_len: int) -> Seq:
        return tokens + [Token.PAD] * (max_len - len(tokens))

    encode_tokens: Seqs = [pad(tokens, source_max_len) for tokens in encode_tokens]
    decode_tokens: Seqs = [pad(tokens, target_max_len) for tokens in decode_tokens]
    output_tokens: Seqs = [pad(tokens, target_max_len) for tokens in output_tokens]

    encode_input: Vectors = [[source_vocab[token] for token in tokens] for tokens in encode_tokens]
    decode_input: Vectors = [[target_vocab[token] for token in tokens] for tokens in decode_tokens]

    decode_output: t.List[Vectors] = [
        [[target_vocab[token]] for token in tokens] for tokens in output_tokens
    ]

    return encode_input, decode_input, decode_output


def train(
    model: Model,
    source_tokens: Seqs,
    target_tokens: Seqs,
    source_vocab: Vocabulary,
    target_vocab: Vocabulary,
    outpath: str,
    epochs: int = 15,
) -> None:
    encode_input, decode_input, decode_output = prepare(
        source_tokens, target_tokens, source_vocab, target_vocab
    )

    # logger = tf.keras.callbacks.CSVLogger(f"{outpath}/history.csv", append=True)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=f"{outpath}/weights",
        save_weights_only=True,
        save_best_only=True,
        save_freq="epoch",
        monitor="loss",
        mode="auto",
        verbose=1,
    )

    model.fit(  # type: ignore
        x=[np.array(encode_input), np.array(decode_input)],
        y=np.array(decode_output),
        validation_split=0.25,
        epochs=epochs,
        batch_size=32,
        callbacks=[checkpoint],
    )


def assemble(source_vocab: Vocabulary, target_vocab: Vocabulary):
    model: Model = get_model(
        token_num=max(len(source_vocab), len(target_vocab)),
        embed_dim=32,
        encoder_num=2,
        decoder_num=2,
        head_num=4,
        hidden_dim=128,
        dropout_rate=0.05,
        use_same_embed=True,
    )

    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])  # type: ignore
    return model


def get_basepath(source: str, target: str) -> str:
    return f"{path}/translations/{source}_{target}"


def get_dspath(source: str, target: str) -> str:
    basepath = get_basepath(source, target)
    return f"{basepath}/dataset.txt"


def get_outpath(source: str, target: str) -> str:
    basepath = get_basepath(source, target)
    return f"{basepath}/out"


@functools.lru_cache
def build_translator(
    source: str,
    target: str,
    mode: TranslatorBuilderMode = TranslatorBuilderMode.LOAD,
    **kwargs: int,
) -> t.Callable[[str], str]:
    dspath = get_dspath(source, target)
    reverse = not os.path.isfile(dspath)

    # Comprueba si el dataset existe. Si no, utiliza el inverso.
    if reverse:
        dspath = get_dspath(target, source)

    pairs = parse(dspath, sep=",", reverse=reverse)
    source_tokens, target_tokens = preprocess(pairs)

    source_vocab = build_vocab(source_tokens)
    target_vocab = build_vocab(target_tokens)
    target_vocab_inv: InvVocabulary = {v: k for k, v in target_vocab.items()}

    model = assemble(source_vocab, target_vocab)
    outpath = get_outpath(source, target)

    if mode == TranslatorBuilderMode.AUTO:
        mode = (
            TranslatorBuilderMode.LOAD
            if os.path.isfile(f"{outpath}/checkpoint")
            else TranslatorBuilderMode.TRAIN
        )

    if mode == TranslatorBuilderMode.LOAD:
        load(model, outpath)

    elif mode == TranslatorBuilderMode.TRAIN:
        train(model, source_tokens, target_tokens, source_vocab, target_vocab, outpath, **kwargs)

    def translator(input: str) -> str:
        tokens: Seq = split_by_words(normalize(input)) + [Token.END, Token.PAD]
        input_tokens: Vector = [source_vocab[token] for token in tokens]

        decoded: Vector = decode(
            model,
            input_tokens,
            start_token=target_vocab[Token.START],
            end_token=target_vocab[Token.END],
            pad_token=target_vocab[Token.PAD],
        )

        return " ".join(target_vocab_inv[token] for token in decoded[1:-1])

    return translator
