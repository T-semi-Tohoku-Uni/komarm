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

## issacsim
execute handless
```bash
PUBLIC_IP=$(tailscale ip -4)
uv run isaacsim isaacsim.exp.full.streaming --no-window --/app/livestream/publicEndpointAddress=$PUBLIC_IP --/app/livestream/port=49100
```
