# komarm

## setup
install dependency
```bash
cd komarm
uv sync
```

install lsaac lab
```bash

```

## Train and Evaluation
```bash
uv run -m  komarm.scripts.rsl_rl.train --task Isaac-SO-ARM100-Reach-Play-v0 --headless
```

```bash
uv run -m komarm.scripts.rsl_rl.play \
  --task Isaac-SO-ARM100-Reach-Play-v0 \
  --headless \
  --enable_cameras \
  --livestream 1 \
  --kit_args "--no-window --/app/livestream/publicEndpointAddress=${PUBLIC_IP} --/app/livestream/port=49100"
```

## issacsim
execute handless
```bash
PUBLIC_IP=$(tailscale ip -4)
uv run isaacsim isaacsim.exp.full.streaming --no-window --/app/livestream/publicEndpointAddress=$PUBLIC_IP --/app/livestream/port=49100
```
