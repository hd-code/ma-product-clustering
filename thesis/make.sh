# uses the pandoc template of the University
IMAGE_NAME='pandoc-fhe'

# go to correct directory
cd $(dirname $0)

# compile pdf from markdown
docker run -it --rm -v ${PWD}:/data $IMAGE_NAME thesis *.md
