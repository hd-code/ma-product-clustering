cd $(dirname $0)
SELF="$(basename $0)"

export PIPENV_VERBOSITY=-1

CMD="$1"
shift

case $CMD in
  check)
    echo "\n--- Format codebase:"
    sh $SELF format
    echo "\n--- Typecheck codebase:"
    sh $SELF lint
    echo "\n--- Test codebase:"
    sh $SELF test
    ;;
  coverage)
    pipenv run coverage run -m unittest discover -p '*_test.py'
    pipenv run coverage report -m --skip-covered
    ;;
  format)
    pipenv run python -m isort --profile black ./src
    pipenv run python -m black ./src
    ;;
  init)
    pipenv --rm
    pipenv install --dev
    ;;
  install)
    pipenv install "$@"
    ;;
  lint)
    pipenv run python -m mypy src
    ;;
  run)
    pipenv run python "$@"
    ;;
  test)
    pipenv run python -m unittest discover -p '*_test.py' "$@"
    ;;
  *)
    echo "Usage: $0 CMD"
    echo "  check       – does 'format', 'lint' and 'test'"
    echo "  coverage    – checks the code coverage of all unit tests"
    echo "  format      – format all source code files"
    echo "  init        – setup environment with all dependencies"
    echo "  install PKG – install PKG into environment (add '--dev' for dev dependencies)"
    echo "  lint        – static check the source code, especially the types"
    echo "  run PY_FILE – runs a python file"
    echo "  test        – run all unit tests"
esac
