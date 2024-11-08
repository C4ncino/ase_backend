from train2 import main as train
from prepare_data import WORDS


def main():
    n = len(WORDS)
    current_words = WORDS[n // 2: n]

    train(current_words)


if __name__ == "__main__":
    main()
