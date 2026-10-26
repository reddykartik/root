1. check the integrity of the `pipeline.bin` file:
```bash
$ sha256sum pipeline.bin
d706e258bd29cdaaccab12e05a9ffb86a728332dd67629525056492b939da8a8  pipeline.bin
```

2. local development
```bash
cd ./deployment
uvicorn predict:app --host 0.0.0.0 --port 9696
```

3. checking endpoints
```bash
# get url -- checking the model checksum as health response
curl -s -w '\n' http://127.0.0.1:9696/
pipeline.bin: d706e258bd29cdaaccab12e05a9ffb86a728332dd67629525056492b939da8a8

# post url -- lead score prediction
curl -s -w '\n' http://127.0.0.1:9696/predict \
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

4. deployment
 * building phase
  ```bash
  # Nix
  nix build ./deployment#lead-score-image
  podman load < result
  
  # docker or podman
  docker build -t lead-score ./deployment
  ```

  * run
  ```bash
  docker run --rm -p 9696:9696 lead-score:latest
  ```
