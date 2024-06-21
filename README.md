### Install
```
curl -sSL https://install.python-poetry.org | python3 -
poetry install --no-root
```

### Testing

Tested against 5,000 real CURPs. Errors classified as:

```
outer_name     0
date           0
gender         0
state          0
inner_name     1
homonimia     74
checksum       0
```

(Homonym errors can't be prevented).