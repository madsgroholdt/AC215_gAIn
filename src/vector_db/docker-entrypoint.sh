echo "Container is running!!!"

args="$@"
echo $args

if [[ -z ${args} ]]; then
    echo "Running 'python cli.py --preprocess'..."
    pipenv run python cli.py --preprocess
else
    echo "Running custom command: $args"
    pipenv run python $args
fi
