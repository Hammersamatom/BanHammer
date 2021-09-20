def main():
    lines = [];
    with open("list.txt") as F:
        lines = F.readlines();
        lines = [line.rstrip() for line in lines];
    lines = [i for i in lines if i];
    lines = list(set(lines));
    lines.sort();
    with open("list_new.txt", "w") as R:
        for i in lines:
            R.write(i + "\n");

main();