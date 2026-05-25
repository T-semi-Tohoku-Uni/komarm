# komarm

## Setup
install dependency
```bash
cd komarm
uv sync
```
To record log to wandb while training arm, copy wandb api key and paste to .env
```bash
echo 'WANDB_API_KEY=***' >> .env
```

## issacsim
execute handless
```bash
PUBLIC_IP=$(tailscale ip -4)
uv run isaacsim isaacsim.exp.full.streaming --no-window --/app/livestream/publicEndpointAddress=$PUBLIC_IP --/app/livestream/port=49100
```

## Train and Evaluation
```bash
uv run -m  script.rsl_rl.train --task Isaac-KOMARM-Reach-v0 --headless
```

```bash
uv run -m script.rsl_rl.play \
  --task Isaac-KOMARM-Reach-Play-v0 \
  --headless \
  --enable_cameras \
  --livestream 1 \
  --kit_args "--no-window --/app/livestream/publicEndpointAddress=${PUBLIC_IP} --/app/livestream/port=49100"
```
