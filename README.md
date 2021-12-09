#  json-to-typescript-interfaces

> JSON converter for typescript interfaces

## Developing

```bash
poetry shell
```

### Install dependencies

```bash
poetry install
```

## Executing

```bash
cat example.json | python json_to_ts/main.py
```

### Input example
```json
{
  "@id": 1,
    "abilities": [
      {
        "ability": {
          "name": "overgrow",
          "url": "https://pokeapi.co/api/v2/ability/65/"
        },
        "is_hidden": false,
        "slot": 1
      },
      {
        "ability": {
          "name": "chlorophyll",
          "url": "https://pokeapi.co/api/v2/ability/34/"
        },
        "is_hidden": true,
        "slot": 3
      }
    ],
    "base_experience": 64,

    ...

```

### Output example

```typescript
export interface Ability {
  name: string;
  url: string;
}

export interface Abilitie {
  ability: ability;
  isHidden: boolean;
  slot: number;
}

export interface Form {
  name: string;
  url: string;
}

...

```

## Testing

```bash
pytest -v
```

