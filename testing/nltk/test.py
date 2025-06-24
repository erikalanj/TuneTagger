from blah import test


def main():
    with open("material.txt", "w") as f:
        f.write(test)


if __name__ == "main":
    main()
