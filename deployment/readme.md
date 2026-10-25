- check the integrity of the `pipeline.bin` file:
```bash
$ sha256sum pipeline.bin
d706e258bd29cdaaccab12e05a9ffb86a728332dd67629525056492b939da8a8  pipeline.bin
```

1. checking endpoints
```bash
// get url 
$ curl -s -w '\n' http://0.0.0.0:9696/
pipeline.bin: d706e258bd29cdaaccab12e05a9ffb86a728332dd67629525056492b939da8a8

// post url
$ curl -s -w '\n' http://0.0.0.0:9696/predict \
    -H 'Content-Type: application/json' \
    -d '{
      "lead_source":"organic_search",
      "industry":"technology",
      "employment_status":"employed",
      "location":"europe",
      "number_of_courses_viewed":4,
      "annual_income":80304.0,
      "interaction_count":7,
      "lead_score":0.74
    }'
{"probability":0.9291428210576756}
```

