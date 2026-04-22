from generator import generate_score
from lilypond import score_to_lily


def main():
    score = generate_score(8)

    lilypond_code = score_to_lily(score)

    with open("output.ly", "w") as f:
        f.write(lilypond_code)

    print("Generated output.ly")
    print("Run: lilypond output.ly")


if __name__ == "__main__":
    main()
