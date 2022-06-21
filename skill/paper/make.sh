cd $(dirname $0)

pandock() {
    docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) "$@"
}

pandock pandoc-skill --biblatex content.md -o content.tex

pandock --entrypoint pdflatex pandoc-skill paper
pandock --entrypoint biber pandoc-skill paper
pandock --entrypoint pdflatex pandoc-skill paper
