Example config from [Demo](https://huggingface.co/spaces/PIISA/PIISA_Demo/tree/main) space:
```
{
    "format": "piisa:config:full:v1",
    "config": [
        {
            "format": "piisa:config:pii-extract-plg-transformers:main:v1",
            "task_config": {
                "cachedir": "/home/user/app/cache",
                "reuse_engine": true,
                "aggregation": "max",
                "models": [
                    {
                        "lang_code": "en",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    },
                    {
                        "lang_code": "es",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    },
                    {
                        "lang_code": "de",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    },
                    {
                        "lang_code": "fr",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    },
                    {
                        "lang_code": "it",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    },
                    {
                        "lang_code": "pt",
                        "model": "Babelscape/wikineural-multilingual-ner"
                    }
                ]
            },
            "pii_list": [
                {
                    "type": "PERSON",
                    "lang": [
                        "en",
                        "es",
                        "it",
                        "pt",
                        "de",
                        "fr"
                    ],
                    "method": "model",
                    "extra": {
                        "map": "PER"
                    }
                },
                {
                    "type": "LOCATION",
                    "lang": [
                        "en",
                        "es",
                        "it",
                        "pt",
                        "de",
                        "fr"
                    ],
                    "method": "model",
                    "extra": {
                        "map": "LOC"
                    }
                }
            ]
        },
        {
            "format": "piisa:config:pii-extract:plugins:v1",
            "piisa-detectors-presidio": {
                "load": false
            }
        }
    ]
}
```