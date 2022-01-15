cd $(dirname $0)

export PIPENV_VERBOSITY=-1

CMD="$1"
shift

case $CMD in
  format)
    pipenv run python -m autopep8 -ir .
    ;;
  init)
    pipenv --rm
    pipenv install --dev
    ;;
  install)
    pipenv install "$@"
    ;;
  run)
    pipenv run python "$@"
    ;;
  test)
    pipenv run python -m unittest discover -s src -p '*_test.py'
    ;;
  *)
    echo "Usage: $0 CMD"
    echo "  format      – format all source code files"
    echo "  init        – setup environment with all dependencies"
    echo "  install PKG – install PKG into environment (add '--dev' for dev dependencies)"
    echo "  run PY_FILE – runs a python file"
    echo "  test        – run all unit tests"
esac
